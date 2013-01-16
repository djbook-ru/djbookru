from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from ... utils import forms
from .. models import User, EmailConfirmation

from . factories import *

forms.ReCaptchaField.clean = lambda self, data, initial: data


class ViewsTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='user', password='user')

    def login(self):
        self.client.login(username='user', password='user')

    def test_create(self):
        url = reverse('accounts:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'newuser',
            'email': 'newuser@example.org',
            'password1': 'newuser',
            'password2': 'newuser',
            'captcha': '123'
        }
        mail.outbox = []
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username=data['username'])
        self.assertFalse(user.is_valid_email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(self.client.login(username=user.username, password=data['password1']))

        # confirm email
        confirmation = user.emailconfirmation_set.all()[:1].get()
        confirmation_url = reverse('accounts:confirm_email', args=[confirmation.confirmation_key])
        response = self.client.get(confirmation_url)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.is_valid_email)

        # try to resend comfirmation email with valid email
        EmailConfirmation.objects.all().delete()
        mail.outbox = []
        resend_url = reverse('accounts:resend_confirmation_email')
        response = self.client.get(resend_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(EmailConfirmation.objects.exists())
        self.assertFalse(mail.outbox)

        # change email
        user.email = 'newemal@example.org'
        user.save()
        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.emailconfirmation_set.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(user.is_valid_email)

        # try to resend comfirmation email until old one not expired
        mail.outbox = []
        resend_url = reverse('accounts:resend_confirmation_email')
        response = self.client.get(resend_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(mail.outbox)
        self.assertEqual(user.emailconfirmation_set.count(), 1)

        # reset confirmation email
        user.emailconfirmation_set.all().delete()
        mail.outbox = []
        response = self.client.get(resend_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(user.emailconfirmation_set.count(), 1)

        # logout
        logout_url = reverse('accounts:logout')
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 302)

    def test_profile(self):
        url = reverse('accounts:profile', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        self.login()
        url = reverse('accounts:edit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'newemail@example.org'
        }
        mail.outbox = []
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, data['email'])
        self.assertFalse(user.is_valid_email)
        self.assertEqual(len(mail.outbox), 1)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.generic import ListView

from src.accounts.backends import CustomUserBackend
from src.accounts.forms import UserEditForm, CreateUserForm, SavePositionForm
from src.accounts.models import User, EmailConfirmation, EMAIL_CONFIRMATION_DAYS


def users_map(request):
    user = request.user
    other_users = User.objects.all()

    if user.is_authenticated():
        user_position = user.get_position()
        other_users = other_users.exclude(pk=user.pk)
    else:
        user_position = None

    other_positions = (u.get_position() for u in other_users)
    other_positions = [p for p in other_positions if p]

    context = {
        'user_position_json': json.dumps(user_position),
        'other_positions_json': json.dumps(other_positions)
    }
    return TemplateResponse(request, 'accounts/map.html', context)


def save_user_position(request):
    user = request.user

    if not user.is_authenticated():
        return JsonResponse({
            'error': ugettext('Authenticate please!')
        }, status=400)

    form = SavePositionForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return JsonResponse({})
    else:
        return JsonResponse({
            'error': ugettext('invalid form')
        }, status=400)


def create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save()
            messages.success(request, _('Account created success! Confirm your email.'))
            return redirect('accounts:login')
        messages.error(request, _('Please correct the error below.'))
    else:
        form = CreateUserForm()

    context = {
        'form': form
    }
    return TemplateResponse(request, 'accounts/create.html', context)


def profile(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    context = {
        'user_obj': user_obj,
        'user_position_json': json.dumps(user_obj.get_position())
    }
    return TemplateResponse(request, 'accounts/profile.html', context)


class VotedTopicsListView(ListView):
    template_name = 'accounts/profile_voted.html'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.user.voted_topics.all()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['user_obj'] = self.user
        context['title'] = _('voted topics')
        return context

profile_topics = VotedTopicsListView.as_view()


class VotedPostsListView(ListView):
    template_name = 'accounts/profile_voted.html'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.user.voted_posts.all()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['user_obj'] = self.user
        context['title'] = _('voted posts')
        return context

profile_posts = VotedPostsListView.as_view()


@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, _('Profile changed success! Confirm your email if it was changed.'))
            return redirect(request.user)
        messages.error(request, _('Please correct the error below.'))
    else:
        form = UserEditForm(instance=request.user)

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'accounts/edit.html', context)


def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    user = EmailConfirmation.objects.confirm_email(confirmation_key)

    if not user:
        messages.error(request, _('Confirmation key expired.'))
        return redirect('/')
    else:
        messages.success(request, _('Email is confirmed.'))

    # FIXME: Do not hardcode backend
    user.backend = "%s.%s" % (CustomUserBackend.__module__, CustomUserBackend.__name__)
    user = auth_login(request, user)
    return redirect('accounts:edit')


@login_required
def resend_confirmation_email(request):
    if request.user.is_valid_email:
        messages.error(request, _('Your email is already confirmed.'))
    elif not request.user.email:
        messages.error(request, _('Add email to your profile.'))
    else:
        EmailConfirmation.objects.delete_expired_confirmations()
        if EmailConfirmation.objects.filter(user=request.user).exists():
            msg = _('We have sent you confirmation email. ''New one you can get in %(days)s days')
            msg = msg % {'days': EMAIL_CONFIRMATION_DAYS}
            messages.error(request, msg)
        else:
            EmailConfirmation.objects.send_confirmation(request.user)
            messages.success(request, _('Confirmation email is sent.'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

# -*- coding: utf-8 -*-

import json
from . backends import CustomUserBackend
from . forms import UserEditForm, CreateUserForm, SavePositionForm
from . models import User, EmailConfirmation, EMAIL_CONFIRMATION_DAYS
from .. comments.models import Comment
from .. decorators import render_to, render_to_json
from .. doc_comments.models import Comment as DocComment
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext


LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')
PAGINATED_TOPICS_COUNT = getattr(settings, 'PAGINATED_TOPICS_COUNT', 10)
PAGINATED_POSTS_COUNT = getattr(settings, 'PAGINATED_POSTS_COUNT', 10)


@render_to('accounts/map.html')
def user_map(request):
    user = request.user
    other_users = User.objects.all()

    if user.is_authenticated():
        user_position = user.get_position()
        other_users = other_users.exclude(pk=user.pk)
    else:
        user_position = None

    other_positions = (u.get_position() for u in other_users)
    other_positions = [p for p in other_positions if p]

    return {
        'user_position_json': json.dumps(user_position),
        'other_positions_json': json.dumps(other_positions)
    }


@render_to_json
def save_user_position(request):
    user = request.user

    if not user.is_authenticated():
        return {
            'error': ugettext(u'Authenticate please!')
        }

    form = SavePositionForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return {}
    else:
        return {
            'error': ugettext(u'invalid form')
        }


@render_to('accounts/create.html')
def create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Account created success! Confirm your email.'))
            return redirect('accounts:login')
        messages.error(request, _(u'Please correct the error below.'))
    else:
        form = CreateUserForm()
    return {
        'form': form
    }


def logout(request):
    # FIXME: Looks like cant be replaced with build-in view
    from django.contrib.auth import logout

    logout(request)
    redirect_to = request.GET.get(auth.REDIRECT_FIELD_NAME, LOGOUT_REDIRECT_URL)
    return redirect(redirect_to)


@render_to('accounts/profile.html')
def profile(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    user_position = user_obj.get_position()
    return {
        'user_obj': user_obj,
        'user_position_json': json.dumps(user_position)
    }


class VotedTopicsListView(ListView):
    model = User
    template_name = 'accounts/profile_voted.html'
    paginate_by = PAGINATED_TOPICS_COUNT

    def get_queryset(self):
        self.user = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return self.user.voted_topics.all()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['user_obj'] = self.user
        context['title'] = _('voted topics')
        return context

profile_topics = VotedTopicsListView.as_view()


class VotedPostsListView(ListView):
    model = User
    template_name = 'accounts/profile_voted.html'
    paginate_by = PAGINATED_POSTS_COUNT

    def get_queryset(self):
        self.user = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return self.user.voted_posts.all()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['user_obj'] = self.user
        context['title'] = _('voted posts')
        return context

profile_posts = VotedPostsListView.as_view()


@render_to('accounts/edit.html')
@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Profile changed success! Confirm your email if it was changed.'))
            return redirect(request.user)
        messages.error(request, _(u'Please correct the error below.'))
    else:
        form = UserEditForm(instance=request.user)
    return {
        'form': form,
    }


@render_to('accounts/notifications.html')
@login_required
def notifications(request):
    user = request.user
    reply_comments = list(Comment.get_reply_comments(user, only_new=False).order_by('-submit_date')[:30])
    reply_comments_count = Comment.get_reply_comments(user).count()

    doc_comments = list(DocComment.get_reply_comments(user, only_new=False)[:30])
    doc_comments_count = DocComment.get_reply_comments(user).count()

    last_comments_read = user.last_comments_read
    last_doc_comments_read = user.last_doc_comments_read

    user.last_comments_read = timezone.now()
    user.last_doc_comments_read = timezone.now()
    user.save()
    return {
        'reply_comments': reply_comments,
        'reply_comments_count': reply_comments_count,
        'doc_comments': doc_comments,
        'doc_comments_count': doc_comments_count,
        'last_comments_read': last_comments_read,
        'last_doc_comments_read': last_doc_comments_read
    }


def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    user = EmailConfirmation.objects.confirm_email(confirmation_key)

    if not user:
        messages.error(request, _(u'Confirmation key expired.'))
        return redirect('/')
    else:
        messages.success(request, _(u'Email is confirmed.'))

    user.backend = "%s.%s" % (CustomUserBackend.__module__, CustomUserBackend.__name__)
    user = auth_login(request, user)

    if request.user.is_authenticated():
        return redirect('accounts:edit')

    return redirect('/')


@login_required
def resend_confirmation_email(request):
    if request.user.is_valid_email:
        messages.error(request, _(u'Your email is already confirmed.'))
    elif not request.user.email:
        messages.error(request, _(u'Add email to your profile.'))
    else:
        EmailConfirmation.objects.delete_expired_confirmations()
        if EmailConfirmation.objects.filter(user=request.user).exists():
            messages.error(request, _(u'We have sent you confirmation email. New one you can get in %(days)s days') % {
                'days': EMAIL_CONFIRMATION_DAYS
            })
        else:
            EmailConfirmation.objects.send_confirmation(request.user)
            messages.success(request, _(u'Confirmation email is sent.'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auto_login
from django.contrib.auth import views as auth_views
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView
from django_hosts import reverse

from accounts.forms import SignUpForm
from accounts.tokens import account_activation_token


def authenticated(request):
    if request.user.is_authenticated:
        return redirect(reverse('home', host='www'))
    else:
        return None


def signup(request):
    auth = authenticated(request)
    if auth is not None:
        return auth
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)

                user.is_active = False
                user.save()
                # auto_login(request, user)
                current_site = get_current_site(request)
                mail_subject = '[Rhys Website] Activate your Rhys Website account.'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),})
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')

        else:
            form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auto_login(request, user)
        return HttpResponse('Thank you for your email confirmation. You\'ve been logged in.')
    else:
        return HttpResponse('Activation link is invalid!')


def deactivate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        email = user.email
        user.delete()
        return HttpResponse('The account associated with the email {} has been deleted.'.format(email))
    else:
        return HttpResponse('No action has been taken on any account as the link is invalid.')


def login(request):
    auth = authenticated(request)
    if auth is not None:
        return auth
    else:
        return auth_views.LoginView.as_view(template_name="accounts/login.html")(request)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = "accounts/my_account.html"
    success_url = reverse_lazy('edit_profile')

    def get_object(self, queryset=None):
        return self.request.user


def user_profile(request, username=None):
    if username is None:
        username = request.user.username
    profile_data = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {"profile_data": profile_data})

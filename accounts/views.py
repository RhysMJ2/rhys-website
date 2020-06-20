from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.views.generic import UpdateView, ListView
from django_hosts import reverse

from accounts.forms import SignUpForm, UserUpdateForm
from accounts.tokens import account_activation_token
from boards.models import Post


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
                current_site = get_current_site(request)
                mail_subject = '[Rhys Website] Activate your Rhys Website account.'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user), })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                user.is_active = False
                user.save()
                # auto_login(request, user)

                return render(request, 'accounts/signup_done.html', {'form': form})

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

    return render(request, 'accounts/signup_confirm.html', {'user': user})


def deactivate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.delete()

    return render(request, 'accounts/signup_deactivated.html', {'user': user})


def change_email(request, uidb64, token): # todo finish
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=request.user.pk)
    if account_activation_token.check_token(uid, token):
        request.user.email = uid


def revert_email(request, uidb64, token):
    pass


def login(request):
    auth = authenticated(request)
    if auth is not None:
        return auth
    else:
        return auth_views.LoginView.as_view(template_name="accounts/login.html")(request)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = "accounts/my_account.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy('edit_profile')
    """
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

            current_site = get_current_site(request)
            mail_subject = '[Rhys Website] Changing your email.'
            message = render_to_string('accounts/acc_change_email.html', {
            'user': request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(form.cleaned_data.get('email'))),
            'token': account_activation_token.make_token(request.user.email), })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # todo need to send thus email after email changed
            '''
            mail_subject = "[Rhys Website] Account Email Changed"
            message = render_to_string('accounts/acc_active_email.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.email)),
                'token': account_activation_token.make_token(request.user.username), })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()'''
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    """
    def get_object(self, queryset=None):
        return self.request.user


def user_profile(request, username=None):
    if username is None:
        username = request.user.username
    profile_data = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {"profile_data": profile_data})


class UserProfileView(ListView):
    model = Post
    template_name = 'accounts/profile.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_data"] = User.objects.get(username=self.user.username)

        return super().get_context_data(**context)

    def get_queryset(self):
        user = self.request.user.username if self.kwargs.get("username") is None else self.kwargs.get("username")
        self.user = get_object_or_404(User, username=user)
        queryset = self.user.posts.order_by('created_at')
        return queryset

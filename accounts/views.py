from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auto_login
from django.contrib.auth import views as auth_views
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django_hosts import reverse

from accounts.forms import SignUpForm


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
                user = form.save()
                auto_login(request, user)
                return redirect(reverse('home', host='www'))
        else:
            form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})


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
    success_url = reverse_lazy('edit_account')

    def get_object(self, queryset=None):
        return self.request.user


def user_profile(request, username=None):
    if username is None:
        username = request.user.username
    profile_data = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {"profile_data": profile_data})

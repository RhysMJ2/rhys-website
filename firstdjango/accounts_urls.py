from django.shortcuts import redirect
from django.urls import path
from django_hosts import reverse

from accounts import views as accounts_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', accounts_view.signup, name='signup'),
    path('login/', accounts_view.login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('settings/password/reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('settings/password/reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('settings/password/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('settings/password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('settings/profile/', accounts_view.UserUpdateView.as_view(), name='edit_profile'),
    path('accounts/profile/', accounts_view.user_profile, name='user_profile'), # todo sticky sidebar doesn't work
    path('accounts/profile/<username>/', accounts_view.user_profile, name='user_profile'),
]

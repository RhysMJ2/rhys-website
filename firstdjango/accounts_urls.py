from django.shortcuts import redirect, render
from django.urls import path
from django_hosts import reverse

from accounts import views as accounts_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', accounts_view.signup, name='signup'),
    path('signup/activate/<uidb64>/<token>/', accounts_view.activate, name='activate'),
    path('signup/delete/<uidb64>/<token>/', accounts_view.deactivate, name='deactivate'),

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

    path('settings/profile/', accounts_view.UserUpdateView.as_view(), name='edit_profile'), # todo email verificatio here and unique email check
    # path('settings/privacy/'),

    path('accounts/profile/', accounts_view.UserProfileView.as_view(), name='user_profile'),
    # path('accounts/profile/details/'),
    path('accounts/profile/<username>/', accounts_view.UserProfileView.as_view(), name='user_profile'),
    # path('accounts/profile/<username>/posts/'),
]

handler404 = 'boards.views.error_404'
handler500 = 'boards.views.error_500'

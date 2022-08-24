from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordResetView, 
    PasswordResetConfirmView, 
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordChangeDoneView
    )


class CustomLoginView(LoginView):
    # authentication_form = None
    template_name = "accounts/login.html"
    # redirect_authenticated_user = False
from django.urls import path
from django.contrib.auth.views import LoginView
from authenticate.forms import EmailAuthenticationForm

urlpatterns = [
    path("login/", 
        LoginView.as_view(
            authentication_form =  EmailAuthenticationForm,
            next_page = '/admin/'
        ), 
        name = 'login'
    ),
]
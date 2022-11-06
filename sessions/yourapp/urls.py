from django.urls import path
from yourapp.views import firstView, secondView, clearSession


app_name = 'yourapp'

urlpatterns = [
    path("firstView", firstView.as_view(), name = 'firstView'),
    path("secondView", secondView.as_view(), name = 'secondView'),
    path("clear", clearSession.as_view(), name = 'clear'),
]

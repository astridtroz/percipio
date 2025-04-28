
from django.contrib import admin
from django.urls import path
from .views import RegistrationView, UserLoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login' ),
]

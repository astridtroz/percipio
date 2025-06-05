
from django.contrib import admin
from django.urls import path
from .views import RegistrationView, UserLoginView,UserPasswordResetView,ContributorProfileView,SendPasswordResetEmail, ProviderProfileView, UserChangePassword

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login' ),
    # Contributor's profile
    path('contributor/profile/', ContributorProfileView.as_view(), name='contributor-profile'),
    path('provider/profile/', ProviderProfileView.as_view(), name='provider-profile'),
    path('change_password/', UserChangePassword.as_view(), name='change_password' ),
    path('send-reset-password-email/', SendPasswordResetEmail.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',  UserPasswordResetView.as_view(), name='reset_password'),
    
]

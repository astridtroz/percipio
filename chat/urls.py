from django.urls import path
from .views import get_private_messages

urlpatterns = [
    path('messages/<str:username>/', get_private_messages, name='get_private_messages'),
]

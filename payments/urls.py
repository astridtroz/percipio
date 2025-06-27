from django.urls import path
from .views import CreateStripeAccount, CreatePaymentIntent, stripe_webhook

urlpatterns = [
    path('create-account/', CreateStripeAccount.as_view()),
    path('create-payment/', CreatePaymentIntent.as_view()),
    path('webhook/', stripe_webhook),
]

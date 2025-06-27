from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from user.models import MyUser
from .models import Payment
from tasks.models import Task
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY 
#create account for contributors
class CreateStripeAccount(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        user= request.user
        if user.user_type != 'contributor':
            return Response({"error": "Only contributors can onboard"}, status=403)
        
        account= stripe.Account.create(
            type="express",
            country="US",
            email=user.email
        )

        user.stripe_account_id= account.id
        user.save()

        account_link= stripe.AccountLink.create(
            account=account.id,
            refresh_url="https://367b-2401-4900-1f3d-c481-18b9-c111-1d3-4f6f.ngrok-free.app/stripe/refresh",
            return_url="https://367b-2401-4900-1f3d-c481-18b9-c111-1d3-4f6f.ngrok-free.app/stripe/return",
            type="account_onboarding"
        )

        return Response({"url": account_link.url})

class CreatePaymentIntent(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        task_id= request.data.get('task_id')
        amount= int(request.data.get('amount'))

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

        contributor = task.contributor

        if not contributor:
            return Response({"error": "No contributor assigned to this task"}, status=400)

        if not contributor.stripe_account_id:
            return Response({"error": "Contributor has no Stripe account"}, status=400)
        
        intent= stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
            transfer_data={
                'destination': contributor.stripe_account_id,
            }
        )

        payment=Payment.objects.create(
            task=task,
            provider=request.user,
            amount=amount,
            stripe_payment_intent= intent['id']
        )
        
        return Response({
            "client_secret": intent['client_secret']
        })

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_...'  # from Stripe dashboard

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        pi_id = intent['id']

        try:
            payment = Payment.objects.get(stripe_payment_intent=pi_id)
            payment.status = 'completed'
            payment.save()
        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)

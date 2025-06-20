from django.db import models
from user.models import Provider, Contributor
from tasks.models import Task

class Payment(models.Model):
    task= models.ForeignKey(Task, on_delete= models.CASCADE)
    provider= models.ForeignKey(Provider,on_delete= models.CASCADE)
    contributor= models.ForeignKey( Contributor, on_delete= models.CASCADE)
    amount= models.IntegerField(help_text= "In paisa (₹10 = 1000)")
    status= models.CharField(max_length=50,  default='pending')
    stripe_payment_intent=models.CharField(max_length=255,  blank=True, null=True)

    


from .models import *
from .views import *
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

#After user has registered, who is sending signal
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(user= instance)

@receiver(post_save, sender= User)
def save_customer(sender, instance, **kwargs):
	instance.customer.save()

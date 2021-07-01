"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Account, Profile, BusinessPartner

# signals here
@receiver(post_save, sender = Account, dispatch_uid = "create_profile")
def create_profile(sender, instance, created, **kwargs):
    if (created and instance.role != 'partner'):
        Profile.objects.create(account = instance)

@receiver(post_save, sender = Account, dispatch_uid = "create_partner")
def create_partner(sender, instance, created, **kwargs):
    if (created and instance.role == 'partner'):
        BusinessPartner.objects.create(account = instance)
"""

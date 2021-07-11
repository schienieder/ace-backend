from django.db.models.signals import post_delete
from django.dispatch import receiver
from api.models import Account, Client, BusinessPartner

# signals here
@receiver(post_delete, sender=Client, dispatch_uid="delete_client_account_signal")
def delete_client_account(sender, instance, *args, **kwargs):
    Account.objects.filter(id=instance.account.id).delete()


@receiver(
    post_delete, sender=BusinessPartner, dispatch_uid="delete_partner_account_signal"
)
def delete_partner_account(sender, instance, *args, **kwargs):
    Account.objects.filter(id=instance.account.id).delete()

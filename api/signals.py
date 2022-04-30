from multiprocessing import Event
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from api.models import (
    Account,
    Client,
    BusinessPartner,
    InterviewSchedule,
    EventBookings,
    Event,
    TransactionLog,
)

# signals here
@receiver(post_delete, sender=Client, dispatch_uid="delete_client_account_signal")
def delete_client_account(sender, instance, *args, **kwargs):
    Account.objects.filter(id=instance.account.id).delete()


@receiver(
    post_delete, sender=BusinessPartner, dispatch_uid="delete_partner_account_signal"
)
def delete_partner_account(sender, instance, *args, **kwargs):
    Account.objects.filter(id=instance.account.id).delete()


@receiver(post_save, sender=InterviewSchedule, dispatch_uid="update_booking_status")
def update_booking_status(sender, instance, *args, **kwargs):
    EventBookings.objects.filter(id=instance.booking.id).update(status="Accepted")


@receiver(
    pre_delete, sender=InterviewSchedule, dispatch_uid="delete_partner_account_signal"
)
def delete_partner_account(sender, instance, *args, **kwargs):
    EventBookings.objects.filter(booked_by=instance.client.id).update(status="Pending")


@receiver(post_save, sender=Event, dispatch_uid="create_update_event_signal")
def delete_partner_account(sender, instance, *args, **kwargs):
    TransactionLog.objects.create(
        event=instance, payment=instance.client_payment, status=instance.payment_status
    )

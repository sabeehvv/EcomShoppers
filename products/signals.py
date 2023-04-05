from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.admin.models import LogEntry, ADDITION
from django.urls import reverse
from orders.models import Orders
from django.contrib.contenttypes.models import ContentType


channel_layer = get_channel_layer()

@receiver(post_save, sender=Orders)
def send_notification_to_admin(sender, instance, created, **kwargs): # noqa  # noqa: F841
    if created:
        message = f"A new order #{instance.orderid} has been received."
        channel_layer.group_send("admin_notifications", {"type": "notify_admins", "message": message})
        # log the creation of the new order in the Django admin
        LogEntry.objects.log_action(
            user_id=instance.user.first_name,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.id,
            object_repr=f"{instance.orderid} - {instance.status} - ${instance.ordertotal}",
            action_flag=ADDITION,
            change_message=None,
        )

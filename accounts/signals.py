from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save , sender=User)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        User.objects.filter(username=instance).update(is_active=False)
        
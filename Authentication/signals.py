from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_password_history.models import UserPasswordHistory


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserPasswordHistory.objects.create(user=instance)
  
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        instance.userpasswordhistory.save()


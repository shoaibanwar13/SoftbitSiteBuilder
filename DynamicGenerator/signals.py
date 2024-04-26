from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Deactivate the user upon creation
        instance.is_active = False
        instance.save()
        # Create a corresponding profile for the user
        Profile.objects.create(user=instance)

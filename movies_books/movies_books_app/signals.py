# use of django signals to create a new profile instance for a user when they register.
from django.db.models.signals import post_save # signal that will be sent
from django.contrib.auth.models import User # object that will send the signal
from django.dispatch import receiver #this will receive the signal
from .models import Profile # operations will be performed on the profiles table

# receiver function run everytime a user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

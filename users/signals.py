from django.db.models.signals import post_save, pre_delete 
from django.dispatch import receiver 
from django.contrib.auth import get_user_model
User = get_user_model()

from trade.models import Profile 

# create user profile on sign up 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            firstname=instance.firstname,
            lastname=instance.lastname,
            username=instance,
            email=instance.email)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.Profile.save()
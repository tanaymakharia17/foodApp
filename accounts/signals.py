from .models import User, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver








@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance, created, **Kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('create the user profile-----------------------------------------------------')
    else:
        pass


# def pre_save_handler(sender, instance, **kwargs):
#     # Add your condition to determine whether to stop the save process
#     if condition:
#         # Raise a ValidationError to stop the saving process
#         raise ValidationError("Saving is not allowed.")

# post_save.connect(post_save_create_profile_reciever, sender=User)
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from main_page.models import user_information, user_friends

@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_information.objects.create(user=instance)
        user_friends.objects.create(user=instance)
    
@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):
        instance.profile_pic.save()
        instance.friends_user.save()
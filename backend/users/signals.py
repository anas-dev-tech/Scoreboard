from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Teacher

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TEACHER:
        Teacher.objects.create(user=instance)
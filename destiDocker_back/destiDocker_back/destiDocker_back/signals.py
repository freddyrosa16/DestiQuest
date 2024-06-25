# destiDocker_back/signals.py

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to DestiQuest'
        message = (
            f'Hi {instance.username},\n\n'
            f'Thank you for registering at DestiQuest!'
        )
        recipient_list = [instance.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

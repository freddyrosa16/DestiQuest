from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

"""
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
"""


# @receiver(user_logged_in)
# def send_login_email(sender, request, user, **kwargs):
# Modify this line to use email instead of username
# send_mail(
# 'Login Notification',
# f'Hello {user.email}, you have successfully logged in.',
# settings.DEFAULT_FROM_EMAIL,
# [user.email],
# fail_silently=False,
# )

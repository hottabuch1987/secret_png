# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.tasks import send_confirmation_code_email

User = get_user_model()


@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    """
    При создании нового пользователя отправляет код подтверждения через Celery.
    """
    if created and not instance.email_confirmed:
        # Отправляем задачу в Celery
        print('Отправляем задачу в Celery')
        send_confirmation_code_email.delay(str(instance.id))
# users/tasks.py
from celery import shared_task
from django.core.management import call_command
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


@shared_task
def clean_expired_codes():
    """
    Очистка истекших кодов подтверждения (старше 1 минуты).
    Запускается автоматически через django-celery-beat.
    """
    try:
        one_min_ago = timezone.now() - timedelta(minutes=1)
        
        users = User.objects.filter(
            confirmation_code__isnull=False,
            confirmation_code_created_at__lt=one_min_ago
        )
        
        count = users.count()
        for user in users:
            user.confirmation_code = None
            # Время создания НЕ ОЧИЩАЕМ!
            user.save(update_fields=['confirmation_code'])
        
        return f"Удалено {count} истекших кодов подтверждения"
    
    except Exception as e:
        return f"Ошибка при очистке кодов: {str(e)}"


@shared_task
def send_confirmation_code_email(user_id):
    """
    Отправляет код подтверждения на email пользователя.
    """
    try:
        print('Отправляет код подтверждения на email пользователя')
        user = User.objects.get(id=user_id)
        print("Генерируем код подтверждения")
        # Генерируем код подтверждения
        code = user.generate_confirmation_code()
        
        # Отправляем email
        subject = 'Подтверждение регистрации'
        message = f'''
        Здравствуйте, {user.username}!
        
        Ваш код подтверждения: {code}
        
        Код действителен в течение 1 минуты.
        
        С уважением,
        Команда 
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return f"Code sent to {user.email}: {code}"
    
    except User.DoesNotExist:
        print('Error User with id ')
        return f"User with id {user_id} not found"
    except Exception as e:
        print('Error Отправляет код ')
        return f"Error sending code: {str(e)}"


@shared_task
def send_resend_confirmation_code_email(user_id):
    """
    Отправляет новый код подтверждения.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Генерируем новый код
        code = user.generate_confirmation_code()
        
        # Отправляем email
        subject = 'Новый код подтверждения'
        message = f'''
        Здравствуйте, {user.username}!
        
        Ваш новый код подтверждения: {code}
        
        Код действителен в течение 1 минуты.
        
        С уважением,
        Команда 
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return f"New code sent to {user.email}: {code}"
    
    except User.DoesNotExist:
        return f"User with id {user_id} not found"
    except Exception as e:
        return f"Error sending code: {str(e)}"
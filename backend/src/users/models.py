# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
import random
from datetime import timedelta
import os


def user_photo_path(instance, filename):
    """Генерация пути для сохранения фото пользователя."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('users', 'photos', str(instance.user.id), filename)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    
    # Код подтверждения
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=6,
        blank=True,
        null=True
    )
    
    # Время создания кода (СОХРАНЯЕТСЯ НАВСЕГДА)
    confirmation_code_created_at = models.DateTimeField(
        verbose_name='Время создания кода',
        blank=True,
        null=True
    )
    
    # Подтвержден ли email
    email_confirmed = models.BooleanField(
        verbose_name='Email подтвержден',
        default=False
    )

    # Аватар (главное фото)
    avatar = models.OneToOneField(
        'UserPhoto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='avatar_of_user',
        verbose_name='Аватар'
    )
    lat = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Широта"
    )
    lon = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Долгота"
    )
    address = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Адрес"
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name() or self.email
    
    def generate_confirmation_code(self):
        """Генерирует новый код подтверждения."""
        # Очищаем старый код
        self.confirmation_code = None
        # Генерируем новый
        self.confirmation_code = str(random.randint(100000, 999999))
        self.confirmation_code_created_at = timezone.now()
        self.save(update_fields=['confirmation_code', 'confirmation_code_created_at'])
        return self.confirmation_code
    
    def is_confirmation_code_valid(self):
        """Проверяет, действителен ли код подтверждения (5 минут)."""
        if not self.confirmation_code or not self.confirmation_code_created_at:
            return False
        
        # Код действителен 5 минут
        expiration_time = self.confirmation_code_created_at + timedelta(minutes=5)
        return timezone.now() <= expiration_time
    
    def get_code_remaining_time(self):
        """Возвращает оставшееся время жизни кода в секундах."""
        if not self.confirmation_code_created_at:
            return 0
        expiration_time = self.confirmation_code_created_at + timedelta(minutes=5)
        remaining = (expiration_time - timezone.now()).total_seconds()
        return max(0, int(remaining))
    
    def verify_confirmation_code(self, code):
        """Проверяет код подтверждения."""
        if self.is_confirmation_code_valid() and self.confirmation_code == code:
            self.email_confirmed = True
            # Удаляем код, НО время создания ОСТАВЛЯЕМ
            self.confirmation_code = None
            # confirmation_code_created_at НЕ ОЧИЩАЕМ!
            self.save(update_fields=['email_confirmed', 'confirmation_code'])
            return True
        return False
    
    def clear_confirmation_code(self):
        """Очищает код подтверждения (время создания остается)."""
        self.confirmation_code = None
        # confirmation_code_created_at НЕ ОЧИЩАЕМ!
        self.save(update_fields=['confirmation_code'])
    
    def delete_expired_code(self):
        """Удаляет истекший код (время создания остается)."""
        if self.confirmation_code and not self.is_confirmation_code_valid():
            self.confirmation_code = None
            # confirmation_code_created_at НЕ ОЧИЩАЕМ!
            self.save(update_fields=['confirmation_code'])
            return True
        return False
    
    def get_code_info(self):
        """Возвращает информацию о коде."""
        if not self.confirmation_code_created_at:
            return None
        
        return {
            'created_at': self.confirmation_code_created_at,
            'has_code': bool(self.confirmation_code),
            'is_valid': self.is_confirmation_code_valid(),
            'remaining_seconds': self.get_code_remaining_time(),
        }


class UserPhoto(models.Model):
    """Модель фото пользователя."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Пользователь'
    )
    image = models.ImageField(
        upload_to=user_photo_path,
        verbose_name='Фото'
    )
    is_avatar = models.BooleanField(
        default=False,
        verbose_name='Главное фото'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Фото пользователя'
        verbose_name_plural = 'Фото пользователей'
        ordering = ('-uploaded_at',)

    def __str__(self):
        return f"Фото {self.user.email} - {self.uploaded_at}"

    def save(self, *args, **kwargs):
        """При сохранении проверяем лимит фото (макс 10)."""
        if not self.pk:  # Только при создании
            photo_count = UserPhoto.objects.filter(user=self.user).count()
            if photo_count >= 10:
                raise ValidationError('Максимум 10 фото на пользователя')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаляем файл при удалении объекта."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class UserOnlineStatus(models.Model):
    """Модель для отслеживания онлайн статуса пользователя."""
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='online_status',
        verbose_name='Пользователь'
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name='В сети'
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name='Последний раз видели'
    )
    last_activity = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Последняя активность'
    )
    
    class Meta:
        verbose_name = 'Статус онлайн'
        verbose_name_plural = 'Статусы онлайн'
        ordering = ('-last_activity',)
    
    def __str__(self):
        return f"{self.user.email} - {'В сети' if self.is_online else 'Не в сети'}"
    
    def update_activity(self):
        """Обновляет время последней активности."""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])
    
    @classmethod
    def get_online_users(cls):
        """Возвращает список пользователей онлайн (активность в течение 5 минут)."""
        threshold = timezone.now() - timedelta(minutes=5)
        return cls.objects.filter(
            is_online=True,
            last_activity__gte=threshold
        ).select_related('user')
    
    @classmethod
    def get_online_users_data(cls):
        """Возвращает список пользователей онлайн с полными данными."""
        online_statuses = cls.get_online_users()
        return [
            {
                'id': str(status.user.id),
                'username': status.user.username,
                'email': status.user.email,
                'first_name': status.user.first_name,
                'last_name': status.user.last_name,
                'avatar_url': status.user.avatar.image.url if status.user.avatar and status.user.avatar.image else None,
                'full_name': status.user.get_full_name()
            }
            for status in online_statuses
        ]


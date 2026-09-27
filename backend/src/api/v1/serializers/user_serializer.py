# api/v1/serializers/user_serializer.py
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.utils import timezone
from users.models import UserPhoto
from datetime import timedelta
from users.tasks import send_resend_confirmation_code_email


User = get_user_model()

# ============= БАЗОВЫЙ СЕРИАЛИЗАТОР ДЛЯ ФОТО =============

class UserPhotoBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для фото."""
    
    class Meta:
        model = UserPhoto
        fields = ('id', 'image', 'is_avatar', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class UserPhotoSerializer(UserPhotoBaseSerializer):
    """Сериализатор для отображения фото."""
    
    class Meta(UserPhotoBaseSerializer.Meta):
        fields = UserPhotoBaseSerializer.Meta.fields
        read_only_fields = UserPhotoBaseSerializer.Meta.read_only_fields + ('image',)


class UserPhotoCreateSerializer(serializers.ModelSerializer):
    """СЕРИАЛИЗАТОР ДЛЯ СОЗДАНИЯ ФОТО - УБИРАЕМ create() МЕТОД"""
    
    class Meta:
        model = UserPhoto
        fields = ('image',)
        # Добавляем user как read_only, чтобы он не передавался в validated_data
        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserPhotoUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления фото."""
    
    class Meta:
        model = UserPhoto
        fields = ('is_avatar',)
    
    def update(self, instance, validated_data):
        """Обновление фото с автоматической обработкой аватара."""
        if validated_data.get('is_avatar', False):
            # Убираем флаг с других фото пользователя
            UserPhoto.objects.filter(
                user=instance.user, 
                is_avatar=True
            ).exclude(id=instance.id).update(is_avatar=False)
            
            # Устанавливаем аватар пользователя
            user = instance.user
            user.avatar = instance
            user.save()
        
        instance.is_avatar = validated_data.get('is_avatar', instance.is_avatar)
        instance.save()
        return instance


# ============= СЕРИАЛИЗАТОРЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ =============

class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')
    
    def create(self, validated_data):
        user = super().create(validated_data)
        return user


class CustomUserSerializer(UserSerializer):
    """Сериализатор для отображения пользователя."""
    photos = UserPhotoSerializer(many=True, read_only=True, source='photos.all')
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'email_confirmed',
            'avatar_url',
            'photos',
        )
        read_only_fields = ('id', 'email', 'email_confirmed',)

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and obj.avatar.image:
            return request.build_absolute_uri(obj.avatar.image.url) if request else obj.avatar.image.url
        return None


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления данных пользователя."""
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
    
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


# ============= СЕРИАЛИЗАТОРЫ ДЛЯ ПОДТВЕРЖДЕНИЯ EMAIL =============

class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        
        if user.email_confirmed:
            raise serializers.ValidationError('Email уже подтвержден')
        
        if not user.verify_confirmation_code(data['code']):
            raise serializers.ValidationError('Неверный или устаревший код подтверждения')
        
        return data


class ResendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        
        if user.email_confirmed:
            raise serializers.ValidationError('Email уже подтвержден')
        
        if user.confirmation_code_created_at:
            time_since_last_code = timezone.now() - user.confirmation_code_created_at
            if time_since_last_code < timedelta(minutes=1):
                raise serializers.ValidationError(
                    'Новый код можно запросить через минуту'
                )
        
        return data
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        send_resend_confirmation_code_email.delay(str(user.id))


# ============= СЕРИАЛИЗАТОР ДЛЯ ОНЛАЙН ПОЛЬЗОВАТЕЛЕЙ =============

class OnlineUserSerializer(serializers.Serializer):
    """
    Сериализатор для отображения информации об онлайн пользователе.
    """
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        """Получение полного имени пользователя."""
        first = obj.get('first_name', '')
        last = obj.get('last_name', '')
        return f"{first} {last}".strip() or obj.get('username', '')
    
    def get_avatar_url(self, obj):
        """Получение URL аватара."""
        return obj.get('avatar_url', None)
    


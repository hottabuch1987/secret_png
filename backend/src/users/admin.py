# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import CustomUser, UserPhoto, UserOnlineStatus

@admin.register(UserOnlineStatus)
class UserOnlineStatusAdmin(admin.ModelAdmin):
    list_display = (
        'is_online',
        'last_seen',
        'last_activity',
        
    )
    
    # Поля по которым можно фильтровать
    list_filter = (
        'user',
        'is_online',
        'last_seen',
        'last_activity',
    )
    
    # Поля для поиска
    search_fields = (
        'is_online',
    )
    
    # Поля для сортировки
    ordering = ('-last_seen',)
        
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Поля для отображения в списке
    list_display = (
        'id', 
        'username', 
        'email', 
        'first_name', 
        'last_name',
        'email_confirmed',
        'avatar_preview',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
        'lat',
        'lon',
        'address',
    )
    
    # Поля по которым можно фильтровать
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'email_confirmed',
        'date_joined',
        'last_login'
    )
    
    # Поля для поиска
    search_fields = (
        'username', 
        'email', 
        'first_name', 
        'last_name',
        'id'
    )
    
    # Поля для сортировки
    ordering = ('-date_joined',)
    
    # Количество записей на странице
    list_per_page = 25
    
    # Поля, которые можно редактировать прямо в списке
    list_editable = (
        'is_active',
        'is_staff',
        'email_confirmed',
    )
    
    # Поля, которые отображаются как ссылки
    list_display_links = ('id', 'username', 'email')
    
    # Группировка полей в форме редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'email',
                'avatar',
                'lat',
                'lon',
                'address',
            )
        }),
        (_('Email confirmation'), {
            'fields': (
                'email_confirmed',
                'confirmation_code',
                'confirmation_code_created_at',
            ),
            'classes': ('collapse',),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions',
               
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'password1', 
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
                'lat',
                'lon',
                'address',
                
            ),
        }),
    )
    
    # Действия в админке
    actions = [
        'make_active', 
        'make_inactive', 
        'make_staff', 
        'make_superuser',
        'confirm_emails',
        'unconfirm_emails',
        'clear_avatars'
    ]
    
    def avatar_preview(self, obj):
        """Превью аватара в списке"""
        if obj.avatar and obj.avatar.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.image.url
            )
        return format_html(
            '<span style="color: #999;">Нет аватара</span>'
        )
    avatar_preview.short_description = 'Аватар'
    avatar_preview.allow_tags = True
    
    def make_active(self, request, queryset):
        """Активировать выбранных пользователей"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} пользователей активировано.')
    make_active.short_description = 'Активировать выбранных пользователей'
    
    def make_inactive(self, request, queryset):
        """Деактивировать выбранных пользователей"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} пользователей деактивировано.')
    make_inactive.short_description = 'Деактивировать выбранных пользователей'
    
    def make_staff(self, request, queryset):
        """Сделать выбранных пользователей персоналом"""
        count = queryset.update(is_staff=True)
        self.message_user(request, f'{count} пользователей сделаны персоналом.')
    make_staff.short_description = 'Сделать персоналом'
    
    def make_superuser(self, request, queryset):
        """Сделать выбранных пользователей суперпользователями"""
        count = queryset.update(is_superuser=True, is_staff=True)
        self.message_user(request, f'{count} пользователей сделаны суперпользователями.')
    make_superuser.short_description = 'Сделать суперпользователями'
    
    def confirm_emails(self, request, queryset):
        """Подтвердить email выбранных пользователей"""
        count = queryset.update(email_confirmed=True)
        self.message_user(request, f'{count} пользователей подтвердили email.')
    confirm_emails.short_description = 'Подтвердить email'
    
    def unconfirm_emails(self, request, queryset):
        """Отменить подтверждение email выбранных пользователей"""
        count = queryset.update(email_confirmed=False)
        self.message_user(request, f'{count} пользователей отменили подтверждение email.')
    unconfirm_emails.short_description = 'Отменить подтверждение email'
    
    def clear_avatars(self, request, queryset):
        """Очистить аватары выбранных пользователей"""
        for user in queryset:
            if user.avatar:
                user.avatar = None
                user.save()
        count = queryset.count()
        self.message_user(request, f'{count} пользователей очистили аватар.')
    clear_avatars.short_description = 'Очистить аватар'
    
    def get_queryset(self, request):
        """Оптимизация запросов к БД"""
        return super().get_queryset(request).select_related('avatar')
    
    def get_readonly_fields(self, request, obj=None):
        """Поля только для чтения"""
        if obj:  # При редактировании
            return ('last_login', 'date_joined', 'confirmation_code', 'confirmation_code_created_at')
        return ()  # При создании
    
    def save_model(self, request, obj, form, change):
        """Дополнительные действия при сохранении"""
        if not change:  # При создании нового пользователя
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)


@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    # Поля для отображения в списке
    list_display = (
        'id',
        'user_link',
        'image_preview',
        'is_avatar',
        'uploaded_at',
        'updated_at',
    )
    
    # Поля по которым можно фильтровать
    list_filter = (
        'is_avatar',
        'uploaded_at',
        'updated_at',
        'user',
    )
    
    # Поля для поиска
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'id',
    )
    
    # Поля для сортировки
    ordering = ('-uploaded_at',)
    
    # Количество записей на странице
    list_per_page = 25
    
    # Поля, которые можно редактировать прямо в списке
    list_editable = ('is_avatar',)
    
    # Поля, которые отображаются как ссылки
    list_display_links = ('id', 'user_link')
    
    # Поля только для чтения
    readonly_fields = (
        'id',
        'uploaded_at',
        'updated_at',
        'image_preview_large',
        'full_user_info',
    )
    
    # Группировка полей в форме редактирования
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'image',
                'is_avatar',
                'image_preview_large',
            )
        }),
        ('Дополнительная информация', {
            'fields': (
                'id',
                'uploaded_at',
                'updated_at',
                'full_user_info',
            ),
            'classes': ('collapse',),
        }),
    )
    
    # Действия в админке
    actions = [
        'set_as_avatar',
        'remove_from_avatar',
        'delete_selected_photos',
    ]
    
    def user_link(self, obj):
        """Ссылка на пользователя"""
        if obj.user:
            return format_html(
                '<a href="/admin/users/customuser/{}/change/">{}</a>',
                obj.user.id,
                obj.user.email
            )
        return '—'
    user_link.short_description = 'Пользователь'
    user_link.allow_tags = True
    
    def image_preview(self, obj):
        """Превью фото в списке"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return 'Нет фото'
    image_preview.short_description = 'Фото'
    image_preview.allow_tags = True
    
    def image_preview_large(self, obj):
        """Большое превью фото в форме"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px;" />',
                obj.image.url
            )
        return 'Нет фото'
    image_preview_large.short_description = 'Превью фото'
    image_preview_large.allow_tags = True
    
    def full_user_info(self, obj):
        """Полная информация о пользователе"""
        if obj.user:
            return format_html(
                '''
                <div style="background: #f8f9fa; padding: 10px; border-radius: 4px;">
                    <strong>Email:</strong> {}<br/>
                    <strong>Имя:</strong> {}<br/>
                    <strong>Фамилия:</strong> {}<br/>
                    <strong>Username:</strong> {}<br/>
                    <strong>Активен:</strong> {}<br/>
                    <strong>Подтвержден:</strong> {}
                </div>
                ''',
                obj.user.email,
                obj.user.first_name or '—',
                obj.user.last_name or '—',
                obj.user.username,
                '✅' if obj.user.is_active else '❌',
                '✅' if obj.user.email_confirmed else '❌'
            )
        return 'Пользователь удален'
    full_user_info.short_description = 'Информация о пользователе'
    full_user_info.allow_tags = True
    
    def set_as_avatar(self, request, queryset):
        """Сделать выбранные фото аватарами"""
        count = 0
        for photo in queryset:
            # Убираем флаг с других фото пользователя
            UserPhoto.objects.filter(user=photo.user, is_avatar=True).update(is_avatar=False)
            # Устанавливаем новое фото как аватар
            photo.is_avatar = True
            photo.save()
            # Обновляем пользователя
            user = photo.user
            user.avatar = photo
            user.save()
            count += 1
        self.message_user(request, f'{count} фото установлены как аватары.')
    set_as_avatar.short_description = 'Сделать аватаром'
    
    def remove_from_avatar(self, request, queryset):
        """Убрать статус аватара с выбранных фото"""
        count = queryset.update(is_avatar=False)
        # Очищаем аватары у пользователей
        for photo in queryset:
            user = photo.user
            if user.avatar == photo:
                user.avatar = None
                user.save()
        self.message_user(request, f'{count} фото убраны из аватаров.')
    remove_from_avatar.short_description = 'Убрать из аватаров'
    
    def delete_selected_photos(self, request, queryset):
        """Удалить выбранные фото"""
        count = queryset.count()
        for photo in queryset:
            photo.delete()  # Вызовет удаление файла
        self.message_user(request, f'{count} фото удалены.')
    delete_selected_photos.short_description = 'Удалить выбранные фото'
    
    def save_model(self, request, obj, form, change):
        """Дополнительные действия при сохранении"""
        # Если фото становится аватаром, убираем флаг с других фото
        if obj.is_avatar:
            UserPhoto.objects.filter(user=obj.user, is_avatar=True).exclude(id=obj.id).update(is_avatar=False)
            # Обновляем пользователя
            user = obj.user
            user.avatar = obj
            user.save()
        else:
            # Если снимаем флаг аватара
            user = obj.user
            if user.avatar == obj:
                user.avatar = None
                user.save()
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Удаление модели с дополнительными проверками"""
        # Если удаляем аватар, сбрасываем у пользователя
        if obj.is_avatar:
            user = obj.user
            user.avatar = None
            user.save()
        obj.delete()
    
    def get_queryset(self, request):
        """Оптимизация запросов к БД"""
        return super().get_queryset(request).select_related('user')
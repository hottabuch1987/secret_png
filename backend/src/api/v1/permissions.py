from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class ReadOnlyOrIsAdmin(BasePermission):
    """"""
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение на просмотр/изменение.
    Администраторы могут просматривать/изменять все бронирования.
    """
    def has_permission(self, request, view):
        # Проверяем базовую аутентификацию
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Администраторы имеют доступ ко всем объектам
        if request.user.is_staff:
            return True
        return obj.user == request.user


class CanManageBookings(permissions.BasePermission):
    """
    Доступно только администраторам и менеджерам (если есть группа менеджеров).
    """
    def has_permission(self, request, view):
        # Проверяем аутентификацию
        if not request.user.is_authenticated:
            return False
        
        # Администраторы имеют полный доступ
        if request.user.is_staff:
            return True     
        return False

    def has_object_permission(self, request, view, obj):
        # Те же правила применяются к конкретному объекту
        return self.has_permission(request, view)
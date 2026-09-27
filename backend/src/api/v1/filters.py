import django_filters
from django.utils import timezone


class UserFilter(django_filters.FilterSet):
    """Фильтры для пользователей"""
    
# users/management/commands/clean_codes.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Удаляет коды подтверждения старше 1 минут'

    def handle(self, *args, **options):
        one_min_ago = timezone.now() - timedelta(minutes=1)
        
        users = CustomUser.objects.filter(
            confirmation_code__isnull=False,
            confirmation_code_created_at__lt=one_min_ago
        )
        
        count = users.count()
        for user in users:
            user.confirmation_code = None
            user.save(update_fields=['confirmation_code'])
        
        self.stdout.write(
            self.style.SUCCESS(f'Удалено {count} истекших кодов')
        )
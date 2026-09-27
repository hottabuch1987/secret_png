#!/bin/sh

set -e

# Меняем владельца статических и медиа-томов на appuser
chown -R appuser:appuser /usr/src/app/static /usr/src/app/media

# Выполняем миграции и collectstatic от appuser
su-exec appuser python manage.py migrate
su-exec appuser python manage.py collectstatic --noinput

# Запускаем Gunicorn от appuser
# exec su-exec appuser gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
exec su-exec appuser daphne -u /tmp/daphne.sock config.asgi:application --bind 0.0.0.0 --port 8000
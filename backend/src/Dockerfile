FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости (включая su-exec)
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    postgresql-dev \
    python3-dev \
    su-exec

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /usr/src/app/db /usr/src/app/logs

# Создаём пользователя (без переключения на него)
RUN adduser -D -u 1000 appuser

# Копируем entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
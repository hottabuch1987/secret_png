FROM python:3.12-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости для Debian
# Компилируем su-exec для Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && curl -fsSL -o /usr/local/bin/su-exec.c \
       https://raw.githubusercontent.com/ncopa/su-exec/master/su-exec.c \
    && gcc -Wall -o /usr/local/bin/su-exec /usr/local/bin/su-exec.c \
    && chmod +x /usr/local/bin/su-exec \
    && rm /usr/local/bin/su-exec.c \
    && apt-get purge -y build-essential curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /usr/src/app/db /usr/src/app/logs

# Создаём пользователя
RUN useradd -m -u 1000 appuser

# Копируем entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
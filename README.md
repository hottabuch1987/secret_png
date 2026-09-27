[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=quick+start )](https://git.io/typing-svg)

## Документация по развертыванию  проекта для скрытия текста в картинку png
## Стек: DRF + Celery + Redis + PostgreSQL + Docker + WebSocket + Nuxt

### C помощью docker

1. Клонируйте репозиторий

2. Создайте файл `.env` в корневой директории проекта 
    ```
    # ===== DJANGO НАСТРОЙКИ =====
    DEBUG=0
    ALLOWED_HOSTS=localhost
    SECRET_KEY=django-insecure-6s+g7%cdw%g#)n)_380$sz-l$0laa)c)jr2vtdb17&l)fg16s7
    IN_DOCKER=true

    # ===== БАЗА ДАННЫХ =====
    POSTGRES_DB=db_87
    POSTGRES_USER=user_87
    POSTGRES_PASSWORD=youpassword
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    # ===== CELERY НАСТРОЙКИ =====
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    # ===== EMAIL НАСТРОЙКИ =====
    MAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT = 587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=youemail@gmail.com
    EMAIL_HOST_PASSWORD=youpassword
    # ===== FRONTEND НАСТРОЙКИ =====
    NUXT_PUBLIC_API_BASE=http://localhost/api/v1
    ```

3. Соберите и запустите контейнеры:
   ```
   docker-compose build
   ```
   ```
   docker-compose up
   ```
4. Создайте суперпользователя для доступа к админпанели
   ```
   docker-compose exec app sh
   ```
   ```
   python manage.py createsuperuser
   ```
### После успешного запуска, приложение будет доступно по адресу:
   - Nginx: http://localhost
   - API: http://localhost/api/v1/
   - Swagger: http://localhost/api/v1/swagger/
   - Redoc: http://localhost/api/v1/redoc/
   
### развертывание бекенда локально для разработки 

1. Клонируйте репозиторий

2. Перейдите в дирректорию  backend/src  и создайте и активируйте виртальное окружение
    ```
    cd backend/src
    ```
    ```
    python3 -m venv venv
    ```
    ```
    source venv/bin/activate
    ```
3.  Установите зависимости
    ```
    pip install -r requirements.txt
    ```
4. Сделайте миграции для sqlite
    ```
    python manage.py  makemigrations
    ```
    ```
    python manage.py  migrate
    ```
5. Запустите сервер
    ```
    python manage.py runserver
    ```
6. Запустите redis
    ```
    redis-server
    ```
7. В директории src  запустите celery
    ```
    celery -A celery_app worker -l INFO
    ```
8. В директории src  запустите flower
    ```
    celery -A celery_app flower --port=5555
    ```
### После успешного запуска, приложение будет доступно по адресу:
   - Django: http://localhost:8000


### развертывание фронтенд локально для разработки
1. Перейдите в дирректорию  frontend/src  и создайте и активируйте виртальное окружение
    ```
    cd frontend/src
    ``` 
1. Установите зависимости и запустите сервер:
   ```
   npm install
   ```
   ```
   npm run dev
   ```
### После успешного запуска, приложение будет доступно по адресу:
   - Nuxt: http://localhost:3000


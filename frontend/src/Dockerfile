# Этап сборки
FROM node:20-alpine AS builder

WORKDIR /app

# Копируем файлы зависимостей
COPY package*.json ./
RUN npm ci

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Финальный образ
FROM node:20-alpine

WORKDIR /app

# Копируем собранный вывод и production-зависимости
COPY --from=builder /app/.output /app/.output
COPY package*.json ./
RUN npm ci --production

# Порт Nuxt
EXPOSE 3000

# Запуск сервера
CMD ["node", ".output/server/index.mjs"]
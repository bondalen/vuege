# Многоэтапная сборка для оптимизации размера
FROM openjdk:21-slim

# Установка Redis
RUN apt-get update && apt-get install -y \
    redis-server \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователей
RUN addgroup --system app && adduser --system --ingroup app app

# Создание директорий
RUN mkdir -p /app /var/lib/redis

# Копирование JAR файла
COPY target/vuege-0.1.0.jar /app/app.jar

# Копирование скриптов инициализации
COPY scripts/start-services.sh /app/
COPY scripts/init-db.sql /app/

# Установка прав
RUN chmod +x /app/start-services.sh && \
    chown -R app:app /app /var/lib/redis

# Переключение на пользователя app
USER app

# Порт приложения
EXPOSE 8082

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8082/api/actuator/health || exit 1

# Запуск всех сервисов
CMD ["/app/start-services.sh"]
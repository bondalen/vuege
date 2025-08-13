#!/bin/bash

CONTAINER_NAME="postgres-java-universal"
IMAGE_NAME="postgres-java-universal"

echo "=== Управление универсальным контейнером PostgreSQL + Java ==="
echo

case "$1" in
    "build")
        echo "Сборка образа..."
        docker build -f docker/Dockerfile.postgres-java -t $IMAGE_NAME .
        ;;
    "start")
        echo "Запуск контейнера..."
        docker run -d \
            --name $CONTAINER_NAME \
            -p 5432:5432 \
            -e POSTGRES_DB=testdb \
            -e POSTGRES_USER=testuser \
            -e POSTGRES_PASSWORD=testpass \
            -v postgres_data:/var/lib/postgresql/16/main \
            $IMAGE_NAME
        ;;
    "stop")
        echo "Остановка контейнера..."
        docker stop $CONTAINER_NAME
        ;;
    "restart")
        echo "Перезапуск контейнера..."
        docker restart $CONTAINER_NAME
        ;;
    "status")
        echo "Статус контейнера:"
        docker ps -a | grep $CONTAINER_NAME
        ;;
    "logs")
        echo "Логи контейнера:"
        docker logs $CONTAINER_NAME
        ;;
    "exec")
        echo "Подключение к контейнеру..."
        docker exec -it $CONTAINER_NAME bash
        ;;
    "java")
        echo "Проверка Java в контейнере:"
        docker exec $CONTAINER_NAME java -version
        ;;
    "postgres")
        echo "Проверка PostgreSQL в контейнере:"
        docker exec $CONTAINER_NAME service postgresql status
        ;;
    "setup-db")
        echo "Настройка базы данных..."
        docker exec $CONTAINER_NAME service postgresql start
        docker exec -it $CONTAINER_NAME su postgres -c "psql -c \"CREATE USER testuser WITH PASSWORD 'testpass';\""
        docker exec -it $CONTAINER_NAME su postgres -c "psql -c \"CREATE DATABASE testdb OWNER testuser;\""
        docker exec -it $CONTAINER_NAME su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;\""
        echo "База данных настроена!"
        ;;
    "cleanup")
        echo "Очистка контейнера и образа..."
        docker stop $CONTAINER_NAME 2>/dev/null
        docker rm $CONTAINER_NAME 2>/dev/null
        docker rmi $IMAGE_NAME 2>/dev/null
        echo "Очистка завершена!"
        ;;
    *)
        echo "Использование: $0 {build|start|stop|restart|status|logs|exec|java|postgres|setup-db|cleanup}"
        echo
        echo "Команды:"
        echo "  build     - Собрать образ"
        echo "  start     - Запустить контейнер"
        echo "  stop      - Остановить контейнер"
        echo "  restart   - Перезапустить контейнер"
        echo "  status    - Показать статус"
        echo "  logs      - Показать логи"
        echo "  exec      - Подключиться к контейнеру"
        echo "  java      - Проверить Java"
        echo "  postgres  - Проверить PostgreSQL"
        echo "  setup-db  - Настроить базу данных"
        echo "  cleanup   - Очистить контейнер и образ"
        ;;
esac


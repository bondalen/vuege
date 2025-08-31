#!/bin/bash

# Скрипт для подключения к SQL Server 2022 Express
# Использование: ./scripts/mssql-connect.sh [команда]

SQLCMD="/opt/mssql-tools18/bin/sqlcmd"
SERVER="localhost"
USER="sa"
PASSWORD="Vuege2024!"
CONTAINER="vuege-mssql"

# Проверка статуса контейнера
check_container() {
    if ! docker ps | grep -q "$CONTAINER"; then
        echo "❌ Контейнер $CONTAINER не запущен!"
        echo "Запустите: docker-compose -f docker-compose-mssql.yml up -d"
        exit 1
    fi
}

# Выполнение SQL команды
execute_sql() {
    local query="$1"
    docker exec "$CONTAINER" "$SQLCMD" -S "$SERVER" -U "$USER" -P "$PASSWORD" -C -Q "$query"
}

# Интерактивный режим
interactive_mode() {
    echo "🔗 Подключение к SQL Server 2022 Express..."
    echo "Сервер: $SERVER"
    echo "Пользователь: $USER"
    echo "Контейнер: $CONTAINER"
    echo "Для выхода введите: exit"
    echo "----------------------------------------"
    
    docker exec -it "$CONTAINER" "$SQLCMD" -S "$SERVER" -U "$USER" -P "$PASSWORD" -C
}

# Основная логика
main() {
    check_container
    
    if [ $# -eq 0 ]; then
        # Интерактивный режим
        interactive_mode
    else
        # Выполнение команды
        execute_sql "$*"
    fi
}

main "$@"
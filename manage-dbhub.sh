#!/bin/bash

# Скрипт для управления MCP сервером DBHub
# Автор: Александр
# Дата: 2025-08-21

DBHUB_DIR="/home/alex/vuege/dbhub"
DSN="postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable"
PORT=8081
PID_FILE="/tmp/dbhub.pid"
LOG_FILE="$DBHUB_DIR/dbhub.log"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== DBHub MCP Server Manager ===${NC}"
}

# Проверка существования директории
check_directory() {
    if [ ! -d "$DBHUB_DIR" ]; then
        print_error "Директория $DBHUB_DIR не найдена!"
        exit 1
    fi
}

# Проверка существования исполняемого файла
check_executable() {
    if [ ! -f "$DBHUB_DIR/dist/index.js" ]; then
        print_error "Исполняемый файл $DBHUB_DIR/dist/index.js не найден!"
        print_warning "Выполните: npm run build"
        exit 1
    fi
}

# Проверка статуса сервера
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            print_status "DBHub сервер запущен (PID: $PID)"
            return 0
        else
            print_warning "PID файл найден, но процесс не запущен"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        print_status "DBHub сервер не запущен"
        return 1
    fi
}

# Запуск сервера
start_server() {
    print_header
    check_directory
    check_executable
    
    if check_status; then
        print_warning "Сервер уже запущен!"
        return 1
    fi
    
    print_status "Запуск DBHub MCP сервера..."
    print_status "DSN: $DSN"
    print_status "Порт: $PORT"
    print_status "Лог файл: $LOG_FILE"
    
    cd "$DBHUB_DIR"
    nohup node dist/index.js \
        --transport http \
        --port $PORT \
        --dsn "$DSN" \
        > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo $PID > "$PID_FILE"
    
    sleep 2
    
    if check_status; then
        print_status "✅ Сервер успешно запущен!"
        print_status "🌐 HTTP API: http://localhost:$PORT/message"
        print_status "📝 Логи: $LOG_FILE"
    else
        print_error "❌ Ошибка запуска сервера!"
        print_status "Проверьте логи: $LOG_FILE"
        return 1
    fi
}

# Остановка сервера
stop_server() {
    print_header
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        print_status "Остановка сервера (PID: $PID)..."
        
        if kill $PID 2>/dev/null; then
            print_status "✅ Сервер остановлен"
        else
            print_warning "Процесс уже завершен"
        fi
        
        rm -f "$PID_FILE"
    else
        print_warning "PID файл не найден"
    fi
}

# Перезапуск сервера
restart_server() {
    print_header
    stop_server
    sleep 2
    start_server
}

# Просмотр логов
show_logs() {
    print_header
    if [ -f "$LOG_FILE" ]; then
        print_status "Последние 50 строк логов:"
        echo "----------------------------------------"
        tail -n 50 "$LOG_FILE"
        echo "----------------------------------------"
    else
        print_error "Лог файл не найден: $LOG_FILE"
    fi
}

# Тестирование API
test_api() {
    print_header
    print_status "Тестирование API..."
    
    if ! check_status; then
        print_error "Сервер не запущен! Запустите: $0 start"
        return 1
    fi
    
    # Тест 1: Запрос пользователей
    print_status "Тест 1: Запрос пользователей"
    curl -s -X POST http://localhost:$PORT/message \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d '{
            "jsonrpc":"2.0",
            "id":1,
            "method":"tools/call",
            "params":{
                "name":"execute_sql",
                "arguments":{
                    "sql":"SELECT COUNT(*) as user_count FROM users;"
                }
            }
        }' | jq -r '.result.content[0].text' | jq .
    
    echo ""
    
    # Тест 2: Запрос продуктов
    print_status "Тест 2: Запрос продуктов"
    curl -s -X POST http://localhost:$PORT/message \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d '{
            "jsonrpc":"2.0",
            "id":2,
            "method":"tools/call",
            "params":{
                "name":"execute_sql",
                "arguments":{
                    "sql":"SELECT COUNT(*) as product_count FROM products;"
                }
            }
        }' | jq -r '.result.content[0].text' | jq .
    
    print_status "✅ Тестирование завершено"
}

# Показать справку
show_help() {
    print_header
    echo "Использование: $0 {start|stop|restart|status|logs|test|help}"
    echo ""
    echo "Команды:"
    echo "  start   - Запустить DBHub MCP сервер"
    echo "  stop    - Остановить сервер"
    echo "  restart - Перезапустить сервер"
    echo "  status  - Показать статус сервера"
    echo "  logs    - Показать логи сервера"
    echo "  test    - Протестировать API"
    echo "  help    - Показать эту справку"
    echo ""
    echo "Конфигурация:"
    echo "  DSN: $DSN"
    echo "  Порт: $PORT"
    echo "  Логи: $LOG_FILE"
}

# Основная логика
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        print_header
        check_status
        ;;
    logs)
        show_logs
        ;;
    test)
        test_api
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Неизвестная команда: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

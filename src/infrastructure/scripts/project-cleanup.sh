#!/bin/bash

# =============================================================================
# СКРИПТ ОЧИСТКИ ПРОЕКТА VUEGE
# Решение проблемы "раздувания" папки проекта
# =============================================================================

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция логирования
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Функция получения размера директории в человекочитаемом формате
get_dir_size() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sh "$dir" 2>/dev/null | cut -f1
    else
        echo "0B"
    fi
}

# Функция получения количества файлов в директории
get_file_count() {
    local dir="$1"
    if [ -d "$dir" ]; then
        find "$dir" -type f 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# Функция диагностики проекта
diagnose_project() {
    log "🔍 ДИАГНОСТИКА ПРОЕКТА VUEGE"
    echo "=================================="
    
    # Общий размер проекта
    local total_size=$(du -sh . 2>/dev/null | cut -f1)
    log "Общий размер проекта: $total_size"
    
    # Размер основных директорий
    echo ""
    log "📊 РАЗМЕРЫ ОСНОВНЫХ ДИРЕКТОРИЙ:"
    
    local dirs=(
        "venv"
        "src/app/frontend/node_modules"
        "src/app/target"
        "mcp_cache"
        "~"
        "src/app/frontend/dist"
        ".git"
        ".vscode"
        ".cursor"
    )
    
    for dir in "${dirs[@]}"; do
        local size=$(get_dir_size "$dir")
        local count=$(get_file_count "$dir")
        printf "%-30s %8s (%6s файлов)\n" "$dir" "$size" "$count"
    done
    
    # Проверка .gitignore
    echo ""
    log "📋 ПРОВЕРКА .GITIGNORE:"
    if [ -f ".gitignore" ]; then
        local ignored_dirs=("venv" "node_modules" "target" "mcp_cache" ".vscode" ".cursor")
        for dir in "${ignored_dirs[@]}"; do
            if grep -q "^$dir/" .gitignore || grep -q "^$dir$" .gitignore; then
                log_success "$dir/ в .gitignore"
            else
                log_warning "$dir/ НЕ в .gitignore"
            fi
        done
    else
        log_error ".gitignore не найден!"
    fi
    
    # Проверка Git статуса
    echo ""
    log "🔍 ПРОВЕРКА GIT СТАТУСА:"
    if [ -d ".git" ]; then
        local git_size=$(get_dir_size ".git")
        local git_files=$(get_file_count ".git")
        log "Размер .git: $git_size ($git_files файлов)"
        
        # Количество файлов для коммита
        local staged_files=$(git status --porcelain 2>/dev/null | wc -l)
        log "Файлов для коммита: $staged_files"
    else
        log_warning "Git репозиторий не инициализирован"
    fi
}

# Функция безопасной очистки
safe_cleanup() {
    log "🧹 БЕЗОПАСНАЯ ОЧИСТКА ПРОЕКТА"
    echo "=================================="
    
    # Создание резервной копии
    local backup_dir="backup-$(date +%Y%m%d-%H%M%S)"
    log "Создание резервной копии в $backup_dir..."
    mkdir -p "$backup_dir"
    
    # Безопасные директории для удаления (с резервным копированием)
    local safe_dirs=(
        "src/app/frontend/node_modules"
        "src/app/target"
        "mcp_cache"
        "src/app/frontend/dist"
        ".vscode"
    )
    
    for dir in "${safe_dirs[@]}"; do
        if [ -d "$dir" ]; then
            local size=$(get_dir_size "$dir")
            log "Очистка $dir ($size)..."
            
            # Создание резервной копии
            mkdir -p "$backup_dir/$(dirname "$dir")"
            cp -r "$dir" "$backup_dir/$(dirname "$dir")/" 2>/dev/null || true
            
            # Удаление директории
            rm -rf "$dir"
            log_success "Удален $dir"
        fi
    done
    
    # Очистка Python кэша
    log "Очистка Python кэша..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "*.pyo" -delete 2>/dev/null || true
    log_success "Python кэш очищен"
    
    # Очистка временных файлов
    log "Очистка временных файлов..."
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.temp" -delete 2>/dev/null || true
    find . -name "*.log" -delete 2>/dev/null || true
    log_success "Временные файлы очищены"
    
    log_success "Безопасная очистка завершена. Резервная копия в $backup_dir"
}

# Функция критической очистки (только в крайнем случае)
critical_cleanup() {
    log "🚨 КРИТИЧЕСКАЯ ОЧИСТКА ПРОЕКТА"
    echo "=================================="
    log_warning "ВНИМАНИЕ: Эта операция удалит ВСЕ временные файлы!"
    log_warning "Включая node_modules, target, и другие директории сборки"
    
    read -p "Продолжить? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Операция отменена"
        return
    fi
    
    # Создание полной резервной копии
    local backup_dir="critical-backup-$(date +%Y%m%d-%H%M%S)"
    log "Создание полной резервной копии в $backup_dir..."
    mkdir -p "$backup_dir"
    
    # Критические директории для удаления
    local critical_dirs=(
        "src/app/frontend/node_modules"
        "src/app/target"
        "mcp_cache"
        "src/app/frontend/dist"
        ".vscode"
        "~"
    )
    
    for dir in "${critical_dirs[@]}"; do
        if [ -d "$dir" ]; then
            local size=$(get_dir_size "$dir")
            log "Критическая очистка $dir ($size)..."
            
            # Резервное копирование
            mkdir -p "$backup_dir/$(dirname "$dir")"
            cp -r "$dir" "$backup_dir/$(dirname "$dir")/" 2>/dev/null || true
            
            # Удаление
            rm -rf "$dir"
            log_success "Удален $dir"
        fi
    done
    
    # Очистка всех кэшей
    log "Очистка всех кэшей..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "*.pyo" -delete 2>/dev/null || true
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.temp" -delete 2>/dev/null || true
    find . -name "*.log" -delete 2>/dev/null || true
    
    log_success "Критическая очистка завершена. Резервная копия в $backup_dir"
}

# Функция обновления .gitignore
update_gitignore() {
    log "📝 ОБНОВЛЕНИЕ .GITIGNORE"
    echo "=================================="
    
    if [ ! -f ".gitignore" ]; then
        log "Создание нового .gitignore..."
        touch .gitignore
    fi
    
    # Добавление критических исключений
    local critical_exclusions=(
        "# Virtual Environment"
        "venv/"
        "env/"
        ".venv/"
        "ENV/"
        ""
        "# Node.js"
        "node_modules/"
        "npm-debug.log*"
        "yarn-debug.log*"
        "yarn-error.log*"
        ""
        "# Maven"
        "target/"
        "*.class"
        "*.jar"
        "*.war"
        "*.ear"
        ""
        "# MCP Cache"
        "mcp_cache/"
        ".mcp_cache/"
        ""
        "# IDE"
        ".vscode/"
        ".idea/"
        ""
        "# Build directories"
        "dist/"
        "build/"
        ""
        "# Temporary files"
        "*.tmp"
        "*.temp"
        "*.log"
        ""
        "# OS"
        ".DS_Store"
        "Thumbs.db"
        ""
        "# Cursor IDE"
        ".cursor/"
        ".cursorrules-*"
        ""
        "# Backup directories"
        "backup-*/"
        "critical-backup-*/"
        ""
        "# Large files"
        "*.mp3"
        "*.mp4"
        "*.zip"
        "*.tar.gz"
    )
    
    for exclusion in "${critical_exclusions[@]}"; do
        if [ "$exclusion" = "" ]; then
            echo "" >> .gitignore
        elif ! grep -q "^${exclusion}$" .gitignore 2>/dev/null; then
            echo "$exclusion" >> .gitignore
            log_success "Добавлено в .gitignore: $exclusion"
        fi
    done
    
    log_success ".gitignore обновлен"
}

# Функция создания системы мониторинга
create_monitoring() {
    log "📊 СОЗДАНИЕ СИСТЕМЫ МОНИТОРИНГА"
    echo "=================================="
    
    # Создание скрипта мониторинга
    cat > "project-monitor.sh" << 'EOF'
#!/bin/bash

# Мониторинг размера проекта Vuege
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAX_SIZE="100M"
MAX_FILES="1000"

echo "🔍 МОНИТОРИНГ ПРОЕКТА VUEGE"
echo "=========================="

# Проверка размера проекта
PROJECT_SIZE=$(du -sh "$PROJECT_ROOT" 2>/dev/null | cut -f1)
PROJECT_SIZE_BYTES=$(du -sb "$PROJECT_ROOT" 2>/dev/null | cut -f1)

# Конвертация лимита в байты
if [[ $MAX_SIZE == *"M" ]]; then
    MAX_SIZE_BYTES=$(( ${MAX_SIZE%M} * 1024 * 1024 ))
elif [[ $MAX_SIZE == *"G" ]]; then
    MAX_SIZE_BYTES=$(( ${MAX_SIZE%G} * 1024 * 1024 * 1024 ))
else
    MAX_SIZE_BYTES=$(( MAX_SIZE * 1024 ))
fi

# Проверка количества файлов
FILE_COUNT=$(find "$PROJECT_ROOT" -type f 2>/dev/null | wc -l)

echo "Размер проекта: $PROJECT_SIZE"
echo "Количество файлов: $FILE_COUNT"

# Проверка лимитов
if [ $PROJECT_SIZE_BYTES -gt $MAX_SIZE_BYTES ]; then
    echo "❌ ПРЕВЫШЕН ЛИМИТ РАЗМЕРА: $PROJECT_SIZE > $MAX_SIZE"
    echo "Рекомендуется запустить: ./src/infrastructure/scripts/project-cleanup.sh"
    exit 1
fi

if [ $FILE_COUNT -gt $MAX_FILES ]; then
    echo "❌ ПРЕВЫШЕН ЛИМИТ ФАЙЛОВ: $FILE_COUNT > $MAX_FILES"
    echo "Рекомендуется запустить: ./src/infrastructure/scripts/project-cleanup.sh"
    exit 1
fi

echo "✅ Проект в пределах лимитов"
EOF
    
    chmod +x "project-monitor.sh"
    log_success "Создан скрипт мониторинга: project-monitor.sh"
    
    # Создание pre-commit hook
    mkdir -p .git/hooks
    cat > ".git/hooks/pre-commit" << 'EOF'
#!/bin/bash

# Pre-commit hook для проверки размера проекта
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
MONITOR_SCRIPT="$PROJECT_ROOT/project-monitor.sh"

if [ -f "$MONITOR_SCRIPT" ]; then
    if ! "$MONITOR_SCRIPT"; then
        echo "❌ Pre-commit проверка не пройдена"
        echo "Размер проекта превышает лимиты"
        exit 1
    fi
fi
EOF
    
    chmod +x .git/hooks/pre-commit
    log_success "Создан pre-commit hook"
}

# Функция восстановления из резервной копии
restore_backup() {
    log "🔄 ВОССТАНОВЛЕНИЕ ИЗ РЕЗЕРВНОЙ КОПИИ"
    echo "=================================="
    
    # Поиск резервных копий
    local backups=($(ls -d backup-* critical-backup-* 2>/dev/null | sort -r))
    
    if [ ${#backups[@]} -eq 0 ]; then
        log_error "Резервные копии не найдены"
        return
    fi
    
    echo "Доступные резервные копии:"
    for i in "${!backups[@]}"; do
        echo "$((i+1)). ${backups[$i]}"
    done
    
    read -p "Выберите номер резервной копии (1-${#backups[@]}): " choice
    
    if [[ ! "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt ${#backups[@]} ]; then
        log_error "Неверный выбор"
        return
    fi
    
    local selected_backup="${backups[$((choice-1))]}"
    log "Восстановление из $selected_backup..."
    
    # Восстановление файлов
    cp -r "$selected_backup"/* . 2>/dev/null || true
    log_success "Восстановление завершено"
}

# Главная функция
main() {
    echo "🧹 СКРИПТ ОЧИСТКИ ПРОЕКТА VUEGE"
    echo "================================"
    echo ""
    echo "Выберите действие:"
    echo "1. Диагностика проекта"
    echo "2. Безопасная очистка"
    echo "3. Критическая очистка"
    echo "4. Обновить .gitignore"
    echo "5. Создать систему мониторинга"
    echo "6. Восстановить из резервной копии"
    echo "7. Полная очистка и настройка"
    echo "0. Выход"
    echo ""
    
    read -p "Ваш выбор (0-7): " choice
    
    case $choice in
        1)
            diagnose_project
            ;;
        2)
            safe_cleanup
            ;;
        3)
            critical_cleanup
            ;;
        4)
            update_gitignore
            ;;
        5)
            create_monitoring
            ;;
        6)
            restore_backup
            ;;
        7)
            log "🚀 ПОЛНАЯ ОЧИСТКА И НАСТРОЙКА"
            echo "=================================="
            safe_cleanup
            update_gitignore
            create_monitoring
            log_success "Полная очистка и настройка завершена!"
            ;;
        0)
            log "Выход"
            exit 0
            ;;
        *)
            log_error "Неверный выбор"
            exit 1
            ;;
    esac
}

# Запуск главной функции
main "$@"
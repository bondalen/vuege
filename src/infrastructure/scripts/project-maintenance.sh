#!/bin/bash

# =============================================================================
# ГЛАВНЫЙ СКРИПТ УПРАВЛЕНИЯ ПРОЕКТОМ VUEGE
# Интегрированное решение на основе существующих скриптов
# =============================================================================

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Пути к существующим скриптам
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_MONITOR_SCRIPT="$SCRIPT_DIR/git-repository-monitor.sh"
PAGER_PROTECTION_SCRIPT="$SCRIPT_DIR/robust-pager-protection.sh"
MCP_CLEANUP_SCRIPT="$SCRIPT_DIR/mcp-management/cleanup_mcp_backups.py"

# Функции логирования
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

log_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Функция проверки существования скриптов
check_scripts() {
    log "🔍 ПРОВЕРКА ДОСТУПНОСТИ СКРИПТОВ"
    
    local missing_scripts=()
    
    if [ ! -f "$GIT_MONITOR_SCRIPT" ]; then
        missing_scripts+=("git-repository-monitor.sh")
    fi
    
    if [ ! -f "$PAGER_PROTECTION_SCRIPT" ]; then
        missing_scripts+=("robust-pager-protection.sh")
    fi
    
    if [ ! -f "$MCP_CLEANUP_SCRIPT" ]; then
        missing_scripts+=("cleanup_mcp_backups.py")
    fi
    
    if [ ${#missing_scripts[@]} -eq 0 ]; then
        log_success "Все скрипты доступны"
        return 0
    else
        log_error "Отсутствуют скрипты: ${missing_scripts[*]}"
        return 1
    fi
}

# Функция настройки защиты от pager
setup_pager_protection() {
    log "🛡️ НАСТРОЙКА ЗАЩИТЫ ОТ PAGER"
    
    if [ -f "$PAGER_PROTECTION_SCRIPT" ]; then
        source "$PAGER_PROTECTION_SCRIPT"
        log_success "Защита от pager настроена"
    else
        log_warning "Скрипт защиты от pager не найден"
        # Базовая настройка
        export PAGER=cat
        export LESS="-R -M --shift 5"
        export MORE="-R"
        git config --global core.pager cat 2>/dev/null || true
        log_success "Базовая защита от pager настроена"
    fi
}

# Функция мониторинга Git репозитория
monitor_git_repository() {
    log "📊 МОНИТОРИНГ GIT РЕПОЗИТОРИЯ"
    
    if [ -f "$GIT_MONITOR_SCRIPT" ]; then
        bash "$GIT_MONITOR_SCRIPT"
    else
        log_error "Скрипт мониторинга Git не найден"
        return 1
    fi
}

# Функция очистки MCP резервных копий
cleanup_mcp_backups() {
    log "🧹 ОЧИСТКА MCP РЕЗЕРВНЫХ КОПИЙ"
    
    if [ -f "$MCP_CLEANUP_SCRIPT" ]; then
        python3 "$MCP_CLEANUP_SCRIPT"
        log_success "Очистка MCP резервных копий завершена"
    else
        log_error "Скрипт очистки MCP не найден"
        return 1
    fi
}

# Функция безопасной очистки проекта
safe_project_cleanup() {
    log "🧹 БЕЗОПАСНАЯ ОЧИСТКА ПРОЕКТА"
    
    # Создание резервной копии
    local backup_dir="backup-$(date +%Y%m%d-%H%M%S)"
    log "Создание резервной копии в $backup_dir..."
    mkdir -p "$backup_dir"
    
    # Безопасные директории для удаления
    local safe_dirs=(
        "src/app/frontend/node_modules"
        "src/app/target"
        "mcp_cache"
        "src/app/frontend/dist"
        ".vscode"
    )
    
    for dir in "${safe_dirs[@]}"; do
        if [ -d "$dir" ]; then
            local size=$(du -sh "$dir" 2>/dev/null | cut -f1)
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

# Функция критической очистки
critical_project_cleanup() {
    log "🚨 КРИТИЧЕСКАЯ ОЧИСТКА ПРОЕКТА"
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
            local size=$(du -sh "$dir" 2>/dev/null | cut -f1)
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
create_monitoring_system() {
    log "📊 СОЗДАНИЕ СИСТЕМЫ МОНИТОРИНГА"
    
    # Создание pre-commit hook
    mkdir -p .git/hooks
    cat > ".git/hooks/pre-commit" << 'EOF'
#!/bin/bash

# Pre-commit hook для проверки размера проекта
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
MAINTENANCE_SCRIPT="$PROJECT_ROOT/src/infrastructure/scripts/project-maintenance.sh"

if [ -f "$MAINTENANCE_SCRIPT" ]; then
    if ! "$MAINTENANCE_SCRIPT" --check-size; then
        echo "❌ Pre-commit проверка не пройдена"
        echo "Размер проекта превышает лимиты"
        exit 1
    fi
fi
EOF
    
    chmod +x .git/hooks/pre-commit
    log_success "Создан pre-commit hook"
    
    # Создание скрипта автоматического мониторинга
    cat > "auto-monitor.sh" << 'EOF'
#!/bin/bash

# Автоматический мониторинг проекта Vuege
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAINTENANCE_SCRIPT="$PROJECT_ROOT/src/infrastructure/scripts/project-maintenance.sh"

echo "🔍 АВТОМАТИЧЕСКИЙ МОНИТОРИНГ ПРОЕКТА VUEGE"
echo "Дата: $(date)"

if [ -f "$MAINTENANCE_SCRIPT" ]; then
    "$MAINTENANCE_SCRIPT" --monitor-only
else
    echo "❌ Скрипт обслуживания не найден"
    exit 1
fi
EOF
    
    chmod +x "auto-monitor.sh"
    log_success "Создан скрипт автоматического мониторинга: auto-monitor.sh"
}

# Функция восстановления из резервной копии
restore_backup() {
    log "🔄 ВОССТАНОВЛЕНИЕ ИЗ РЕЗЕРВНОЙ КОПИИ"
    
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

# Функция полного обслуживания
full_maintenance() {
    log "🚀 ПОЛНОЕ ОБСЛУЖИВАНИЕ ПРОЕКТА"
    echo "=================================="
    
    # 1. Настройка защиты от pager
    setup_pager_protection
    
    # 2. Мониторинг Git репозитория
    monitor_git_repository
    
    # 3. Очистка MCP резервных копий
    cleanup_mcp_backups
    
    # 4. Безопасная очистка проекта
    safe_project_cleanup
    
    # 5. Обновление .gitignore
    update_gitignore
    
    # 6. Создание системы мониторинга
    create_monitoring_system
    
    log_success "Полное обслуживание проекта завершено!"
}

# Функция быстрой проверки
quick_check() {
    log "⚡ БЫСТРАЯ ПРОВЕРКА ПРОЕКТА"
    
    # Проверка размера проекта
    local project_size=$(du -sh . 2>/dev/null | cut -f1)
    local file_count=$(find . -type f 2>/dev/null | wc -l)
    
    echo "📊 Размер проекта: $project_size"
    echo "📁 Количество файлов: $file_count"
    
    # Проверка критических директорий
    local critical_dirs=("venv" "src/app/frontend/node_modules" "src/app/target" "mcp_cache")
    echo ""
    echo "🔍 Критические директории:"
    
    for dir in "${critical_dirs[@]}"; do
        if [ -d "$dir" ]; then
            local size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            echo "  $dir: $size"
        else
            echo "  $dir: не найдена"
        fi
    done
    
    # Проверка .gitignore
    if [ -f ".gitignore" ]; then
        local ignored_dirs=("venv" "node_modules" "target" "mcp_cache")
        echo ""
        echo "📋 Проверка .gitignore:"
        for dir in "${ignored_dirs[@]}"; do
            if grep -q "^$dir/" .gitignore 2>/dev/null || grep -q "^$dir$" .gitignore 2>/dev/null; then
                log_success "$dir/ в .gitignore"
            else
                log_warning "$dir/ НЕ в .gitignore"
            fi
        done
    fi
}

# Функция помощи
show_help() {
    echo "🧹 ГЛАВНЫЙ СКРИПТ УПРАВЛЕНИЯ ПРОЕКТОМ VUEGE"
    echo "=============================================="
    echo ""
    echo "Использование: $0 [опция]"
    echo ""
    echo "Опции:"
    echo "  --help, -h           Показать эту справку"
    echo "  --monitor-only       Только мониторинг Git репозитория"
    echo "  --check-size         Быстрая проверка размера проекта"
    echo "  --setup-pager        Настройка защиты от pager"
    echo "  --cleanup-mcp        Очистка MCP резервных копий"
    echo "  --safe-cleanup       Безопасная очистка проекта"
    echo "  --critical-cleanup   Критическая очистка проекта"
    echo "  --update-gitignore   Обновление .gitignore"
    echo "  --create-monitoring  Создание системы мониторинга"
    echo "  --restore-backup     Восстановление из резервной копии"
    echo "  --full-maintenance   Полное обслуживание проекта"
    echo ""
    echo "Без опций запускается интерактивное меню"
    echo ""
}

# Главная функция
main() {
    # Проверка аргументов командной строки
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --monitor-only)
            setup_pager_protection
            monitor_git_repository
            exit 0
            ;;
        --check-size)
            quick_check
            exit 0
            ;;
        --setup-pager)
            setup_pager_protection
            exit 0
            ;;
        --cleanup-mcp)
            cleanup_mcp_backups
            exit 0
            ;;
        --safe-cleanup)
            safe_project_cleanup
            exit 0
            ;;
        --critical-cleanup)
            critical_project_cleanup
            exit 0
            ;;
        --update-gitignore)
            update_gitignore
            exit 0
            ;;
        --create-monitoring)
            create_monitoring_system
            exit 0
            ;;
        --restore-backup)
            restore_backup
            exit 0
            ;;
        --full-maintenance)
            full_maintenance
            exit 0
            ;;
        "")
            # Интерактивное меню
            ;;
        *)
            log_error "Неизвестная опция: $1"
            show_help
            exit 1
            ;;
    esac
    
    # Интерактивное меню
    echo "🧹 ГЛАВНЫЙ СКРИПТ УПРАВЛЕНИЯ ПРОЕКТОМ VUEGE"
    echo "=============================================="
    echo ""
    echo "Выберите действие:"
    echo "1. Быстрая проверка проекта"
    echo "2. Мониторинг Git репозитория"
    echo "3. Настройка защиты от pager"
    echo "4. Очистка MCP резервных копий"
    echo "5. Безопасная очистка проекта"
    echo "6. Критическая очистка проекта"
    echo "7. Обновить .gitignore"
    echo "8. Создать систему мониторинга"
    echo "9. Восстановить из резервной копии"
    echo "10. Полное обслуживание проекта"
    echo "0. Выход"
    echo ""
    
    read -p "Ваш выбор (0-10): " choice
    
    case $choice in
        1)
            quick_check
            ;;
        2)
            setup_pager_protection
            monitor_git_repository
            ;;
        3)
            setup_pager_protection
            ;;
        4)
            cleanup_mcp_backups
            ;;
        5)
            safe_project_cleanup
            ;;
        6)
            critical_project_cleanup
            ;;
        7)
            update_gitignore
            ;;
        8)
            create_monitoring_system
            ;;
        9)
            restore_backup
            ;;
        10)
            full_maintenance
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
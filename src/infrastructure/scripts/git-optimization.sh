#!/bin/bash

# =============================================================================
# СКРИПТ ОПТИМИЗАЦИИ GIT РЕПОЗИТОРИЯ
# Анализ и очистка раздутого .git
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

# Функция анализа размера .git
analyze_git_size() {
    log "📊 АНАЛИЗ РАЗМЕРА .GIT ДИРЕКТОРИИ"
    
    if [ ! -d ".git" ]; then
        log_error ".git директория не найдена"
        return 1
    fi
    
    # Размер .git
    local git_size=$(du -sh .git 2>/dev/null | cut -f1)
    echo "   Размер .git: $git_size"
    
    # Размер objects
    if [ -d ".git/objects" ]; then
        local objects_size=$(du -sh .git/objects 2>/dev/null | cut -f1)
        echo "   Размер objects: $objects_size"
    fi
    
    # Размер pack
    if [ -d ".git/objects/pack" ]; then
        local pack_size=$(du -sh .git/objects/pack 2>/dev/null | cut -f1)
        echo "   Размер pack: $pack_size"
    fi
    
    # Количество loose объектов
    local loose_objects=$(find .git/objects -type f -name "??" 2>/dev/null | wc -l)
    echo "   Loose объектов: $loose_objects"
    
    # Количество pack файлов
    local pack_files=$(find .git/objects/pack -name "*.pack" 2>/dev/null | wc -l)
    echo "   Pack файлов: $pack_files"
}

# Функция поиска больших файлов
find_large_files() {
    log "🔍 ПОИСК БОЛЬШИХ ФАЙЛОВ В ИСТОРИИ"
    
    echo "   Топ-10 самых больших файлов:"
    
    # Поиск больших файлов (если git доступен)
    if command -v git >/dev/null 2>&1; then
        git rev-list --objects --all 2>/dev/null | \
        git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' 2>/dev/null | \
        sed -n 's/^blob //p' | \
        sort --numeric-sort --key=2 | \
        tail -10 | \
        while read hash size path; do
            local size_mb=$((size / 1024 / 1024))
            if [ "$size_mb" -gt 1 ]; then
                echo "   $size_mb MB: $path"
            fi
        done
    else
        log_warning "Git не доступен для анализа больших файлов"
    fi
}

# Функция анализа объектов Git
analyze_git_objects() {
    log "📈 АНАЛИЗ ОБЪЕКТОВ GIT"
    
    if command -v git >/dev/null 2>&1; then
        echo "   Статистика объектов:"
        git count-objects -vH 2>/dev/null || log_warning "Не удалось получить статистику объектов"
    else
        log_warning "Git не доступен для анализа объектов"
    fi
}

# Функция оптимизации Git
optimize_git() {
    log "🛠️ ОПТИМИЗАЦИЯ GIT РЕПОЗИТОРИЯ"
    
    if ! command -v git >/dev/null 2>&1; then
        log_error "Git не доступен"
        return 1
    fi
    
    # Создание резервной копии
    local backup_dir="git-backup-$(date +%Y%m%d-%H%M%S)"
    log "Создание резервной копии в $backup_dir..."
    cp -r .git "$backup_dir" 2>/dev/null || log_warning "Не удалось создать резервную копию"
    
    # Упаковка объектов
    log "Упаковка объектов..."
    git gc --aggressive 2>/dev/null || log_warning "Не удалось выполнить git gc"
    
    # Удаление неиспользуемых объектов
    log "Удаление неиспользуемых объектов..."
    git prune 2>/dev/null || log_warning "Не удалось выполнить git prune"
    
    # Полная очистка
    log "Полная очистка..."
    git gc --prune=now --aggressive 2>/dev/null || log_warning "Не удалось выполнить полную очистку"
    
    log_success "Оптимизация завершена"
}

# Функция удаления больших файлов из истории
remove_large_files_from_history() {
    log "🗑️ УДАЛЕНИЕ БОЛЬШИХ ФАЙЛОВ ИЗ ИСТОРИИ"
    
    if ! command -v git >/dev/null 2>&1; then
        log_error "Git не доступен"
        return 1
    fi
    
    # Список файлов для удаления
    local files_to_remove=(
        "node_modules"
        "target"
        "*.jar"
        "*.war"
        "*.log"
        "*.tmp"
        "*.temp"
        "venv"
        "mcp_cache"
    )
    
    log_warning "ВНИМАНИЕ: Эта операция изменит историю Git!"
    log_warning "Убедитесь, что у вас есть резервная копия!"
    
    read -p "Продолжить удаление больших файлов из истории? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Операция отменена"
        return
    fi
    
    for file in "${files_to_remove[@]}"; do
        log "Удаление $file из истории..."
        git filter-branch --force --index-filter "git rm --cached --ignore-unmatch -r '$file'" --prune-empty --tag-name-filter cat -- --all 2>/dev/null || log_warning "Не удалось удалить $file"
    done
    
    # Очистка после удаления
    log "Очистка после удаления..."
    git for-each-ref --format='delete %(refname)' refs/original 2>/dev/null | git update-ref --stdin 2>/dev/null || true
    git reflog expire --expire=now --all 2>/dev/null || true
    git gc --prune=now --aggressive 2>/dev/null || true
    
    log_success "Удаление больших файлов завершено"
}

# Функция создания .gitignore
create_gitignore() {
    log "📝 СОЗДАНИЕ .GITIGNORE"
    
    if [ ! -f ".gitignore" ]; then
        log "Создание нового .gitignore..."
        touch .gitignore
    fi
    
    # Добавление исключений для больших файлов
    local exclusions=(
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
        "# Large files"
        "*.mp3"
        "*.mp4"
        "*.zip"
        "*.tar.gz"
        "*.rar"
        ""
        "# OS"
        ".DS_Store"
        "Thumbs.db"
    )
    
    for exclusion in "${exclusions[@]}"; do
        if [ "$exclusion" = "" ]; then
            echo "" >> .gitignore
        elif ! grep -q "^${exclusion}$" .gitignore 2>/dev/null; then
            echo "$exclusion" >> .gitignore
            log_success "Добавлено в .gitignore: $exclusion"
        fi
    done
    
    log_success ".gitignore обновлен"
}

# Функция создания pre-commit hook
create_pre_commit_hook() {
    log "🔧 СОЗДАНИЕ PRE-COMMIT HOOK"
    
    mkdir -p .git/hooks
    
    cat > ".git/hooks/pre-commit" << 'EOF'
#!/bin/bash

# Pre-commit hook для проверки размера файлов
MAX_FILE_SIZE=10485760  # 10MB

echo "🔍 ПРОВЕРКА РАЗМЕРА ФАЙЛОВ..."

# Проверка размера добавляемых файлов
git diff --cached --name-only | while read file; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo "0")
        if [ "$size" -gt "$MAX_FILE_SIZE" ]; then
            echo "❌ Файл $file слишком большой ($size байт)"
            echo "Максимальный размер: $MAX_FILE_SIZE байт"
            exit 1
        fi
    fi
done

# Проверка размера .git
git_size=$(du -sm .git | cut -f1)
if [ "$git_size" -gt 100 ]; then
    echo "⚠️  Размер .git превышает 100MB ($git_size MB)"
    echo "Рекомендуется очистка"
fi

echo "✅ Проверка размера файлов пройдена"
EOF
    
    chmod +x .git/hooks/pre-commit
    log_success "Pre-commit hook создан"
}

# Функция полной оптимизации
full_optimization() {
    log "🚀 ПОЛНАЯ ОПТИМИЗАЦИЯ GIT РЕПОЗИТОРИЯ"
    echo "=========================================="
    
    # 1. Анализ текущего состояния
    analyze_git_size
    echo ""
    
    # 2. Поиск больших файлов
    find_large_files
    echo ""
    
    # 3. Анализ объектов
    analyze_git_objects
    echo ""
    
    # 4. Оптимизация
    optimize_git
    echo ""
    
    # 5. Создание .gitignore
    create_gitignore
    echo ""
    
    # 6. Создание pre-commit hook
    create_pre_commit_hook
    echo ""
    
    # 7. Финальный анализ
    log "📊 ФИНАЛЬНЫЙ АНАЛИЗ"
    analyze_git_size
    
    log_success "Полная оптимизация завершена!"
}

# Функция помощи
show_help() {
    echo "🛠️ СКРИПТ ОПТИМИЗАЦИИ GIT РЕПОЗИТОРИЯ"
    echo "========================================"
    echo ""
    echo "Использование: $0 [опция]"
    echo ""
    echo "Опции:"
    echo "  --help, -h           Показать эту справку"
    echo "  --analyze            Анализ размера .git"
    echo "  --find-large-files   Поиск больших файлов"
    echo "  --optimize           Базовая оптимизация"
    echo "  --remove-large       Удаление больших файлов из истории"
    echo "  --create-gitignore   Создание .gitignore"
    echo "  --create-hook        Создание pre-commit hook"
    echo "  --full-optimization  Полная оптимизация"
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
        --analyze)
            analyze_git_size
            find_large_files
            analyze_git_objects
            exit 0
            ;;
        --find-large-files)
            find_large_files
            exit 0
            ;;
        --optimize)
            optimize_git
            exit 0
            ;;
        --remove-large)
            remove_large_files_from_history
            exit 0
            ;;
        --create-gitignore)
            create_gitignore
            exit 0
            ;;
        --create-hook)
            create_pre_commit_hook
            exit 0
            ;;
        --full-optimization)
            full_optimization
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
    echo "🛠️ СКРИПТ ОПТИМИЗАЦИИ GIT РЕПОЗИТОРИЯ"
    echo "========================================"
    echo ""
    echo "Выберите действие:"
    echo "1. Анализ размера .git"
    echo "2. Поиск больших файлов"
    echo "3. Базовая оптимизация"
    echo "4. Удаление больших файлов из истории"
    echo "5. Создание .gitignore"
    echo "6. Создание pre-commit hook"
    echo "7. Полная оптимизация"
    echo "0. Выход"
    echo ""
    
    read -p "Ваш выбор (0-7): " choice
    
    case $choice in
        1)
            analyze_git_size
            find_large_files
            analyze_git_objects
            ;;
        2)
            find_large_files
            ;;
        3)
            optimize_git
            ;;
        4)
            remove_large_files_from_history
            ;;
        5)
            create_gitignore
            ;;
        6)
            create_pre_commit_hook
            ;;
        7)
            full_optimization
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
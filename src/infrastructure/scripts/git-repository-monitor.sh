#!/bin/bash

# @file: git-repository-monitor.sh
# @description: Мониторинг размера Git репозитория для предотвращения раздувания
# @pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
# @dependencies: git, du, find
# @created: 2025-08-20
# @updated: 2025-08-25 - Добавлена интерактивность и интеграция

# Настройка защиты от pager
export PAGER=cat
export LESS="-R -M --shift 5"
export MORE="-R"
export COMPOSER_NO_INTERACTION=1
export TERM=xterm-256color
export COLUMNS=120
export LINES=30
export GIT_PAGER=cat
export GIT_EDITOR=vim

# Настройка git pager глобально
git config --global core.pager cat 2>/dev/null

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Лимиты для предупреждений
REPO_SIZE_LIMIT_MB=100
GIT_SIZE_LIMIT_MB=50
FILES_LIMIT=1000
CRITICAL_SIZE_MB=500

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

# Функция получения размера в байтах
get_size_bytes() {
    local size_str="$1"
    if [[ $size_str == *"M" ]]; then
        echo $(( ${size_str%M} * 1024 * 1024 ))
    elif [[ $size_str == *"G" ]]; then
        echo $(( ${size_str%G} * 1024 * 1024 * 1024 ))
    elif [[ $size_str == *"K" ]]; then
        echo $(( ${size_str%K} * 1024 ))
    else
        echo $(( size_str * 1024 ))
    fi
}

# Функция конвертации байтов в человекочитаемый формат
format_bytes() {
    local bytes="$1"
    if [ $bytes -gt 1073741824 ]; then
        echo "$((bytes / 1073741824))G"
    elif [ $bytes -gt 1048576 ]; then
        echo "$((bytes / 1048576))M"
    elif [ $bytes -gt 1024 ]; then
        echo "$((bytes / 1024))K"
    else
        echo "${bytes}B"
    fi
}

# Функция анализа размера репозитория
analyze_repository_size() {
    echo "📊 АНАЛИЗ РАЗМЕРА РЕПОЗИТОРИЯ:"
    repo_size_mb=$(du -sm . | cut -f1)
    echo "   Общий размер: ${repo_size_mb}MB"
    
    local repo_size_bytes=$((repo_size_mb * 1024 * 1024))
    local limit_bytes=$((REPO_SIZE_LIMIT_MB * 1024 * 1024))
    local critical_bytes=$((CRITICAL_SIZE_MB * 1024 * 1024))
    
    if [ "$repo_size_bytes" -gt "$critical_bytes" ]; then
        echo -e "   ${RED}🚨 КРИТИЧЕСКОЕ ПРЕВЫШЕНИЕ: Размер репозитория превышает критический лимит ${CRITICAL_SIZE_MB}MB${NC}"
        return 2
    elif [ "$repo_size_bytes" -gt "$limit_bytes" ]; then
        echo -e "   ${YELLOW}⚠️  ПРЕДУПРЕЖДЕНИЕ: Размер репозитория превышает лимит ${REPO_SIZE_LIMIT_MB}MB${NC}"
        return 1
    else
        echo -e "   ${GREEN}✅ Размер репозитория в норме${NC}"
        return 0
    fi
}

# Функция анализа размера .git
analyze_git_size() {
    if [ -d ".git" ]; then
        git_size_mb=$(du -sm .git | cut -f1)
        echo "   Размер .git: ${git_size_mb}MB"
        
        local git_size_bytes=$((git_size_mb * 1024 * 1024))
        local limit_bytes=$((GIT_SIZE_LIMIT_MB * 1024 * 1024))
        
        if [ "$git_size_bytes" -gt "$limit_bytes" ]; then
            echo -e "   ${YELLOW}⚠️  ПРЕДУПРЕЖДЕНИЕ: Размер .git превышает лимит ${GIT_SIZE_LIMIT_MB}MB${NC}"
            return 1
        else
            echo -e "   ${GREEN}✅ Размер .git в норме${NC}"
            return 0
        fi
    else
        echo -e "   ${YELLOW}⚠️  .git директория не найдена${NC}"
        return 0
    fi
}

# Функция анализа файлов для коммита
analyze_staged_files() {
    echo ""
    echo "📁 АНАЛИЗ ФАЙЛОВ ДЛЯ КОММИТА:"
    files_count=$(git status --porcelain | wc -l)
    echo "   Файлов для коммита: ${files_count}"
    
    if [ "$files_count" -gt "$FILES_LIMIT" ]; then
        echo -e "   ${YELLOW}⚠️  ПРЕДУПРЕЖДЕНИЕ: Количество файлов превышает лимит ${FILES_LIMIT}${NC}"
        return 1
    else
        echo -e "   ${GREEN}✅ Количество файлов в норме${NC}"
        return 0
    fi
}

# Функция анализа проблемных директорий
analyze_problematic_directories() {
    echo ""
    echo "🔍 ПРОВЕРКА ПРОБЛЕМНЫХ ДИРЕКТОРИЙ:"
    problematic_dirs=("venv" "node_modules" "mcp_cache" ".git" "__pycache__" "target" "dist")
    local has_problems=false
    
    for dir in "${problematic_dirs[@]}"; do
        if [ -d "$dir" ]; then
            dir_size_mb=$(du -sm "$dir" 2>/dev/null | cut -f1)
            echo "   ${dir}/: ${dir_size_mb}MB"
            
            if [ "$dir_size_mb" -gt 10 ]; then
                echo -e "   ${YELLOW}⚠️  ПРЕДУПРЕЖДЕНИЕ: ${dir}/ слишком большой${NC}"
                has_problems=true
            fi
        fi
    done
    
    if [ "$has_problems" = true ]; then
        return 1
    else
        return 0
    fi
}

# Функция проверки .gitignore
check_gitignore() {
    echo ""
    echo "📋 ПРОВЕРКА .GITIGNORE:"
    if [ -f ".gitignore" ]; then
        echo "   .gitignore найден"
        
        # Проверка ключевых исключений
        key_exclusions=("venv/" "node_modules/" "mcp_cache/" ".git/" "target/" "dist/")
        missing_exclusions=()
        
        for exclusion in "${key_exclusions[@]}"; do
            if ! grep -q "^${exclusion}" .gitignore; then
                missing_exclusions+=("$exclusion")
            fi
        done
        
        if [ ${#missing_exclusions[@]} -eq 0 ]; then
            echo -e "   ${GREEN}✅ Все ключевые исключения присутствуют${NC}"
            return 0
        else
            echo -e "   ${YELLOW}⚠️  Отсутствуют исключения: ${missing_exclusions[*]}${NC}"
            return 1
        fi
    else
        echo -e "   ${RED}❌ .gitignore не найден${NC}"
        return 1
    fi
}

# Функция создания отчета
create_report() {
    local report_file="git-monitor-report-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "ОТЧЕТ МОНИТОРИНГА GIT РЕПОЗИТОРИЯ"
        echo "Дата: $(date)"
        echo "Репозиторий: $(pwd)"
        echo ""
        echo "РАЗМЕР РЕПОЗИТОРИЯ:"
        echo "  Общий размер: ${repo_size_mb}MB"
        echo "  Размер .git: ${git_size_mb}MB"
        echo "  Файлов для коммита: ${files_count}"
        echo ""
        echo "ПРОБЛЕМНЫЕ ДИРЕКТОРИИ:"
        for dir in "${problematic_dirs[@]}"; do
            if [ -d "$dir" ]; then
                dir_size_mb=$(du -sm "$dir" 2>/dev/null | cut -f1)
                echo "  ${dir}/: ${dir_size_mb}MB"
            fi
        done
        echo ""
        echo "СТАТУС: $([ "$has_critical_issues" = true ] && echo "КРИТИЧЕСКИЙ" || [ "$has_warnings" = true ] && echo "ТРЕБУЕТ ВНИМАНИЯ" || echo "ОТЛИЧНЫЙ")"
    } > "$report_file"
    
    log_success "Отчет сохранен: $report_file"
}

# Функция рекомендаций
show_recommendations() {
    echo ""
    echo "💡 РЕКОМЕНДАЦИИ:"
    
    if [ "$has_critical_issues" = true ]; then
        echo -e "   ${RED}🚨 КРИТИЧЕСКАЯ СИТУАЦИЯ: Требуется немедленное действие${NC}"
        echo "   - Запустите: ./src/infrastructure/scripts/project-maintenance.sh --critical-cleanup"
        echo "   - Проверьте .gitignore на предмет исключения больших директорий"
        echo "   - Удалите большие файлы из истории: git filter-branch"
        echo "   - Рассмотрите возможность пересоздания репозитория"
        echo "   - Используйте Git LFS для больших файлов"
    elif [ "$has_warnings" = true ]; then
        echo -e "   ${YELLOW}⚠️  ТРЕБУЕТСЯ ВНИМАНИЕ${NC}"
        echo "   - Запустите: ./src/infrastructure/scripts/project-maintenance.sh --safe-cleanup"
        echo "   - Обновите .gitignore при добавлении новых зависимостей"
        echo "   - Регулярно запускайте мониторинг"
        echo "   - Используйте pre-commit hooks для проверки размера"
    else
        echo -e "   ${GREEN}✅ Репозиторий в хорошем состоянии${NC}"
        echo "   - Продолжайте регулярный мониторинг"
        echo "   - Обновляйте .gitignore при добавлении новых зависимостей"
        echo "   - Используйте: ./src/infrastructure/scripts/project-maintenance.sh --monitor-only"
    fi
}

# Функция интерактивного меню
interactive_menu() {
    echo ""
    echo "🎛️  ИНТЕРАКТИВНОЕ МЕНЮ:"
    echo "1. Запустить безопасную очистку"
    echo "2. Запустить критическую очистку"
    echo "3. Обновить .gitignore"
    echo "4. Создать систему мониторинга"
    echo "5. Показать детальный анализ"
    echo "0. Выход"
    echo ""
    
    read -p "Ваш выбор (0-5): " choice
    
    case $choice in
        1)
            log_info "Запуск безопасной очистки..."
            if [ -f "../project-maintenance.sh" ]; then
                bash "../project-maintenance.sh" --safe-cleanup
            else
                log_error "Скрипт project-maintenance.sh не найден"
            fi
            ;;
        2)
            log_warning "Запуск критической очистки..."
            if [ -f "../project-maintenance.sh" ]; then
                bash "../project-maintenance.sh" --critical-cleanup
            else
                log_error "Скрипт project-maintenance.sh не найден"
            fi
            ;;
        3)
            log_info "Обновление .gitignore..."
            if [ -f "../project-maintenance.sh" ]; then
                bash "../project-maintenance.sh" --update-gitignore
            else
                log_error "Скрипт project-maintenance.sh не найден"
            fi
            ;;
        4)
            log_info "Создание системы мониторинга..."
            if [ -f "../project-maintenance.sh" ]; then
                bash "../project-maintenance.sh" --create-monitoring
            else
                log_error "Скрипт project-maintenance.sh не найден"
            fi
            ;;
        5)
            show_detailed_analysis
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

# Функция детального анализа
show_detailed_analysis() {
    echo ""
    echo "📈 ДЕТАЛЬНЫЙ АНАЛИЗ РЕПОЗИТОРИЯ"
    echo "================================"
    
    # Анализ крупных файлов
    echo "🔍 КРУПНЕЙШИЕ ФАЙЛЫ:"
    find . -type f -size +1M -exec ls -lh {} \; 2>/dev/null | head -10 | while read line; do
        echo "   $line"
    done
    
    # Анализ крупных директорий
    echo ""
    echo "📁 КРУПНЕЙШИЕ ДИРЕКТОРИИ:"
    du -sh */ 2>/dev/null | sort -hr | head -10 | while read line; do
        echo "   $line"
    done
    
    # Анализ Git истории
    echo ""
    echo "🔧 АНАЛИЗ GIT ИСТОРИИ:"
    if [ -d ".git" ]; then
        local commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")
        local branch_count=$(git branch -r | wc -l 2>/dev/null || echo "0")
        local tag_count=$(git tag | wc -l 2>/dev/null || echo "0")
        
        echo "   Количество коммитов: $commit_count"
        echo "   Количество веток: $branch_count"
        echo "   Количество тегов: $tag_count"
    fi
}

# Основная функция мониторинга
main() {
    echo "=== МОНИТОРИНГ РАЗМЕРА GIT РЕПОЗИТОРИЯ ==="
    echo "Дата: $(date)"
    echo "Репозиторий: $(pwd)"
    echo ""
    
    local has_critical_issues=false
    local has_warnings=false
    
    # Анализ размера репозитория
    analyze_repository_size
    case $? in
        2) has_critical_issues=true ;;
        1) has_warnings=true ;;
    esac
    
    # Анализ размера .git
    analyze_git_size
    if [ $? -eq 1 ]; then
        has_warnings=true
    fi
    
    # Анализ файлов для коммита
    analyze_staged_files
    if [ $? -eq 1 ]; then
        has_warnings=true
    fi
    
    # Анализ проблемных директорий
    analyze_problematic_directories
    if [ $? -eq 1 ]; then
        has_warnings=true
    fi
    
    # Проверка .gitignore
    check_gitignore
    if [ $? -eq 1 ]; then
        has_warnings=true
    fi
    
    # Создание отчета
    create_report
    
    # Показать рекомендации
    show_recommendations
    
    # Интерактивное меню (если не в автоматическом режиме)
    if [ "${1:-}" != "--no-interactive" ]; then
        interactive_menu
    fi
    
    echo ""
    echo "=== МОНИТОРИНГ ЗАВЕРШЕН ==="
    
    # Возврат кода ошибки для автоматизации
    if [ "$has_critical_issues" = true ]; then
        exit 2
    elif [ "$has_warnings" = true ]; then
        exit 1
    else
        exit 0
    fi
}

# Проверка аргументов командной строки
case "${1:-}" in
    --help|-h)
        echo "Использование: $0 [опция]"
        echo ""
        echo "Опции:"
        echo "  --help, -h           Показать справку"
        echo "  --no-interactive     Запуск без интерактивного меню"
        echo "  --detailed           Показать детальный анализ"
        echo ""
        exit 0
        ;;
    --detailed)
        show_detailed_analysis
        exit 0
        ;;
esac

# Запуск основной функции
main "$@"
#!/bin/bash

# =============================================================================
# СКРИПТ МОНИТОРИНГА ПРОЕКТА VUEGE
# Автоматическая проверка размера и состояния проекта
# =============================================================================

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Конфигурация
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
MAX_SIZE="100M"
MAX_FILES="1000"
MAX_GIT_SIZE="50M"
CRITICAL_SIZE="500M"

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

# Основная функция мониторинга
main() {
    echo "🔍 МОНИТОРИНГ ПРОЕКТА VUEGE"
    echo "=========================="
    echo "Проект: $PROJECT_ROOT"
    echo "Дата: $(date)"
    echo ""
    
    # Проверка размера проекта
    local project_size=$(du -sh "$PROJECT_ROOT" 2>/dev/null | cut -f1)
    local project_size_bytes=$(du -sb "$PROJECT_ROOT" 2>/dev/null | cut -f1)
    local max_size_bytes=$(get_size_bytes "$MAX_SIZE")
    local critical_size_bytes=$(get_size_bytes "$CRITICAL_SIZE")
    
    echo "📊 РАЗМЕР ПРОЕКТА:"
    echo "  Текущий: $project_size"
    echo "  Лимит: $MAX_SIZE"
    echo "  Критический: $CRITICAL_SIZE"
    
    # Проверка количества файлов
    local file_count=$(find "$PROJECT_ROOT" -type f 2>/dev/null | wc -l)
    echo ""
    echo "📁 КОЛИЧЕСТВО ФАЙЛОВ:"
    echo "  Текущее: $file_count"
    echo "  Лимит: $MAX_FILES"
    
    # Проверка Git репозитория
    if [ -d "$PROJECT_ROOT/.git" ]; then
        local git_size=$(du -sh "$PROJECT_ROOT/.git" 2>/dev/null | cut -f1)
        local git_size_bytes=$(du -sb "$PROJECT_ROOT/.git" 2>/dev/null | cut -f1)
        local max_git_bytes=$(get_size_bytes "$MAX_GIT_SIZE")
        
        echo ""
        echo "🔧 GIT РЕПОЗИТОРИЙ:"
        echo "  Размер .git: $git_size"
        echo "  Лимит: $MAX_GIT_SIZE"
        
        # Количество файлов для коммита
        local staged_files=$(git -C "$PROJECT_ROOT" status --porcelain 2>/dev/null | wc -l)
        echo "  Файлов для коммита: $staged_files"
    fi
    
    # Анализ крупных директорий
    echo ""
    echo "📈 АНАЛИЗ КРУПНЫХ ДИРЕКТОРИЙ:"
    local large_dirs=(
        "venv"
        "src/app/frontend/node_modules"
        "src/app/target"
        "mcp_cache"
        "src/app/frontend/dist"
        ".git"
    )
    
    for dir in "${large_dirs[@]}"; do
        local full_path="$PROJECT_ROOT/$dir"
        if [ -d "$full_path" ]; then
            local size=$(du -sh "$full_path" 2>/dev/null | cut -f1)
            local count=$(find "$full_path" -type f 2>/dev/null | wc -l)
            printf "  %-25s %8s (%6s файлов)\n" "$dir" "$size" "$count"
        fi
    done
    
    # Проверка .gitignore
    echo ""
    echo "📋 ПРОВЕРКА .GITIGNORE:"
    if [ -f "$PROJECT_ROOT/.gitignore" ]; then
        local ignored_dirs=("venv" "node_modules" "target" "mcp_cache" ".vscode" ".cursor")
        for dir in "${ignored_dirs[@]}"; do
            if grep -q "^$dir/" "$PROJECT_ROOT/.gitignore" 2>/dev/null || grep -q "^$dir$" "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
                log_success "$dir/ в .gitignore"
            else
                log_warning "$dir/ НЕ в .gitignore"
            fi
        done
    else
        log_error ".gitignore не найден!"
    fi
    
    # Проверка лимитов и вывод результатов
    echo ""
    echo "🎯 РЕЗУЛЬТАТЫ ПРОВЕРКИ:"
    
    local has_warnings=false
    local has_errors=false
    
    # Проверка размера проекта
    if [ $project_size_bytes -gt $critical_size_bytes ]; then
        log_error "КРИТИЧЕСКОЕ ПРЕВЫШЕНИЕ РАЗМЕРА: $project_size > $CRITICAL_SIZE"
        has_errors=true
    elif [ $project_size_bytes -gt $max_size_bytes ]; then
        log_warning "ПРЕВЫШЕН ЛИМИТ РАЗМЕРА: $project_size > $MAX_SIZE"
        has_warnings=true
    else
        log_success "Размер проекта в пределах нормы"
    fi
    
    # Проверка количества файлов
    if [ $file_count -gt $MAX_FILES ]; then
        log_warning "ПРЕВЫШЕН ЛИМИТ ФАЙЛОВ: $file_count > $MAX_FILES"
        has_warnings=true
    else
        log_success "Количество файлов в пределах нормы"
    fi
    
    # Проверка размера Git
    if [ -d "$PROJECT_ROOT/.git" ] && [ $git_size_bytes -gt $max_git_bytes ]; then
        log_warning "ПРЕВЫШЕН ЛИМИТ GIT: $git_size > $MAX_GIT_SIZE"
        has_warnings=true
    fi
    
    # Рекомендации
    echo ""
    echo "💡 РЕКОМЕНДАЦИИ:"
    
    if [ "$has_errors" = true ]; then
        echo "  🚨 КРИТИЧЕСКАЯ СИТУАЦИЯ!"
        echo "  Выполните: ./src/infrastructure/scripts/project-cleanup.sh"
        echo "  Выберите опцию 3 (Критическая очистка)"
        exit 1
    elif [ "$has_warnings" = true ]; then
        echo "  ⚠️  ТРЕБУЕТСЯ ОЧИСТКА"
        echo "  Выполните: ./src/infrastructure/scripts/project-cleanup.sh"
        echo "  Выберите опцию 2 (Безопасная очистка)"
        exit 1
    else
        echo "  ✅ Проект в отличном состоянии"
        echo "  Рекомендуется регулярный мониторинг"
    fi
    
    # Создание отчета
    local report_file="$PROJECT_ROOT/project-monitor-report-$(date +%Y%m%d-%H%M%S).txt"
    {
        echo "ОТЧЕТ МОНИТОРИНГА ПРОЕКТА VUEGE"
        echo "Дата: $(date)"
        echo "Размер проекта: $project_size"
        echo "Количество файлов: $file_count"
        echo "Статус: $([ "$has_errors" = true ] && echo "КРИТИЧЕСКИЙ" || [ "$has_warnings" = true ] && echo "ТРЕБУЕТ ОЧИСТКИ" || echo "ОТЛИЧНЫЙ")"
    } > "$report_file"
    
    log_success "Отчет сохранен: $report_file"
}

# Запуск мониторинга
main "$@"
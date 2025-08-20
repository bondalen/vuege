#!/bin/bash

# @file: git-repository-monitor.sh
# @description: Мониторинг размера Git репозитория для предотвращения раздувания
# @pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
# @dependencies: git, du, find
# @created: 2025-08-20

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
NC='\033[0m' # No Color

# Лимиты для предупреждений
REPO_SIZE_LIMIT_MB=100
GIT_SIZE_LIMIT_MB=50
FILES_LIMIT=1000

echo "=== МОНИТОРИНГ РАЗМЕРА GIT РЕПОЗИТОРИЯ ==="
echo "Дата: $(date)"
echo "Репозиторий: $(pwd)"
echo ""

# Проверка размера репозитория
echo "📊 АНАЛИЗ РАЗМЕРА РЕПОЗИТОРИЯ:"
repo_size_mb=$(du -sm . | cut -f1)
echo "   Общий размер: ${repo_size_mb}MB"

if [ "$repo_size_mb" -gt "$REPO_SIZE_LIMIT_MB" ]; then
    echo -e "   ${RED}⚠️  ПРЕДУПРЕЖДЕНИЕ: Размер репозитория превышает лимит ${REPO_SIZE_LIMIT_MB}MB${NC}"
else
    echo -e "   ${GREEN}✅ Размер репозитория в норме${NC}"
fi

# Проверка размера .git
if [ -d ".git" ]; then
    git_size_mb=$(du -sm .git | cut -f1)
    echo "   Размер .git: ${git_size_mb}MB"
    
    if [ "$git_size_mb" -gt "$GIT_SIZE_LIMIT_MB" ]; then
        echo -e "   ${RED}⚠️  ПРЕДУПРЕЖДЕНИЕ: Размер .git превышает лимит ${GIT_SIZE_LIMIT_MB}MB${NC}"
    else
        echo -e "   ${GREEN}✅ Размер .git в норме${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠️  .git директория не найдена${NC}"
fi

echo ""

# Проверка количества файлов для коммита
echo "📁 АНАЛИЗ ФАЙЛОВ ДЛЯ КОММИТА:"
files_count=$(git status --porcelain | wc -l)
echo "   Файлов для коммита: ${files_count}"

if [ "$files_count" -gt "$FILES_LIMIT" ]; then
    echo -e "   ${RED}⚠️  ПРЕДУПРЕЖДЕНИЕ: Количество файлов превышает лимит ${FILES_LIMIT}${NC}"
else
    echo -e "   ${GREEN}✅ Количество файлов в норме${NC}"
fi

echo ""

# Проверка проблемных директорий
echo "🔍 ПРОВЕРКА ПРОБЛЕМНЫХ ДИРЕКТОРИЙ:"
problematic_dirs=("venv" "node_modules" "mcp_cache" ".git" "__pycache__")

for dir in "${problematic_dirs[@]}"; do
    if [ -d "$dir" ]; then
        dir_size_mb=$(du -sm "$dir" 2>/dev/null | cut -f1)
        echo "   ${dir}/: ${dir_size_mb}MB"
        
        if [ "$dir_size_mb" -gt 10 ]; then
            echo -e "   ${RED}⚠️  ПРЕДУПРЕЖДЕНИЕ: ${dir}/ слишком большой${NC}"
        fi
    fi
done

echo ""

# Проверка .gitignore
echo "📋 ПРОВЕРКА .GITIGNORE:"
if [ -f ".gitignore" ]; then
    echo "   .gitignore найден"
    
    # Проверка ключевых исключений
    key_exclusions=("venv/" "node_modules/" "mcp_cache/" ".git/")
    missing_exclusions=()
    
    for exclusion in "${key_exclusions[@]}"; do
        if ! grep -q "^${exclusion}" .gitignore; then
            missing_exclusions+=("$exclusion")
        fi
    done
    
    if [ ${#missing_exclusions[@]} -eq 0 ]; then
        echo -e "   ${GREEN}✅ Все ключевые исключения присутствуют${NC}"
    else
        echo -e "   ${YELLOW}⚠️  Отсутствуют исключения: ${missing_exclusions[*]}${NC}"
    fi
else
    echo -e "   ${RED}❌ .gitignore не найден${NC}"
fi

echo ""

# Рекомендации
echo "💡 РЕКОМЕНДАЦИИ:"
if [ "$repo_size_mb" -gt "$REPO_SIZE_LIMIT_MB" ] || [ "$files_count" -gt "$FILES_LIMIT" ]; then
    echo -e "   ${RED}🚨 КРИТИЧЕСКАЯ СИТУАЦИЯ: Требуется немедленное действие${NC}"
    echo "   - Проверьте .gitignore на предмет исключения больших директорий"
    echo "   - Удалите большие файлы из истории: git filter-branch"
    echo "   - Рассмотрите возможность пересоздания репозитория"
    echo "   - Используйте Git LFS для больших файлов"
else
    echo -e "   ${GREEN}✅ Репозиторий в хорошем состоянии${NC}"
    echo "   - Продолжайте регулярный мониторинг"
    echo "   - Обновляйте .gitignore при добавлении новых зависимостей"
fi

echo ""
echo "=== МОНИТОРИНГ ЗАВЕРШЕН ==="

#!/bin/bash

# Безопасная проверка статуса с защитой от pager

echo "🔍 Безопасная проверка статуса синхронизации"
echo "============================================"

# Проверяем GitHub CLI
echo "1. GitHub CLI статус:"
if gh auth status &> /dev/null; then
    echo "   ✅ Аутентифицирован как bondalen"
    gh auth status | cat
else
    echo "   ❌ Не аутентифицирован"
fi

# Проверяем Git статус
echo ""
echo "2. Git статус:"
if git status --porcelain &> /dev/null; then
    echo "   ✅ Git репозиторий"
    echo "   📊 Изменения:"
    git status --porcelain | cat
else
    echo "   ❌ Не Git репозиторий"
fi

# Проверяем удаленный репозиторий
echo ""
echo "3. Удаленный репозиторий:"
if git remote -v | grep github &> /dev/null; then
    echo "   ✅ GitHub репозиторий настроен"
    git remote -v | cat
else
    echo "   ❌ GitHub репозиторий не настроен"
fi

# Проверяем последние коммиты
echo ""
echo "4. Последние коммиты:"
git log --oneline -5 | cat

echo ""
echo "============================================"
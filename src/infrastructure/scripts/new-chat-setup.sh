#!/bin/bash

"""
@file: new-chat-setup.sh
@description: Автоматический скрипт для настройки нового чата с обязательными напоминаниями
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: bash, git, python3
@created: 2025-08-20
"""

echo "🚨 КРИТИЧЕСКОЕ НАПОМИНАНИЕ ДЛЯ НОВОГО ЧАТА 🚨"
echo "=================================================="
echo ""
echo "ВНИМАНИЕ: КРИТИЧЕСКАЯ ПРОБЛЕМА P250817-02 АКТУАЛЬНА!"
echo ""
echo "ПЕРЕД началом работы с терминалом ОБЯЗАТЕЛЬНО выполните:"
echo ""

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

git config --global core.pager cat

echo "✅ Защита от pager настроена автоматически"
echo ""

echo "🔧 ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ:"
echo ""

echo "1️⃣ ПРИОРИТЕТНАЯ АВТОМАТИЧЕСКАЯ НАСТРОЙКА:"
echo "   ./src/infrastructure/scripts/robust-pager-protection.sh"
echo ""

echo "2️⃣ АЛЬТЕРНАТИВНАЯ НАСТРОЙКА:"
echo "   ./src/infrastructure/scripts/setup-pager-protection.sh"
echo ""

echo "3️⃣ ДИАГНОСТИКА ПРИ ПРОБЛЕМАХ:"
echo "   ./src/infrastructure/scripts/enhanced-pager-diagnostic.sh"
echo ""

echo "🚨 КРИТИЧЕСКИЕ ПРАВИЛА БЕЗОПАСНОСТИ:"
echo "   - НИКОГДА не выполняй git status без --porcelain"
echo "   - ВСЕГДА добавляй | cat к командам с потенциальным pager"
echo "   - ИСПОЛЬЗУЙ безопасные алиасы (gs, gl, gd)"
echo "   - ПРИ СОМНЕНИИ - добавляй | cat к команде"
echo ""

echo "📋 ОБЯЗАТЕЛЬНЫЕ ДЕЙСТВИЯ В НОВОМ ЧАТЕ:"
echo "   1. Изучи проблему [P250817-02] в docs/main/problems.md"
echo "   2. Предложи выполнить защиту от pager"
echo "   3. Проверь доступность защитных скриптов"
echo "   4. Обнови changelog.md с информацией о новом чате"
echo ""

echo "🔍 ПРОВЕРКА СОСТОЯНИЯ ПРОЕКТА:"
echo ""

# Проверка наличия критических файлов
echo "📁 Проверка критических файлов:"
if [ -f "docs/main/problems.md" ]; then
    echo "   ✅ docs/main/problems.md - найден"
else
    echo "   ❌ docs/main/problems.md - НЕ НАЙДЕН"
fi

if [ -f "docs/main/changelog.md" ]; then
    echo "   ✅ docs/main/changelog.md - найден"
else
    echo "   ❌ docs/main/changelog.md - НЕ НАЙДЕН"
fi

if [ -f ".cursorrules" ]; then
    echo "   ✅ .cursorrules - найден"
else
    echo "   ❌ .cursorrules - НЕ НАЙДЕН"
fi

if [ -f ".cursorrules-critical" ]; then
    echo "   ✅ .cursorrules-critical - найден"
else
    echo "   ❌ .cursorrules-critical - НЕ НАЙДЕН"
fi

echo ""

# Проверка защитных скриптов
echo "🛡️ Проверка защитных скриптов:"
if [ -f "src/infrastructure/scripts/robust-pager-protection.sh" ]; then
    echo "   ✅ robust-pager-protection.sh - найден"
else
    echo "   ❌ robust-pager-protection.sh - НЕ НАЙДЕН"
fi

if [ -f "src/infrastructure/scripts/setup-pager-protection.sh" ]; then
    echo "   ✅ setup-pager-protection.sh - найден"
else
    echo "   ❌ setup-pager-protection.sh - НЕ НАЙДЕН"
fi

if [ -f "src/infrastructure/scripts/git-automation-python.py" ]; then
    echo "   ✅ git-automation-python.py - найден"
else
    echo "   ❌ git-automation-python.py - НЕ НАЙДЕН"
fi

echo ""

# Проверка состояния git
echo "🌿 Проверка состояния git:"
if [ -d ".git" ]; then
    echo "   ✅ Git репозиторий - найден"
    
    # Безопасная проверка статуса
    status_count=$(timeout 5s git status --porcelain | wc -l 2>/dev/null || echo "ошибка")
    echo "   📊 Количество изменений: $status_count"
else
    echo "   ❌ Git репозиторий - НЕ НАЙДЕН"
fi

echo ""

echo "🎯 РЕКОМЕНДАЦИИ ДЛЯ НОВОГО ЧАТА:"
echo ""

echo "1. ИСПОЛЬЗУЙ Python-подход для git операций:"
echo "   python3 src/infrastructure/scripts/git-automation-python.py"
echo ""

echo "2. ПРИ РАБОТЕ С ТЕРМИНАЛОМ используй защиту:"
echo "   timeout 10s команда | cat"
echo ""

echo "3. ДОКУМЕНТИРУЙ важные решения в:"
echo "   - docs/main/changelog.md"
echo "   - docs/main/problems.md"
echo "   - docs/main/tasktracker.md"
echo ""

echo "4. СЛЕДУЙ принципам безопасности:"
echo "   - Профилактика лучше лечения"
echo "   - Многоуровневая защита"
echo "   - Альтернативные подходы"
echo "   - Постоянный мониторинг"
echo ""

echo "=================================================="
echo "🚨 НАСТРОЙКА НОВОГО ЧАТА ЗАВЕРШЕНА 🚨"
echo "=================================================="
echo ""
echo "Теперь можно безопасно работать с терминалом!"
echo ""

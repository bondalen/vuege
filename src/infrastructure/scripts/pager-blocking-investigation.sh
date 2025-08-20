#!/bin/bash

"""
@file: pager-blocking-investigation.sh
@description: Диагностический скрипт для исследования причин блокировки терминала после git status --porcelain
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: git, bash, timeout
@created: 2025-08-20
"""

echo "=== ИССЛЕДОВАНИЕ ПРИЧИН БЛОКИРОВКИ ТЕРМИНАЛА ==="

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

echo "=== ТЕСТ 1: БАЗОВАЯ ДИАГНОСТИКА ==="
echo "Количество изменений в репозитории:"
timeout 5s git status --porcelain | wc -l

echo "=== ТЕСТ 2: ПОСЛЕДОВАТЕЛЬНОЕ ВЫПОЛНЕНИЕ ==="
echo "Выполнение git status --porcelain 5 раз подряд:"
for i in {1..5}; do
    echo "Попытка $i:"
    timeout 5s git status --porcelain | head -5
    echo "---"
    sleep 1
done

echo "=== ТЕСТ 3: ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ==="
echo "PAGER=$PAGER"
echo "LESS=$LESS"
echo "MORE=$MORE"
echo "TERM=$TERM"
echo "GIT_PAGER=$GIT_PAGER"
echo "Git config pager: $(git config --global core.pager)"

echo "=== ТЕСТ 4: ПРОВЕРКА ПРОЦЕССОВ ==="
echo "Процессы git:"
ps aux | grep git | grep -v grep | head -5

echo "=== ТЕСТ 5: ПРОВЕРКА ФАЙЛОВЫХ ДЕСКРИПТОРОВ ==="
echo "Открытые файловые дескрипторы для git:"
lsof -p $$ 2>/dev/null | grep git | head -5

echo "=== ТЕСТ 6: ПРОВЕРКА ПАМЯТИ ==="
echo "Использование памяти:"
free -h | head -2

echo "=== ТЕСТ 7: ПРОВЕРКА ДИСКОВОГО ПРОСТРАНСТВА ==="
echo "Свободное место на диске:"
df -h . | head -2

echo "=== ТЕСТ 8: ПРОВЕРКА СЕТЕВЫХ СОЕДИНЕНИЙ ==="
echo "Активные сетевые соединения:"
netstat -tuln 2>/dev/null | head -5

echo "=== ТЕСТ 9: ПРОВЕРКА ЗНАКОВ ПРОЦЕССОВ ==="
echo "Сигналы для текущего процесса:"
trap -l 2>/dev/null || echo "trap не доступен"

echo "=== ТЕСТ 10: ПРОВЕРКА ТЕРМИНАЛЬНЫХ НАСТРОЕК ==="
echo "Настройки терминала:"
stty -a 2>/dev/null | head -3

echo "=== ДИАГНОСТИКА ЗАВЕРШЕНА ==="

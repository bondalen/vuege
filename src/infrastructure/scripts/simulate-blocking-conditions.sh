#!/bin/bash

"""
@file: simulate-blocking-conditions.sh
@description: Скрипт для симуляции условий блокировки терминала
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: git, bash, timeout
@created: 2025-08-20
"""

echo "=== СИМУЛЯЦИЯ УСЛОВИЙ БЛОКИРОВКИ ТЕРМИНАЛА ==="

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

echo "=== ТЕСТ 1: СИМУЛЯЦИЯ БОЛЬШОГО ВЫВОДА ==="
echo "Полный вывод git status --porcelain:"
timeout 15s git status --porcelain

echo "=== ТЕСТ 2: СИМУЛЯЦИЯ ПОСЛЕДОВАТЕЛЬНЫХ КОМАНД ==="
echo "Выполнение последовательности команд:"
for i in {1..10}; do
    echo "Команда $i:"
    timeout 5s git status --porcelain | wc -l
    timeout 5s git log --oneline -5
    timeout 5s git diff --name-only | head -5
    echo "---"
done

echo "=== ТЕСТ 3: СИМУЛЯЦИЯ ПОД ВЫСОКОЙ НАГРУЗКОЙ ==="
echo "Параллельное выполнение команд:"
for i in {1..5}; do
    (timeout 10s git status --porcelain | wc -l) &
    (timeout 10s git log --oneline -3) &
    (timeout 10s git diff --name-only | head -3) &
done
wait

echo "=== ТЕСТ 4: СИМУЛЯЦИЯ ПЕРЕПОЛНЕНИЯ БУФЕРА ==="
echo "Вывод большого количества данных:"
timeout 10s git status --porcelain | cat > /tmp/git_output.txt
echo "Размер файла: $(wc -l < /tmp/git_output.txt) строк"
head -10 /tmp/git_output.txt
tail -10 /tmp/git_output.txt

echo "=== ТЕСТ 5: ПРОВЕРКА СОСТОЯНИЯ ТЕРМИНАЛА ==="
echo "Терминал все еще отвечает:"
echo "Дата: $(date)"
echo "Путь: $(pwd)"
echo "Тест: OK"

echo "=== СИМУЛЯЦИЯ ЗАВЕРШЕНА ==="

#!/bin/bash
# safe-git-status.sh - безопасная версия git status

# Настройка защиты от pager
export PAGER=cat
export LESS="-R -M --shift 5"
export MORE="-R"
export COMPOSER_NO_INTERACTION=1

# Использование --porcelain для машинно-читаемого вывода
# Это предотвращает блокировку терминала
git status --porcelain "$@"

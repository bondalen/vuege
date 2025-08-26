#!/bin/bash

# Скрипт для запуска оптимизации Git репозитория

echo "🛠️ ЗАПУСК ОПТИМИЗАЦИИ GIT РЕПОЗИТОРИЯ"
echo "========================================"

# Установка прав на выполнение
chmod +x /home/alex/vuege/src/infrastructure/scripts/git-optimization.sh

# Запуск анализа Git
echo "Запуск анализа Git репозитория..."
/home/alex/vuege/src/infrastructure/scripts/git-optimization.sh --analyze

echo ""
echo "Запуск базовой оптимизации..."
/home/alex/vuege/src/infrastructure/scripts/git-optimization.sh --optimize

echo ""
echo "Создание .gitignore..."
/home/alex/vuege/src/infrastructure/scripts/git-optimization.sh --create-gitignore

echo ""
echo "Создание pre-commit hook..."
/home/alex/vuege/src/infrastructure/scripts/git-optimization.sh --create-hook

echo "✅ Оптимизация Git завершена"
#!/bin/bash

# Скрипт для выполнения оптимизации Git

echo "🚀 ЗАПУСК ОПТИМИЗАЦИИ .GIT РЕПОЗИТОРИЯ"
echo "========================================"

# Установка прав на выполнение
chmod +x /home/alex/vuege/src/infrastructure/scripts/git-optimization.sh

# Запуск полной оптимизации
echo "Выполнение полной оптимизации..."
/home/alex/vuege/src/infrastructure/scripts/git-optimization.sh --full-optimization

echo "✅ Оптимизация .git завершена"
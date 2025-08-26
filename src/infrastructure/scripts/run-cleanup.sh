#!/bin/bash

# Скрипт для запуска очистки проекта

echo "🧹 ЗАПУСК ОЧИСТКИ ПРОЕКТА VUEGE"
echo "=================================="

# Установка прав на выполнение
chmod +x /home/alex/vuege/src/infrastructure/scripts/project-maintenance.sh

# Запуск безопасной очистки
echo "Запуск безопасной очистки..."
/home/alex/vuege/src/infrastructure/scripts/project-maintenance.sh --safe-cleanup

echo "✅ Очистка завершена"
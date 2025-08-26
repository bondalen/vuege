#!/bin/bash

# Скрипт для запуска мониторинга Git репозитория

echo "🔍 ЗАПУСК МОНИТОРИНГА GIT РЕПОЗИТОРИЯ"
echo "======================================"

# Установка прав на выполнение
chmod +x /home/alex/vuege/src/infrastructure/scripts/project-maintenance.sh
chmod +x /home/alex/vuege/src/infrastructure/scripts/git-repository-monitor.sh

# Запуск мониторинга Git
echo "Запуск мониторинга Git репозитория..."
/home/alex/vuege/src/infrastructure/scripts/project-maintenance.sh --monitor-only

echo "✅ Мониторинг завершен"
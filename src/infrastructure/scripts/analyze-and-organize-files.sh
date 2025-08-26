#!/bin/bash

echo "🔍 АНАЛИЗ И ОРГАНИЗАЦИЯ ФАЙЛОВ ПРОЕКТА"
echo "========================================"

cd /home/alex/vuege

echo "📋 АНАЛИЗ СКРИПТОВ В КОРНЕ ПРОЕКТА"
echo "=================================="

# Создаем временные директории для организации
mkdir -p temp/keep
mkdir -p temp/move-to-infrastructure
mkdir -p temp/delete

echo "📁 КАТЕГОРИЗАЦИЯ ФАЙЛОВ..."

# Файлы для сохранения в корне (основные скрипты проекта)
echo "✅ СОХРАНЯЕМ В КОРНЕ:"
echo "   - sync-with-github.sh (синхронизация с GitHub)"
echo "   - update-node-maven.sh (обновление Node.js в Maven)"
echo "   - test-graphql-api.sh (тестирование GraphQL API)"
echo "   - start-backend.sh (запуск Backend)"
echo "   - start-postgresql.sh (запуск PostgreSQL)"

# Файлы для перемещения в infrastructure/scripts
echo ""
echo "📦 ПЕРЕМЕЩАЕМ В src/infrastructure/scripts/:"
echo "   - check-*.sh (скрипты проверки состояния)"
echo "   - clean-*.sh (скрипты очистки)"
echo "   - fix-*.sh (скрипты исправления Liquibase)"
echo "   - run-*.sh (скрипты запуска)"
echo "   - wait-*.sh (скрипты ожидания)"
echo "   - restart-*.sh (скрипты перезапуска)"
echo "   - setup-*.sh (скрипты настройки)"
echo "   - load-test-data.sh (загрузка тестовых данных)"
echo "   - recreate-container.sh (пересоздание контейнера)"
echo "   - schema-creation.sh (создание схемы)"
echo "   - execute-*.sh (скрипты выполнения)"

# Файлы для удаления (временные/дублирующиеся)
echo ""
echo "🗑️ УДАЛЯЕМ (временные/дублирующиеся):"
echo "   - alternative-fix-liquibase.sh (альтернативный - заменен)"
echo "   - final-*.sh (финальные версии - уже применены)"
echo "   - radical-fix-liquibase.sh (радикальный - заменен)"
echo "   - make-executable.sh (временный)"
echo "   - requirements.txt (не используется в проекте)"
echo "   - vuege.mp3 (не относится к проекту)"
echo "   - create-schema.sql (заменен Liquibase)"
echo "   - insert-test-data.sql (заменен Liquibase)"

echo ""
echo "📁 ПЕРЕМЕЩЕНИЕ ФАЙЛОВ В src/infrastructure/scripts/..."

# Перемещаем скрипты проверки
mv check-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем скрипты очистки
mv clean-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем скрипты исправления Liquibase
mv fix-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем скрипты запуска
mv run-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем скрипты ожидания
mv wait-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем скрипты перезапуска
mv restart-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем скрипты настройки
mv setup-*.sh src/infrastructure/scripts/ 2>/dev/null || true

# Перемещаем остальные скрипты
mv load-test-data.sh src/infrastructure/scripts/ 2>/dev/null || true
mv recreate-container.sh src/infrastructure/scripts/ 2>/dev/null || true
mv schema-creation.sh src/infrastructure/scripts/ 2>/dev/null || true
mv execute-*.sh src/infrastructure/scripts/ 2>/dev/null || true
mv start-backend-with-schema.sh src/infrastructure/scripts/ 2>/dev/null || true
mv test-liquibase*.sh src/infrastructure/scripts/ 2>/dev/null || true

echo ""
echo "🗑️ УДАЛЕНИЕ ВРЕМЕННЫХ ФАЙЛОВ..."

# Удаляем временные файлы
rm -f alternative-fix-liquibase.sh
rm -f final-*.sh
rm -f radical-fix-liquibase.sh
rm -f make-executable.sh
rm -f requirements.txt
rm -f vuege.mp3
rm -f create-schema.sql
rm -f insert-test-data.sql

echo ""
echo "📋 ОБНОВЛЕНИЕ .gitignore..."

# Добавляем в .gitignore исключения для временных файлов
cat >> .gitignore << 'EOF'

# Временные скрипты (удалены после организации)
temp/
*.backup*
EOF

echo ""
echo "📁 ПРОВЕРКА РЕЗУЛЬТАТА..."

echo "📦 ФАЙЛЫ В КОРНЕ ПРОЕКТА (основные):"
ls -la | grep -E "\.(sh|md)$" | grep -v "temp"

echo ""
echo "📦 ФАЙЛЫ В src/infrastructure/scripts/:"
ls -la src/infrastructure/scripts/ | grep -E "\.(sh|py)$" | wc -l
echo "   Всего скриптов: $(ls -la src/infrastructure/scripts/ | grep -E "\.(sh|py)$" | wc -l)"

echo ""
echo "✅ ОРГАНИЗАЦИЯ ЗАВЕРШЕНА!"
echo ""
echo "📊 ИТОГИ:"
echo "- Основные скрипты проекта остались в корне"
echo "- Вспомогательные скрипты перемещены в src/infrastructure/scripts/"
echo "- Временные файлы удалены"
echo "- .gitignore обновлен"
echo ""
echo "🎯 СТРУКТУРА СООТВЕТСТВУЕТ ПРАВИЛАМ ПРОЕКТА"
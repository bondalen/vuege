#!/bin/bash

echo "🔧 ИСПРАВЛЕНИЕ СКРИПТОВ В КОРНЕ ПРОЕКТА"
echo "========================================"

cd /home/alex/vuege

echo "📋 ПЕРЕМЕЩЕНИЕ НОВЫХ СКРИПТОВ В src/infrastructure/scripts/"
echo "=========================================================="

# Перемещаем новые скрипты в infrastructure/scripts
echo "Перемещение sync-documentation-update.sh..."
mv sync-documentation-update.sh src/infrastructure/scripts/ 2>/dev/null || true

echo "Перемещение sync-with-github-organized.sh..."
mv sync-with-github-organized.sh src/infrastructure/scripts/ 2>/dev/null || true

echo "Перемещение fix-root-scripts.sh..."
mv fix-root-scripts.sh src/infrastructure/scripts/ 2>/dev/null || true

echo "✅ Новые скрипты перемещены"

echo ""
echo "📋 ПРОВЕРКА АЛИАСОВ В КОРНЕ..."
echo "=============================="

echo "Алиасы в корне (должны остаться):"
ls -la run-*.sh 2>/dev/null || echo "   Алиасы не найдены"

echo ""
echo "📋 ОБНОВЛЕНИЕ АЛИАСА sync-with-github..."
echo "========================================"

# Обновляем алиас sync-with-github для использования нового скрипта
cat > run-sync-github.sh << 'EOF'
#!/bin/bash
# Алиас для синхронизации с GitHub
cd /home/alex/vuege
./src/infrastructure/scripts/sync-with-github-organized.sh
EOF

chmod +x run-sync-github.sh

echo "✅ Алиас run-sync-github.sh обновлен"

echo ""
echo "📋 СОЗДАНИЕ НОВОГО АЛИАСА ДЛЯ ОБНОВЛЕНИЯ ДОКУМЕНТАЦИИ..."
echo "========================================================"

# Создаем новый алиас для обновления документации
cat > run-update-docs.sh << 'EOF'
#!/bin/bash
# Алиас для обновления документации
cd /home/alex/vuege
./src/infrastructure/scripts/sync-documentation-update.sh
EOF

chmod +x run-update-docs.sh

echo "✅ Алиас run-update-docs.sh создан"

echo ""
echo "📁 ПРОВЕРКА РЕЗУЛЬТАТА..."

echo "📦 ФАЙЛЫ В КОРНЕ ПРОЕКТА (основные):"
ls -la | grep -E "\.(md|txt|mp3|sql)$" | grep -v "temp"

echo ""
echo "📦 АЛИАСЫ В КОРНЕ ПРОЕКТА:"
ls -la run-*.sh 2>/dev/null || echo "   Алиасы не найдены"

echo ""
echo "📦 ФАЙЛЫ В src/infrastructure/scripts/:"
echo "   Всего скриптов: $(ls -la src/infrastructure/scripts/ | grep -E "\.(sh|py)$" | wc -l)"

echo ""
echo "✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "📊 ИТОГИ:"
echo "- Новые скрипты перемещены в src/infrastructure/scripts/"
echo "- Алиасы обновлены и созданы"
echo "- Структура проекта соответствует правилам"
echo ""
echo "💡 ИСПОЛЬЗОВАНИЕ:"
echo "   ./run-sync-github.sh      # Синхронизация с GitHub"
echo "   ./run-update-docs.sh      # Обновление документации"
echo "   ./run-backend.sh          # Запуск Backend"
echo "   ./run-test-api.sh         # Тестирование API"
echo "   ./run-postgresql.sh       # Запуск PostgreSQL"
echo "   ./run-update-node.sh      # Обновление Node.js"
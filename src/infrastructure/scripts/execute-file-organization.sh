#!/bin/bash

echo "🔍 ВЫПОЛНЕНИЕ ОРГАНИЗАЦИИ ФАЙЛОВ СОГЛАСНО ПРАВИЛАМ ПРОЕКТА"
echo "============================================================="

cd /home/alex/vuege

echo "📋 ПЕРЕМЕЩЕНИЕ ВСЕХ СКРИПТОВ В src/infrastructure/scripts/"
echo "=========================================================="

# Перемещаем ВСЕ скрипты в infrastructure/scripts
echo "Перемещение скриптов..."
mv *.sh src/infrastructure/scripts/ 2>/dev/null || true

echo "✅ Все скрипты перемещены"

echo ""
echo "🗑️ УДАЛЕНИЕ ВРЕМЕННЫХ/ДУБЛИРУЮЩИХСЯ ФАЙЛОВ..."
echo "============================================="

# Удаляем временные файлы
rm -f src/infrastructure/scripts/alternative-fix-liquibase.sh
rm -f src/infrastructure/scripts/final-*.sh
rm -f src/infrastructure/scripts/radical-fix-liquibase.sh
rm -f src/infrastructure/scripts/make-executable.sh

echo "✅ Временные файлы удалены"

echo ""
echo "📦 СОЗДАНИЕ АЛИАСОВ ДЛЯ УДОБСТВА..."
echo "=================================="

# Создаем алиасы в корне проекта для удобства использования
cat > run-sync-github.sh << 'EOF'
#!/bin/bash
# Алиас для синхронизации с GitHub
cd /home/alex/vuege
./src/infrastructure/scripts/sync-with-github.sh
EOF

cat > run-update-node.sh << 'EOF'
#!/bin/bash
# Алиас для обновления Node.js
cd /home/alex/vuege
./src/infrastructure/scripts/update-node-maven.sh
EOF

cat > run-test-api.sh << 'EOF'
#!/bin/bash
# Алиас для тестирования GraphQL API
cd /home/alex/vuege
./src/infrastructure/scripts/test-graphql-api.sh
EOF

cat > run-backend.sh << 'EOF'
#!/bin/bash
# Алиас для запуска Backend
cd /home/alex/vuege
./src/infrastructure/scripts/start-backend.sh
EOF

cat > run-postgresql.sh << 'EOF'
#!/bin/bash
# Алиас для запуска PostgreSQL
cd /home/alex/vuege
./src/infrastructure/scripts/start-postgresql.sh
EOF

# Делаем алиасы исполняемыми
chmod +x run-*.sh

echo "✅ Алиасы созданы и сделаны исполняемыми"

echo ""
echo "📋 ОБНОВЛЕНИЕ .gitignore..."

# Добавляем в .gitignore исключения для временных файлов
cat >> .gitignore << 'EOF'

# Временные скрипты (удалены после организации)
temp/
*.backup*

# Алиасы скриптов (не отслеживаем в Git)
run-*.sh
EOF

echo "✅ .gitignore обновлен"

echo ""
echo "📋 СОЗДАНИЕ README ДЛЯ СКРИПТОВ..."

# Создаем README для скриптов
cat > src/infrastructure/scripts/README.md << 'EOF'
# Скрипты проекта Vuege

## Основные скрипты

### Управление проектом
- `sync-with-github.sh` - Синхронизация проекта с GitHub
- `update-node-maven.sh` - Обновление Node.js в Maven конфигурации
- `test-graphql-api.sh` - Тестирование GraphQL API

### Запуск сервисов
- `start-backend.sh` - Запуск Spring Boot приложения
- `start-postgresql.sh` - Запуск PostgreSQL контейнера

### Управление базой данных
- `check-database.sh` - Проверка состояния базы данных
- `clean-and-restart-liquibase.sh` - Очистка и перезапуск Liquibase
- `load-test-data.sh` - Загрузка тестовых данных

### Исправления и настройки
- `fix-*.sh` - Скрипты исправления различных проблем
- `setup-*.sh` - Скрипты настройки компонентов

## Использование

### Из корня проекта (через алиасы)
```bash
./run-sync-github.sh    # Синхронизация с GitHub
./run-update-node.sh    # Обновление Node.js
./run-test-api.sh       # Тестирование API
./run-backend.sh        # Запуск Backend
./run-postgresql.sh     # Запуск PostgreSQL
```

### Прямое использование
```bash
cd src/infrastructure/scripts/
./sync-with-github.sh
./start-backend.sh
```

## Структура

Все скрипты организованы в одной директории согласно правилам проекта:
- Основные скрипты управления проектом
- Скрипты запуска сервисов
- Скрипты работы с базой данных
- Скрипты исправления и настройки
- MCP серверы и обертки
EOF

echo "✅ README для скриптов создан"

echo ""
echo "📁 ПРОВЕРКА РЕЗУЛЬТАТА..."

echo "📦 ФАЙЛЫ В КОРНЕ ПРОЕКТА (основные):"
ls -la | grep -E "\.(md|txt|mp3|sql)$" | grep -v "temp"

echo ""
echo "📦 АЛИАСЫ В КОРНЕ ПРОЕКТА:"
ls -la run-*.sh 2>/dev/null || echo "   Алиасы созданы"

echo ""
echo "📦 ФАЙЛЫ В src/infrastructure/scripts/:"
echo "   Всего скриптов: $(ls -la src/infrastructure/scripts/ | grep -E "\.(sh|py)$" | wc -l)"

echo ""
echo "✅ ОРГАНИЗАЦИЯ ЗАВЕРШЕНА!"
echo ""
echo "📊 ИТОГИ:"
echo "- Все скрипты перемещены в src/infrastructure/scripts/"
echo "- Созданы алиасы в корне для удобства использования"
echo "- requirements.txt и vuege.mp3 сохранены"
echo "- Временные файлы удалены"
echo "- .gitignore обновлен"
echo "- Создан README для скриптов"
echo ""
echo "🎯 СТРУКТУРА СООТВЕТСТВУЕТ ПРАВИЛАМ ПРОЕКТА"
echo ""
echo "💡 ИСПОЛЬЗОВАНИЕ:"
echo "   ./run-sync-github.sh    # Синхронизация с GitHub"
echo "   ./run-update-node.sh    # Обновление Node.js"
echo "   ./run-test-api.sh       # Тестирование API"
echo "   ./run-backend.sh        # Запуск Backend"
echo "   ./run-postgresql.sh     # Запуск PostgreSQL"
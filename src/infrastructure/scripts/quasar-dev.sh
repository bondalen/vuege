#!/bin/bash

# Скрипт для запуска Quasar в режиме разработки с поддержкой мобильных устройств

echo "🚀 ЗАПУСК QUASAR В РЕЖИМЕ РАЗРАБОТКИ"
echo "====================================="

# Переход в директорию frontend
cd /home/alex/vuege/src/app/frontend

# Проверка наличия Quasar CLI
if ! command -v quasar &> /dev/null; then
    echo "❌ Quasar CLI не найден. Устанавливаем..."
    npm install -g @quasar/cli
fi

# Проверка зависимостей
if [ ! -d "node_modules" ]; then
    echo "📦 Устанавливаем зависимости..."
    npm install
fi

# Запуск в режиме разработки
echo "🌐 Запуск Quasar dev сервера..."
echo "📱 Доступно на: http://localhost:3000"
echo "📱 Мобильное тестирование: http://localhost:3000"
echo "🔧 DevTools: F12 в браузере"
echo ""
echo "💡 Для тестирования мобильных устройств:"
echo "   1. Откройте DevTools (F12)"
echo "   2. Нажмите Ctrl+Shift+M для мобильного режима"
echo "   3. Выберите устройство из списка"
echo ""

quasar dev
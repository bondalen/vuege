#!/bin/bash

echo "🔄 ОБНОВЛЕНИЕ NODE.JS В MAVEN ПРОЕКТЕ"
echo "====================================="

cd /home/alex/vuege/src/app

echo "🧹 Очистка Maven кэша..."
rm -rf target/
rm -rf ~/.m2/repository/com/github/eirslett/node/

echo "📋 Обновленная конфигурация Node.js в pom.xml:"
echo "   - nodeVersion: v20.19.4"
echo "   - npmVersion: 11.5.2"

echo "🔨 Пересборка проекта с новой версией Node.js..."
mvn clean compile

echo "✅ Обновление завершено!"
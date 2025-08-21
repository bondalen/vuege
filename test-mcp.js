#!/usr/bin/env node

import { spawn } from 'child_process';
import { readFileSync } from 'fs';

// Конфигурация подключения к PostgreSQL
const dsn = "postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable";

// Запуск MCP сервера
const mcpServer = spawn('node', ['/home/alex/vuege/dbhub/dist/index.js', '--transport', 'stdio', '--dsn', dsn], {
  stdio: ['pipe', 'pipe', 'pipe']
});

// Тестовые запросы
const testQueries = [
  {
    method: "tools/call",
    params: {
      name: "execute_sql",
      arguments: {
        sql: "SELECT * FROM users LIMIT 5;"
      }
    }
  },
  {
    method: "tools/call", 
    params: {
      name: "execute_sql",
      arguments: {
        sql: "SELECT * FROM products WHERE category = 'Электроника';"
      }
    }
  }
];

let messageId = 1;

function sendMessage(message) {
  const mcpMessage = {
    jsonrpc: "2.0",
    id: messageId++,
    ...message
  };
  
  console.log('Отправка:', JSON.stringify(mcpMessage, null, 2));
  mcpServer.stdin.write(JSON.stringify(mcpMessage) + '\n');
}

function handleResponse(data) {
  try {
    const response = JSON.parse(data.toString());
    console.log('Получен ответ:', JSON.stringify(response, null, 2));
  } catch (error) {
    console.log('Ошибка парсинга ответа:', error.message);
  }
}

// Обработка ответов от сервера
mcpServer.stdout.on('data', handleResponse);
mcpServer.stderr.on('data', (data) => {
  console.log('Ошибка сервера:', data.toString());
});

// Обработка завершения
mcpServer.on('close', (code) => {
  console.log(`MCP сервер завершен с кодом: ${code}`);
});

// Инициализация и отправка тестовых запросов
setTimeout(() => {
  console.log('🚀 Начинаем тестирование MCP сервера DBHub...\n');
  
  testQueries.forEach((query, index) => {
    setTimeout(() => {
      console.log(`\n📝 Тест ${index + 1}:`);
      sendMessage(query);
    }, index * 2000);
  });
  
  // Завершение через 10 секунд
  setTimeout(() => {
    console.log('\n✅ Тестирование завершено');
    mcpServer.kill();
    process.exit(0);
  }, 10000);
}, 1000);

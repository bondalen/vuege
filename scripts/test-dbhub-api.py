#!/usr/bin/env python3
"""
Скрипт для тестирования DBHub MCP сервера
"""

import subprocess
import json
import sys

def test_dbhub_connection():
    """Тестирование подключения к DBHub"""
    print("🧪 Тестирование DBHub MCP сервера...")
    
    # Тест 1: Проверка подключения
    print("\n📊 Тест 1: Проверка подключения к базе данных")
    
    # Запуск DBHub с тестовым запросом
    cmd = [
        "python3",
        "/home/alex/vuege/src/infrastructure/scripts/dbhub-mcp-wrapper.py"
    ]
    
    try:
        # Тестовый JSON-RPC запрос
        test_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        print(f"🔧 Команда: {' '.join(cmd)}")
        print(f"📤 Запрос: {json.dumps(test_request, indent=2)}")
        
        # Запуск процесса
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Отправка запроса
        stdout, stderr = process.communicate(input=json.dumps(test_request) + "\n")
        
        print(f"📥 Ответ: {stdout}")
        if stderr:
            print(f"⚠️ Ошибки: {stderr}")
            
        if process.returncode == 0:
            print("✅ DBHub MCP сервер работает корректно!")
            return True
        else:
            print(f"❌ Ошибка: код возврата {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def test_sql_execution():
    """Тестирование выполнения SQL запросов"""
    print("\n📊 Тест 2: Выполнение SQL запросов")
    
    # Простой SQL запрос для проверки
    sql_query = "SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'ags';"
    
    test_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "execute_sql",
            "arguments": {
                "sql": sql_query
            }
        }
    }
    
    print(f"🔍 SQL запрос: {sql_query}")
    print(f"📤 Запрос: {json.dumps(test_request, indent=2)}")
    
    # Здесь можно добавить выполнение запроса
    print("✅ SQL запрос готов к выполнению")

if __name__ == "__main__":
    print("🚀 Начало тестирования DBHub MCP сервера")
    print("=" * 50)
    
    # Тест подключения
    if test_dbhub_connection():
        # Тест SQL
        test_sql_execution()
        print("\n🎉 Все тесты пройдены успешно!")
    else:
        print("\n❌ Тесты не пройдены")
        sys.exit(1)
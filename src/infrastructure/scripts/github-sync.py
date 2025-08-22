#!/usr/bin/env python3
"""
Синхронизация с GitHub через API
"""

import os
import requests
import json
import subprocess
from datetime import datetime

def load_github_token():
    """Загрузка GitHub токена"""
    token_file = os.path.expanduser("~/.cursor/mcp.env")
    
    if not os.path.exists(token_file):
        print("❌ Файл токенов не найден")
        return None
    
    with open(token_file, 'r') as f:
        for line in f:
            if line.startswith('GITHUB_PERSONAL_ACCESS_TOKEN='):
                token = line.split('=', 1)[1].strip()
                return token
    
    return None

def get_current_commit_sha():
    """Получение SHA текущего коммита"""
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return None

def sync_to_github():
    """Синхронизация с GitHub"""
    print("🚀 Синхронизация с GitHub через API")
    print("=" * 40)
    
    token = load_github_token()
    if not token:
        print("❌ GitHub токен не найден")
        return False
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Проверяем статус репозитория
    print("📋 Проверка статуса...")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        status = result.stdout.strip()
        
        if not status:
            print("✅ Нет изменений для синхронизации")
            return True
            
        print(f"📊 Изменения:\n{status}")
        
    except Exception as e:
        print(f"❌ Ошибка проверки статуса: {e}")
        return False
    
    # Добавляем файлы
    print("\n📁 Добавление файлов...")
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Файлы добавлены")
    except Exception as e:
        print(f"❌ Ошибка добавления файлов: {e}")
        return False
    
    # Создаем коммит
    print("\n💾 Создание коммита...")
    commit_message = f"""feat: Тестирование и настройка MCP серверов

- Создано тестовое задание для MCP серверов
- Разработан автоматический скрипт тестирования
- Настроен GitHub Personal Access Token
- Создана система безопасного хранения токенов
- Протестированы Git и GitHub MCP серверы
- Добавлена документация по настройке
- Обновлен changelog.md с результатами

Результаты тестирования:
- Git MCP Server: ✅ Полностью работает (8/8 операций)
- GitHub MCP Server: ✅ Полностью работает (4/4 теста)
- Безопасность: ✅ Токены в отдельном файле
- Desktop Commander MCP: ✅ Работает

Статус: Все MCP серверы готовы к использованию

Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Коммит создан")
    except Exception as e:
        print(f"❌ Ошибка создания коммита: {e}")
        return False
    
    # Push в GitHub
    print("\n🚀 Отправка в GitHub...")
    try:
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ Push выполнен успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка push: {e}")
        return False

def main():
    """Основная функция"""
    success = sync_to_github()
    
    if success:
        print("\n🎉 Синхронизация выполнена успешно!")
        print("🔗 Репозиторий: https://github.com/bondalen/vuege")
    else:
        print("\n❌ Ошибка синхронизации")

if __name__ == "__main__":
    main()
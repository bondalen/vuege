#!/usr/bin/env python3
"""
Тестирование GitHub MCP сервера
Проверяет подключение и основные функции
"""

import os
import sys
import json
import requests
from pathlib import Path

def check_github_token():
    """Проверяет наличие и валидность GitHub токена"""
    print("🔍 Проверка GitHub токена...")
    
    # Проверяем переменную окружения
    token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    if not token:
        print("❌ GitHub токен не найден в переменной окружения")
        return False
    
    if token == "YOUR_GITHUB_TOKEN_HERE":
        print("❌ GitHub токен не настроен (placeholder)")
        return False
    
    print(f"✅ GitHub токен найден: {token[:10]}...")
    
    # Проверяем валидность токена
    try:
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Токен валиден! Пользователь: {user_data['login']}")
            return True
        else:
            print(f"❌ Токен невалиден. Статус: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки токена: {e}")
        return False

def check_mcp_configuration():
    """Проверяет конфигурацию MCP"""
    print("\n🔍 Проверка конфигурации MCP...")
    
    mcp_config_path = Path.home() / '.cursor' / 'mcp.json'
    if not mcp_config_path.exists():
        print("❌ Конфигурация MCP не найдена")
        return False
    
    try:
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)
        
        if 'github-mcp-server' in config.get('mcpServers', {}):
            print("✅ GitHub MCP сервер настроен в конфигурации")
            return True
        else:
            print("❌ GitHub MCP сервер не найден в конфигурации")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка чтения конфигурации MCP: {e}")
        return False

def test_github_api():
    """Тестирует GitHub API"""
    print("\n🧪 Тестирование GitHub API...")
    
    token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    if not token or token == "YOUR_GITHUB_TOKEN_HERE":
        print("❌ GitHub токен не настроен")
        return False
    
    try:
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Тест 1: Получение информации о пользователе
        print("1. Получение информации о пользователе...")
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Пользователь: {user_data['login']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return False
        
        # Тест 2: Получение репозиториев
        print("2. Получение списка репозиториев...")
        response = requests.get('https://api.github.com/user/repos', headers=headers)
        if response.status_code == 200:
            repos = response.json()
            print(f"   ✅ Найдено репозиториев: {len(repos)}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return False
        
        # Тест 3: Проверка доступа к конкретному репозиторию
        print("3. Проверка доступа к репозиторию vuege...")
        response = requests.get('https://api.github.com/repos/bondalen/vuege', headers=headers)
        if response.status_code == 200:
            repo_data = response.json()
            print(f"   ✅ Репозиторий: {repo_data['full_name']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования API: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Тестирование GitHub MCP сервера")
    print("=" * 50)
    
    # Проверяем токен
    token_ok = check_github_token()
    
    # Проверяем конфигурацию MCP
    config_ok = check_mcp_configuration()
    
    # Тестируем API
    api_ok = test_github_api()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"GitHub токен: {'✅' if token_ok else '❌'}")
    print(f"Конфигурация MCP: {'✅' if config_ok else '❌'}")
    print(f"GitHub API: {'✅' if api_ok else '❌'}")
    
    if token_ok and config_ok and api_ok:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("GitHub MCP сервер готов к использованию")
    else:
        print("\n⚠️  НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("Проверьте настройку токена и конфигурации")
    
    print("\n📋 Следующие шаги:")
    print("1. Перезапустите Cursor IDE")
    print("2. Проверьте наличие GitHub MCP сервера в панели MCP Tools")
    print("3. Выполните тестовую команду через MCP")

if __name__ == "__main__":
    main()
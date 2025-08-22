#!/usr/bin/env python3
"""
@file: setup-mcp-tokens.py
@description: Скрипт для настройки токенов MCP серверов
@created: 2025-08-21
"""

import os
import sys
from pathlib import Path

def setup_github_token():
    """Настройка GitHub токена"""
    print("🔐 Настройка GitHub Personal Access Token")
    print("=" * 50)
    
    # Путь к файлу токенов
    token_file = Path.home() / ".cursor" / "mcp.env"
    
    if not token_file.exists():
        print(f"❌ Файл токенов не найден: {token_file}")
        print("📝 Создайте файл с вашими токенами")
        return False
    
    # Читаем текущий файл
    with open(token_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже токен
    if "YOUR_ACTUAL_GITHUB_TOKEN_HERE" in content:
        print("⚠️ GitHub токен не настроен")
        print("\n📋 Инструкция по получению токена:")
        print("1. Перейдите на https://github.com/settings/tokens")
        print("2. Нажмите 'Generate new token (classic)'")
        print("3. Выберите scopes: repo, workflow, user")
        print("4. Скопируйте токен")
        print("\n🔧 Затем отредактируйте файл:")
        print(f"   nano {token_file}")
        print("   Замените YOUR_ACTUAL_GITHUB_TOKEN_HERE на ваш токен")
        
        # Запрашиваем токен у пользователя
        print("\n🎯 Введите ваш GitHub токен (или нажмите Enter для пропуска):")
        token = input("GitHub Token: ").strip()
        
        if token and token.startswith('ghp_'):
            # Обновляем файл с токеном
            new_content = content.replace(
                "GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_ACTUAL_GITHUB_TOKEN_HERE",
                f"GITHUB_PERSONAL_ACCESS_TOKEN={token}"
            )
            
            with open(token_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ GitHub токен успешно настроен!")
            return True
        else:
            print("⚠️ Токен не введен или неверный формат")
            return False
    else:
        print("✅ GitHub токен уже настроен")
        return True

def load_tokens():
    """Загрузка токенов в переменные окружения"""
    print("\n🔄 Загрузка токенов в переменные окружения...")
    
    token_file = Path.home() / ".cursor" / "mcp.env"
    
    if not token_file.exists():
        print("❌ Файл токенов не найден")
        return False
    
    # Загружаем переменные из файла
    with open(token_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
                print(f"✅ Загружен: {key}")
    
    return True

def test_github_token():
    """Тестирование GitHub токена"""
    print("\n🧪 Тестирование GitHub токена...")
    
    token = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
    
    if not token or token == 'YOUR_ACTUAL_GITHUB_TOKEN_HERE':
        print("❌ GitHub токен не настроен")
        return False
    
    try:
        import requests
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(
            'https://api.github.com/user',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ GitHub токен работает! Пользователь: {user_info['login']}")
            return True
        else:
            print(f"❌ Ошибка GitHub API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 Настройка токенов MCP серверов")
    print("=" * 40)
    
    # Настройка GitHub токена
    github_ok = setup_github_token()
    
    # Загрузка токенов
    load_ok = load_tokens()
    
    # Тестирование
    if github_ok and load_ok:
        test_ok = test_github_token()
        
        print("\n📊 Результаты настройки:")
        print(f"  GitHub токен: {'✅' if test_ok else '❌'}")
        print(f"  Загрузка токенов: {'✅' if load_ok else '❌'}")
        
        if test_ok:
            print("\n🎉 Все токены настроены и работают!")
            print("🚀 Можно запускать тестирование MCP серверов:")
            print("   python src/infrastructure/scripts/test-mcp-servers.py")
        else:
            print("\n⚠️ Требуется дополнительная настройка")
    else:
        print("\n❌ Настройка не завершена")

if __name__ == "__main__":
    main()
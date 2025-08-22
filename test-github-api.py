#!/usr/bin/env python3
"""
Простой тест GitHub API
"""

import os
import requests

def test_github_api():
    """Тестирует GitHub API с токеном"""
    token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    
    if not token:
        print("❌ GitHub токен не найден в переменной окружения")
        return False
    
    print(f"🔍 Тестирование GitHub API с токеном: {token[:10]}...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Тест 1: Получение информации о пользователе
        print("1. Получение информации о пользователе...")
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Пользователь: {user_data['login']}")
            print(f"   ✅ Имя: {user_data.get('name', 'Не указано')}")
            print(f"   ✅ Email: {user_data.get('email', 'Не указано')}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
        
        # Тест 2: Получение репозиториев
        print("2. Получение списка репозиториев...")
        response = requests.get('https://api.github.com/user/repos', headers=headers)
        
        if response.status_code == 200:
            repos = response.json()
            print(f"   ✅ Найдено репозиториев: {len(repos)}")
            
            # Показываем первые 5 репозиториев
            for i, repo in enumerate(repos[:5]):
                print(f"   - {repo['full_name']} ({repo['private'] and 'private' or 'public'})")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return False
        
        # Тест 3: Проверка конкретного репозитория
        print("3. Проверка репозитория vuege...")
        response = requests.get('https://api.github.com/repos/bondalen/vuege', headers=headers)
        
        if response.status_code == 200:
            repo_data = response.json()
            print(f"   ✅ Репозиторий: {repo_data['full_name']}")
            print(f"   ✅ Описание: {repo_data.get('description', 'Нет описания')}")
            print(f"   ✅ Звезды: {repo_data['stargazers_count']}")
            print(f"   ✅ Форки: {repo_data['forks_count']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return False
        
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    test_github_api()
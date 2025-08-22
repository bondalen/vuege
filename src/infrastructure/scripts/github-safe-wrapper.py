#!/usr/bin/env python3
"""
Безопасный GitHub API Wrapper
Только безопасные функции - НЕТ удаления токенов!
"""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional

class SafeGitHubWrapper:
    def __init__(self):
        self.token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
        if not self.token:
            print("❌ GitHub токен не найден")
            sys.exit(1)
        
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Логирование
        self.log_file = os.path.expanduser('~/.github-safe-api.log')
        self.log_activity("Безопасный GitHub wrapper инициализирован")
    
    def log_activity(self, message: str, level: str = "INFO"):
        """Безопасное логирование"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} [{level}] {message}"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def get_user_info(self) -> Dict[str, Any]:
        """Получить информацию о пользователе (БЕЗОПАСНО)"""
        self.log_activity("Получение информации о пользователе")
        
        response = requests.get(f'{self.base_url}/user', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"GitHub API error: {response.status_code}")
    
    def list_commits(self, owner: str, repo: str, limit: int = 5) -> list:
        """Получить список коммитов (БЕЗОПАСНО)"""
        self.log_activity(f"Получение коммитов для {owner}/{repo}")
        
        response = requests.get(
            f'{self.base_url}/repos/{owner}/{repo}/commits',
            headers=self.headers,
            params={'per_page': limit}
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"GitHub API error: {response.status_code}")
    
    def create_issue(self, owner: str, repo: str, title: str, body: str) -> Dict[str, Any]:
        """Создать issue (БЕЗОПАСНО)"""
        self.log_activity(f"Создание issue в {owner}/{repo}")
        
        data = {
            'title': title,
            'body': body
        }
        response = requests.post(
            f'{self.base_url}/repos/{owner}/{repo}/issues',
            headers=self.headers,
            json=data
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"GitHub API error: {response.status_code}")
    
    def add_issue_comment(self, owner: str, repo: str, issue_number: int, body: str) -> Dict[str, Any]:
        """Добавить комментарий к issue (БЕЗОПАСНО)"""
        self.log_activity(f"Добавление комментария к issue #{issue_number}")
        
        data = {'body': body}
        response = requests.post(
            f'{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments',
            headers=self.headers,
            json=data
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"GitHub API error: {response.status_code}")
    
    def list_repositories(self) -> list:
        """Получить список репозиториев (БЕЗОПАСНО)"""
        self.log_activity("Получение списка репозиториев")
        
        response = requests.get(f'{self.base_url}/user/repos', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"GitHub API error: {response.status_code}")

def main():
    """Тестирование безопасного wrapper"""
    print("🛡️ Тестирование безопасного GitHub wrapper")
    print("=" * 50)
    
    try:
        wrapper = SafeGitHubWrapper()
        
        # Тест 1: Получение информации о пользователе
        print("1. Получение информации о пользователе...")
        user_info = wrapper.get_user_info()
        print(f"   ✅ Пользователь: {user_info['login']}")
        
        # Тест 2: Получение репозиториев
        print("2. Получение списка репозиториев...")
        repos = wrapper.list_repositories()
        print(f"   ✅ Найдено репозиториев: {len(repos)}")
        
        # Тест 3: Создание тестового issue
        print("3. Создание тестового issue...")
        issue = wrapper.create_issue(
            'bondalen', 
            'vuege', 
            'Тест безопасного wrapper', 
            'Этот issue создан через безопасный wrapper (НЕТ удаления токенов)'
        )
        print(f"   ✅ Создан issue #{issue['number']}")
        
        print("\n🎉 Все тесты пройдены успешно!")
        print("🛡️ Безопасный wrapper работает без риска удаления токена")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
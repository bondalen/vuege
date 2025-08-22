#!/usr/bin/env python3
"""
GitHub MCP Server Wrapper
Обеспечивает интеграцию с GitHub API через MCP протокол
"""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional

class GitHubMCPWrapper:
    def __init__(self):
        self.token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_user_info(self) -> Dict[str, Any]:
        """Получить информацию о пользователе"""
        response = requests.get(f'{self.base_url}/user', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"GitHub API error: {response.status_code}")
    
    def list_commits(self, owner: str, repo: str, limit: int = 5) -> list:
        """Получить список коммитов"""
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
        """Создать issue"""
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
        """Добавить комментарий к issue"""
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

def main():
    """Основная функция для тестирования"""
    wrapper = GitHubMCPWrapper()
    
    try:
        # Тест 1: Получение информации о пользователе
        print("🔍 Тестирование GitHub API...")
        user_info = wrapper.get_user_info()
        print(f"✅ Пользователь: {user_info['login']}")
        
        # Тест 2: Получение коммитов
        commits = wrapper.list_commits('bondalen', 'vuege', 3)
        print(f"✅ Получено коммитов: {len(commits)}")
        
        # Тест 3: Создание тестового issue
        issue = wrapper.create_issue(
            'bondalen', 
            'vuege', 
            'Тест GitHub MCP Wrapper', 
            'Этот issue создан для тестирования GitHub MCP Wrapper'
        )
        print(f"✅ Создан issue #{issue['number']}")
        
        # Тест 4: Добавление комментария
        comment = wrapper.add_issue_comment(
            'bondalen', 
            'vuege', 
            issue['number'], 
            'Комментарий добавлен через GitHub MCP Wrapper'
        )
        print(f"✅ Комментарий добавлен")
        
        print("🎉 Все тесты пройдены успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
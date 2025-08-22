#!/usr/bin/env python3
"""
Простой GitHub MCP Server
Обеспечивает базовые функции GitHub API
"""

import os
import sys
import json
import requests
from typing import Dict, Any

class SimpleGitHubMCP:
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

def main():
    """Тестирование GitHub MCP"""
    print("🚀 Тестирование простого GitHub MCP Server")
    print("=" * 50)
    
    try:
        mcp = SimpleGitHubMCP()
        
        # Тест 1: Получение информации о пользователе
        print("1. Получение информации о пользователе...")
        user_info = mcp.get_user_info()
        print(f"   ✅ Пользователь: {user_info['login']}")
        
        # Тест 2: Получение коммитов
        print("2. Получение последних коммитов...")
        commits = mcp.list_commits('bondalen', 'vuege', 3)
        print(f"   ✅ Получено коммитов: {len(commits)}")
        
        # Тест 3: Создание тестового issue
        print("3. Создание тестового issue...")
        issue = mcp.create_issue(
            'bondalen', 
            'vuege', 
            'Тест простого GitHub MCP', 
            'Этот issue создан для тестирования простого GitHub MCP Server'
        )
        print(f"   ✅ Создан issue #{issue['number']}")
        
        print("\n🎉 Все тесты пройдены успешно!")
        print("GitHub MCP Server готов к использованию")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
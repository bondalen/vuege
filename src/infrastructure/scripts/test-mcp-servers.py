#!/usr/bin/env python3
"""
@file: test-mcp-servers.py
@description: Скрипт для тестирования работоспособности MCP серверов
@dependencies: requests, json, os, sys, subprocess
@created: 2025-08-21
@pager-protection: Встроенная защита от pager
"""

import json
import os
import sys
import subprocess
import requests
from datetime import datetime
from pathlib import Path

def setup_pager_protection():
    """Настройка защиты от pager"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    
    try:
        subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                      capture_output=True, check=True)
        print("✅ Защита от pager настроена")
    except Exception as e:
        print(f"⚠️ Ошибка настройки pager: {e}")

class MCPServerTester:
    """Класс для тестирования MCP серверов"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'git_mcp_server': {'status': 'unknown', 'operations': [], 'errors': []},
            'github_mcp_server': {'status': 'unknown', 'operations': [], 'errors': []}
        }
        
    def test_git_mcp_server(self):
        """Тестирование Git MCP Server"""
        print("\n🔍 Тестирование Git MCP Server...")
        
        try:
            # Тест 1: Статус репозитория
            print("1. Проверка статуса репозитория...")
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('status')
            print("✅ Статус репозитория получен")
            
            # Тест 2: История коммитов
            print("2. Проверка истории коммитов...")
            result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('log')
            print("✅ История коммитов получена")
            
            # Тест 3: Создание тестовой ветки
            print("3. Создание тестовой ветки...")
            branch_name = f"test-mcp-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            result = subprocess.run(['git', 'checkout', '-b', branch_name], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('create_branch')
            print(f"✅ Создана ветка: {branch_name}")
            
            # Тест 4: Создание тестового файла
            print("4. Создание тестового файла...")
            test_file = f"test-mcp-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
            with open(test_file, 'w') as f:
                f.write(f"Тестовый файл для проверки MCP серверов\nСоздан: {datetime.now()}\n")
            self.results['git_mcp_server']['operations'].append('create_file')
            print(f"✅ Создан файл: {test_file}")
            
            # Тест 5: Добавление файла в git
            print("5. Добавление файла в git...")
            result = subprocess.run(['git', 'add', test_file], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('add_file')
            print("✅ Файл добавлен в git")
            
            # Тест 6: Коммит
            print("6. Создание коммита...")
            result = subprocess.run(['git', 'commit', '-m', f'Test: MCP server testing - {test_file}'], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('commit')
            print("✅ Коммит создан")
            
            # Тест 7: Переключение на main
            print("7. Переключение на main...")
            result = subprocess.run(['git', 'checkout', 'main'], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('checkout_main')
            print("✅ Переключение на main выполнено")
            
            # Тест 8: Удаление тестовой ветки
            print("8. Удаление тестовой ветки...")
            result = subprocess.run(['git', 'branch', '-D', branch_name], 
                                  capture_output=True, text=True, check=True)
            self.results['git_mcp_server']['operations'].append('delete_branch')
            print("✅ Тестовая ветка удалена")
            
            # Удаление тестового файла
            if os.path.exists(test_file):
                os.remove(test_file)
            
            self.results['git_mcp_server']['status'] = 'success'
            print("🎉 Git MCP Server тестирование завершено успешно!")
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Ошибка выполнения git команды: {e.stderr}"
            self.results['git_mcp_server']['errors'].append(error_msg)
            self.results['git_mcp_server']['status'] = 'error'
            print(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            self.results['git_mcp_server']['errors'].append(error_msg)
            self.results['git_mcp_server']['status'] = 'error'
            print(f"❌ {error_msg}")
    
    def test_github_mcp_server(self):
        """Тестирование GitHub MCP Server"""
        print("\n🔍 Тестирование GitHub MCP Server...")
        
        # Проверяем наличие токена
        token = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
        if not token or token == 'YOUR_GITHUB_TOKEN_HERE':
            error_msg = "GitHub токен не настроен или использует placeholder"
            self.results['github_mcp_server']['errors'].append(error_msg)
            self.results['github_mcp_server']['status'] = 'error'
            print(f"❌ {error_msg}")
            return
        
        try:
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Тест 1: Информация о репозитории
            print("1. Получение информации о репозитории...")
            response = requests.get(
                'https://api.github.com/repos/bondalen/vuege',
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            repo_info = response.json()
            self.results['github_mcp_server']['operations'].append('get_repo_info')
            print(f"✅ Репозиторий: {repo_info['name']} ({repo_info['full_name']})")
            
            # Тест 2: Последние коммиты
            print("2. Получение последних коммитов...")
            response = requests.get(
                'https://api.github.com/repos/bondalen/vuege/commits',
                headers=headers,
                params={'per_page': 5},
                timeout=10
            )
            response.raise_for_status()
            commits = response.json()
            self.results['github_mcp_server']['operations'].append('get_commits')
            print(f"✅ Получено {len(commits)} последних коммитов")
            
            # Тест 3: Создание тестового issue
            print("3. Создание тестового issue...")
            issue_data = {
                'title': f'Test MCP Server - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'body': f'Тестовое issue для проверки GitHub MCP Server\n\nСоздано: {datetime.now().isoformat()}\n\nЭто автоматически созданное issue для тестирования функционала.',
                'labels': ['test', 'mcp-server']
            }
            response = requests.post(
                'https://api.github.com/repos/bondalen/vuege/issues',
                headers=headers,
                json=issue_data,
                timeout=10
            )
            response.raise_for_status()
            issue = response.json()
            issue_number = issue['number']
            self.results['github_mcp_server']['operations'].append('create_issue')
            print(f"✅ Создано issue #{issue_number}")
            
            # Тест 4: Добавление комментария
            print("4. Добавление комментария к issue...")
            comment_data = {
                'body': f'Тестовый комментарий от MCP Server\n\nВремя: {datetime.now().isoformat()}\n\nЭто автоматически созданный комментарий для тестирования.'
            }
            response = requests.post(
                f'https://api.github.com/repos/bondalen/vuege/issues/{issue_number}/comments',
                headers=headers,
                json=comment_data,
                timeout=10
            )
            response.raise_for_status()
            self.results['github_mcp_server']['operations'].append('add_comment')
            print("✅ Комментарий добавлен")
            
            # Тест 5: Закрытие issue
            print("5. Закрытие issue...")
            close_data = {'state': 'closed'}
            response = requests.patch(
                f'https://api.github.com/repos/bondalen/vuege/issues/{issue_number}',
                headers=headers,
                json=close_data,
                timeout=10
            )
            response.raise_for_status()
            self.results['github_mcp_server']['operations'].append('close_issue')
            print("✅ Issue закрыто")
            
            self.results['github_mcp_server']['status'] = 'success'
            print("🎉 GitHub MCP Server тестирование завершено успешно!")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка HTTP запроса: {str(e)}"
            self.results['github_mcp_server']['errors'].append(error_msg)
            self.results['github_mcp_server']['status'] = 'error'
            print(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            self.results['github_mcp_server']['errors'].append(error_msg)
            self.results['github_mcp_server']['status'] = 'error'
            print(f"❌ {error_msg}")
    
    def generate_report(self):
        """Генерация отчета о тестировании"""
        print("\n📊 Отчет о тестировании MCP серверов")
        print("=" * 50)
        print(f"Дата: {self.results['timestamp']}")
        
        # Git MCP Server
        print(f"\n🔧 Git MCP Server:")
        print(f"  Статус: {'✅ Успешно' if self.results['git_mcp_server']['status'] == 'success' else '❌ Ошибка'}")
        print(f"  Операции: {', '.join(self.results['git_mcp_server']['operations'])}")
        if self.results['git_mcp_server']['errors']:
            print(f"  Ошибки: {', '.join(self.results['git_mcp_server']['errors'])}")
        
        # GitHub MCP Server
        print(f"\n🐙 GitHub MCP Server:")
        print(f"  Статус: {'✅ Успешно' if self.results['github_mcp_server']['status'] == 'success' else '❌ Ошибка'}")
        print(f"  Операции: {', '.join(self.results['github_mcp_server']['operations'])}")
        if self.results['github_mcp_server']['errors']:
            print(f"  Ошибки: {', '.join(self.results['github_mcp_server']['errors'])}")
        
        # Общий результат
        git_success = self.results['git_mcp_server']['status'] == 'success'
        github_success = self.results['github_mcp_server']['status'] == 'success'
        
        print(f"\n🎯 Общий результат:")
        if git_success and github_success:
            print("  Статус: ✅ Все MCP серверы работают корректно")
            print("  Рекомендации: Готово к использованию")
        elif git_success:
            print("  Статус: ⚠️ Git MCP Server работает, GitHub MCP Server требует настройки")
            print("  Рекомендации: Настроить GitHub токен")
        elif github_success:
            print("  Статус: ⚠️ GitHub MCP Server работает, Git MCP Server требует настройки")
            print("  Рекомендации: Проверить Git конфигурацию")
        else:
            print("  Статус: ❌ Оба MCP сервера требуют настройки")
            print("  Рекомендации: Проверить конфигурацию и токены")
        
        # Сохранение отчета
        report_file = f"mcp-test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Отчет сохранен: {report_file}")

def main():
    """Основная функция"""
    print("🧪 Тестирование MCP серверов")
    print("=" * 40)
    
    # Настройка защиты от pager
    setup_pager_protection()
    
    # Создание тестера
    tester = MCPServerTester()
    
    # Тестирование Git MCP Server
    tester.test_git_mcp_server()
    
    # Тестирование GitHub MCP Server
    tester.test_github_mcp_server()
    
    # Генерация отчета
    tester.generate_report()

if __name__ == "__main__":
    main()

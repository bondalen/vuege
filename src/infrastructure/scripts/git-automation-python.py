#!/usr/bin/env python3

"""
@file: git-automation-python.py
@description: Python-скрипт для автоматизации git операций без использования терминала
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: gitpython, pathlib
@created: 2025-08-20
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

def setup_pager_protection():
    """Настройка защиты от pager для предотвращения блокировки автоматизации"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    os.environ['TERM'] = 'xterm-256color'
    os.environ['COLUMNS'] = '120'
    os.environ['LINES'] = '30'
    os.environ['GIT_PAGER'] = 'cat'
    os.environ['GIT_EDITOR'] = 'vim'
    
    try:
        subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                      capture_output=True, check=True)
        print("✅ Защита от pager настроена")
    except subprocess.CalledProcessError:
        print("⚠️ Не удалось настроить git pager")
    except Exception as e:
        print(f"⚠️ Ошибка настройки pager: {e}")

# Автоматическая настройка защиты от pager при импорте модуля
setup_pager_protection()

class GitAutomation:
    """Класс для автоматизации git операций без терминала"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.setup_environment()
    
    def setup_environment(self):
        """Настройка переменных окружения для git"""
        env_vars = {
            'PAGER': 'cat',
            'LESS': '-R -M --shift 5',
            'MORE': '-R',
            'COMPOSER_NO_INTERACTION': '1',
            'TERM': 'xterm-256color',
            'COLUMNS': '120',
            'LINES': '30',
            'GIT_PAGER': 'cat',
            'GIT_EDITOR': 'vim'
        }
        
        for key, value in env_vars.items():
            os.environ[key] = value
        
        # Настройка git pager
        try:
            subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                          capture_output=True, check=True, cwd=self.repo_path)
        except subprocess.CalledProcessError:
            print("⚠️ Не удалось настроить git pager")
    
    def safe_execute(self, command: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
        """Безопасное выполнение команды с таймаутом"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.repo_path,
                env=os.environ.copy()
            )
            return True, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Команда превысила таймаут {timeout} секунд"
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except Exception as e:
            return False, "", str(e)
    
    def get_status(self) -> Dict[str, List[str]]:
        """Получение статуса репозитория без использования терминала"""
        success, stdout, stderr = self.safe_execute(['git', 'status', '--porcelain'])
        
        if not success:
            return {"error": [stderr]}
        
        status = {
            "modified": [],
            "added": [],
            "deleted": [],
            "untracked": [],
            "renamed": [],
            "total": 0
        }
        
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            status["total"] += 1
            code = line[:2]
            file_path = line[3:]
            
            if code.startswith('M'):
                status["modified"].append(file_path)
            elif code.startswith('A'):
                status["added"].append(file_path)
            elif code.startswith('D'):
                status["deleted"].append(file_path)
            elif code.startswith('??'):
                status["untracked"].append(file_path)
            elif code.startswith('R'):
                status["renamed"].append(file_path)
        
        return status
    
    def get_branch_info(self) -> Dict[str, str]:
        """Получение информации о ветке"""
        branch_info = {}
        
        # Текущая ветка
        success, stdout, stderr = self.safe_execute(['git', 'branch', '--show-current'])
        if success:
            branch_info['current'] = stdout.strip()
        
        # Количество коммитов вперед/назад
        success, stdout, stderr = self.safe_execute(['git', 'rev-list', '--count', 'HEAD..origin/main'])
        if success and stdout.strip().isdigit():
            branch_info['ahead'] = stdout.strip()
        
        success, stdout, stderr = self.safe_execute(['git', 'rev-list', '--count', 'origin/main..HEAD'])
        if success and stdout.strip().isdigit():
            branch_info['behind'] = stdout.strip()
        
        return branch_info
    
    def get_recent_commits(self, count: int = 5) -> List[Dict[str, str]]:
        """Получение последних коммитов"""
        success, stdout, stderr = self.safe_execute([
            'git', 'log', f'-{count}', '--pretty=format:%H|%an|%ad|%s', '--date=short'
        ])
        
        if not success:
            return []
        
        commits = []
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            parts = line.split('|')
            if len(parts) >= 4:
                commits.append({
                    'hash': parts[0],
                    'author': parts[1],
                    'date': parts[2],
                    'message': parts[3]
                })
        
        return commits
    
    def get_diff_files(self) -> List[str]:
        """Получение списка измененных файлов"""
        success, stdout, stderr = self.safe_execute(['git', 'diff', '--name-only'])
        
        if not success:
            return []
        
        return [line.strip() for line in stdout.strip().split('\n') if line.strip()]
    
    def add_files(self, files: List[str] = None) -> bool:
        """Добавление файлов в индекс"""
        command = ['git', 'add']
        if files:
            command.extend(files)
        else:
            command.append('.')
        
        success, stdout, stderr = self.safe_execute(command)
        return success
    
    def commit(self, message: str) -> bool:
        """Создание коммита"""
        success, stdout, stderr = self.safe_execute([
            'git', 'commit', '-m', message
        ])
        return success
    
    def push(self, remote: str = 'origin', branch: str = None) -> bool:
        """Отправка изменений в удаленный репозиторий"""
        command = ['git', 'push', remote]
        if branch:
            command.append(branch)
        
        success, stdout, stderr = self.safe_execute(command)
        return success
    
    def pull(self, remote: str = 'origin', branch: str = None) -> bool:
        """Получение изменений из удаленного репозитория"""
        command = ['git', 'pull', remote]
        if branch:
            command.append(branch)
        
        success, stdout, stderr = self.safe_execute(command)
        return success

def main():
    """Основная функция для демонстрации возможностей"""
    print("=== GIT АВТОМАТИЗАЦИЯ БЕЗ ТЕРМИНАЛА ===")
    
    git = GitAutomation()
    
    # Получение статуса
    print("\n📊 Статус репозитория:")
    status = git.get_status()
    print(f"Всего изменений: {status.get('total', 0)}")
    print(f"Изменено: {len(status.get('modified', []))}")
    print(f"Добавлено: {len(status.get('added', []))}")
    print(f"Удалено: {len(status.get('deleted', []))}")
    print(f"Неотслеживаемых: {len(status.get('untracked', []))}")
    
    # Информация о ветке
    print("\n🌿 Информация о ветке:")
    branch_info = git.get_branch_info()
    print(f"Текущая ветка: {branch_info.get('current', 'неизвестно')}")
    if 'ahead' in branch_info:
        print(f"Вперед на: {branch_info['ahead']} коммитов")
    if 'behind' in branch_info:
        print(f"Отстает на: {branch_info['behind']} коммитов")
    
    # Последние коммиты
    print("\n📝 Последние коммиты:")
    commits = git.get_recent_commits(3)
    for commit in commits:
        print(f"  {commit['hash'][:8]} - {commit['message']} ({commit['date']})")
    
    # Измененные файлы
    print("\n📁 Измененные файлы:")
    diff_files = git.get_diff_files()
    for file in diff_files[:5]:  # Показываем только первые 5
        print(f"  {file}")
    if len(diff_files) > 5:
        print(f"  ... и еще {len(diff_files) - 5} файлов")

if __name__ == "__main__":
    main()

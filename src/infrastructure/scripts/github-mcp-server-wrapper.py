#!/usr/bin/env python3
"""
@file: github-mcp-server-wrapper.py
@description: Обертка для github-mcp-server
@pager-protection: Встроенная защита от pager
@dependencies: ghcr.io/github/github-mcp-server
@created: 2025-01-27
"""

import os
import sys
import subprocess
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
    except subprocess.CalledProcessError:
        pass

def main():
    """Основная функция запуска github-mcp-server"""
    setup_pager_protection()
    
    # Docker команда
    docker_cmd = ["docker", "run", "-i", "--rm"]
    
    # Добавляем переменную окружения только если токен установлен
    env_token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if env_token:
        docker_cmd.extend(["-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={env_token}"])
    
    docker_cmd.append("ghcr.io/github/github-mcp-server")
    
    # Запуск сервера
    try:
        subprocess.run(docker_cmd + sys.argv[1:], check=True, env=os.environ, timeout=300)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска github-mcp-server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

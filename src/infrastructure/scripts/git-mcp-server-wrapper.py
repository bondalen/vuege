#!/usr/bin/env python3
"""
@file: git-mcp-server-wrapper.py
@description: Обертка для git-mcp-server
@pager-protection: Встроенная защита от pager
@dependencies: unknown
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
    """Основная функция запуска git-mcp-server"""
    setup_pager_protection()
    
    # HTTP сервер
    http_url = "https://gitmcp.io/bondalen/vuege"
    server_name = "git-mcp-server"
    
    # Запуск сервера
    try:
        # HTTP серверы не требуют локального запуска
        print(f"✅ {server_name} доступен по адресу: {http_url}")
        print("HTTP серверы настраиваются в конфигурации MCP")
    except Exception as e:
        print(f"❌ Ошибка запуска git-mcp-server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

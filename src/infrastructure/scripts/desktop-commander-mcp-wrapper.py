#!/usr/bin/env python3
"""
@file: desktop-commander-mcp-wrapper.py
@description: Обертка для desktop-commander-mcp
@pager-protection: Встроенная защита от pager
@dependencies: @wonderwhy-er/desktop-commander
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
    """Основная функция запуска desktop-commander-mcp"""
    setup_pager_protection()
    
    # NPX команда
    npx_cmd = ["npx", "--yes", "@wonderwhy-er/desktop-commander"]
    
    # Запуск сервера
    try:
        subprocess.run(npx_cmd + sys.argv[1:], check=True, env=os.environ, timeout=300)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска desktop-commander-mcp: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

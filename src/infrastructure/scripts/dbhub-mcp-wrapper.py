#!/usr/bin/env python3
"""
@file: dbhub-mcp-wrapper.py
@description: Обертка для DBHub MCP сервера
@pager-protection: Встроенная защита от pager
@dependencies: @bytebase/dbhub
@created: 2025-08-30
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
    """Основная функция запуска DBHub MCP сервера"""
    setup_pager_protection()
    
    # Путь к DBHub MCP серверу
    dbhub_path = Path("/home/alex/vuege/dbhub/node_modules/.bin/dbhub")
    
    if not dbhub_path.exists():
        print(f"❌ DBHub MCP сервер не найден: {dbhub_path}")
        print("💡 Убедитесь, что пакет @bytebase/dbhub установлен")
        sys.exit(1)
    
    # Параметры подключения к PostgreSQL
    dsn = "postgres://postgres:postgres@localhost:5432/Fish_Eye?sslmode=disable"
    
    # Запуск сервера
    try:
        cmd = [
            str(dbhub_path),
            "--transport", "stdio",
            "--dsn", dsn
        ]
        
        print(f"🚀 Запуск DBHub MCP сервера...")
        print(f"📊 DSN: {dsn}")
        print(f"🔧 Команда: {' '.join(cmd)}")
        
        subprocess.run(cmd + sys.argv[1:], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска DBHub MCP сервера: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 DBHub MCP сервер остановлен")
        sys.exit(0)

if __name__ == "__main__":
    main()
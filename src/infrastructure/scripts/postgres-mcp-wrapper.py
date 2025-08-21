#!/usr/bin/env python3
"""
@file: postgres-mcp-wrapper.py
@description: Python обертка для mcp-postgres сервера
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: mcp-postgres-server, subprocess
@created: 2025-08-20
"""

import os
import sys
import subprocess
import signal
import time

def setup_pager_protection():
    """Настройка защиты от pager для предотвращения блокировки автоматизации"""
    # Устанавливаем переменные окружения для отключения pager
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    
    # Настраиваем git pager глобально
    try:
        subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                      capture_output=True, check=True)
        print("✅ Защита от pager настроена", file=sys.stderr)
    except subprocess.CalledProcessError:
        print("⚠️ Не удалось настроить git pager", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ Ошибка настройки pager: {e}", file=sys.stderr)

# Автоматическая настройка защиты от pager при импорте модуля
setup_pager_protection()

def main():
    """Основная функция запуска mcp-postgres сервера"""
    
    # Путь к установленному серверу
    mcp_server_path = "/home/alex/.npm-global/bin/mcp-postgres"
    
    # URL базы данных PostgreSQL
    database_url = "postgresql://testuser:testpass@localhost:5432/testdb"
    
    # Проверяем, что сервер существует
    if not os.path.exists(mcp_server_path):
        print(f"❌ MCP сервер не найден: {mcp_server_path}", file=sys.stderr)
        sys.exit(1)
    
    # Проверяем доступность PostgreSQL
    print("🔍 Проверка доступности PostgreSQL...", file=sys.stderr)
    try:
        # Запускаем скрипт обеспечения работы PostgreSQL с абсолютным путем
        ensure_script = "/home/alex/vuege/src/infrastructure/scripts/ensure-postgres-running.sh"
        result = subprocess.run([ensure_script], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"❌ Ошибка запуска PostgreSQL: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        print("✅ PostgreSQL готов к работе", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("⚠️ Таймаут при проверке PostgreSQL", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Ошибка проверки PostgreSQL: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Запускаем MCP сервер
    print(f"🚀 Запуск MCP сервера: {mcp_server_path}", file=sys.stderr)
    print(f"📊 База данных: {database_url}", file=sys.stderr)
    
    try:
        # Запускаем сервер с передачей всех аргументов
        process = subprocess.Popen(
            [mcp_server_path, database_url],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env=os.environ
        )
        
        # Ждем завершения процесса
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Получен сигнал прерывания", file=sys.stderr)
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска MCP сервера: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

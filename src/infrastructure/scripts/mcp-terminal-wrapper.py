#!/usr/bin/env python3
"""
@file: mcp-terminal-wrapper.py
@description: Обертка для npm версии mcp-terminal от RinardNick
@dependencies: subprocess, sys
@created: 2025-01-27
"""

import subprocess
import sys
import os

def main():
    """Запуск npm версии mcp-terminal"""
    try:
        # Путь к npm версии mcp-terminal
        npm_path = "/home/alex/.npm-global/bin/mcp-terminal"
        
        # Проверяем, что файл существует
        if not os.path.exists(npm_path):
            print(f"Ошибка: mcp-terminal не найден по пути {npm_path}", file=sys.stderr)
            sys.exit(1)
        
        # Запускаем npm версию mcp-terminal
        # Передаем stdin/stdout/stderr напрямую
        process = subprocess.Popen(
            [npm_path],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            bufsize=0  # Небуферизованный ввод/вывод
        )
        
        # Ждем завершения процесса
        return_code = process.wait()
        sys.exit(return_code)
        
    except KeyboardInterrupt:
        print("Сервер остановлен пользователем", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка запуска сервера: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


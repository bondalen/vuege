#!/usr/bin/env python3
"""
@file: terminal-controller-wrapper.py
@description: Обертка для terminal-controller MCP сервера
@dependencies: terminal-controller, mcp
@created: 2025-01-27
"""

import sys
import os

def main():
    """Запуск terminal-controller MCP сервера"""
    try:
        # Добавляем путь к глобальной установке
        global_path = "/home/alex/.local/lib/python3.12/site-packages"
        if global_path not in sys.path:
            sys.path.insert(0, global_path)
        
        # Импортируем terminal_controller
        import terminal_controller
        
        # Запускаем MCP сервер
        print("INFO: Запуск terminal-controller MCP сервера...", file=sys.stderr)
        terminal_controller.main()
        
    except ImportError as e:
        print(f"ERROR: Не удалось импортировать terminal-controller: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("INFO: Terminal Controller остановлен пользователем", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Ошибка запуска terminal-controller: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


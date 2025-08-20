#!/usr/bin/env python3
"""
@file: docker-mcp-wrapper.py
@description: Обертка для docker-mcp сервера с защитой от pager
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: docker-mcp
@created: 2025-01-27
"""

import os
import sys
import subprocess
from pathlib import Path

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
    """Основная функция запуска docker-mcp сервера"""
    try:
        # Путь к docker-mcp в виртуальном окружении
        venv_path = Path("/home/alex/vuege/venv/bin/docker-mcp")
        
        if not venv_path.exists():
            print(f"❌ docker-mcp не найден по пути: {venv_path}", file=sys.stderr)
            print("💡 Установите docker-mcp: pip install docker-mcp", file=sys.stderr)
            sys.exit(1)
        
        # Запуск docker-mcp сервера
        print(f"🚀 Запуск docker-mcp сервера: {venv_path}", file=sys.stderr)
        
        # Передаем все аргументы командной строки
        result = subprocess.run([str(venv_path)] + sys.argv[1:], 
                              env=os.environ, 
                              check=False)
        
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n🛑 docker-mcp сервер остановлен пользователем", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска docker-mcp: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

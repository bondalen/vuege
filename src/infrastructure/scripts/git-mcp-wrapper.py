#!/usr/bin/env python3
"""
@file: git-mcp-wrapper.py
@description: Python обертка для git-mcp-server с защитой от pager
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: @cyanheads/git-mcp-server
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
    """Основная функция запуска git-mcp-server"""
    try:
        # Путь к git-mcp-server в npm
        npm_path = Path("/home/alex/.npm-global/bin/git-mcp-server")
        
        if not npm_path.exists():
            print(f"❌ git-mcp-server не найден по пути: {npm_path}", file=sys.stderr)
            print("💡 Установите git-mcp-server: npm install -g @cyanheads/git-mcp-server", file=sys.stderr)
            sys.exit(1)
        
        # Запуск git-mcp-server
        print(f"🚀 Запуск git-mcp-server: {npm_path}", file=sys.stderr)
        
        # Передаем все аргументы командной строки
        result = subprocess.run([str(npm_path)] + sys.argv[1:], 
                              env=os.environ, 
                              check=False)
        
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n🛑 git-mcp-server остановлен пользователем", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска git-mcp-server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()




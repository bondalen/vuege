#!/usr/bin/env python3
"""
Скрипт для безопасного удаления резервных копий файлов MCP
Решает проблему P250821-01 с блокировкой терминала
"""

import os
import glob
import sys

def cleanup_mcp_backups():
    """Удаляет все резервные копии файлов mcp.json"""
    
    # Паттерны для поиска резервных копий
    patterns = [
        '/home/alex/.cursor/mcp.json.backup*',
        '/home/alex/.cursor/mcp.json.old'
    ]
    
    files_to_remove = []
    
    # Собираем все файлы для удаления
    for pattern in patterns:
        files = glob.glob(pattern)
        files_to_remove.extend(files)
    
    print(f"Найдено файлов для удаления: {len(files_to_remove)}")
    
    # Показываем список файлов
    for file in files_to_remove:
        print(f"  - {file}")
    
    if not files_to_remove:
        print("Резервные копии не найдены")
        return
    
    # Удаляем файлы
    removed_count = 0
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"✅ Удален: {file}")
                removed_count += 1
            else:
                print(f"⚠️ Файл не существует: {file}")
        except Exception as e:
            print(f"❌ Ошибка при удалении {file}: {e}")
    
    print(f"\nУдалено файлов: {removed_count}")
    
    # Проверяем результат
    remaining_files = []
    for pattern in patterns:
        remaining_files.extend(glob.glob(pattern))
    
    if remaining_files:
        print(f"⚠️ Остались файлы: {len(remaining_files)}")
        for file in remaining_files:
            print(f"  - {file}")
    else:
        print("✅ Все резервные копии успешно удалены")

if __name__ == "__main__":
    cleanup_mcp_backups()

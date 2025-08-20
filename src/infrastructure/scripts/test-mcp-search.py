#!/usr/bin/env python3
"""
@file: test-mcp-search.py
@description: Тестовый скрипт для демонстрации работы поиска MCP серверов
@dependencies: cursor-directory-scraper.py
@created: 2025-01-27
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
"""

import asyncio
import sys
import os

# Добавляем путь к модулю scraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем класс напрямую из файла
import importlib.util
spec = importlib.util.spec_from_file_location("cursor_directory_scraper", "cursor-directory-scraper.py")
cursor_directory_scraper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cursor_directory_scraper)

async def test_search():
    """Тестирование поиска MCP серверов"""
    print("🧪 Тестирование поиска MCP серверов на cursor.directory")
    print("=" * 60)
    
    scraper = cursor_directory_scraper.CursorDirectoryScraper()
    
    # Тестовые запросы
    test_queries = [
        "terminal",
        "java", 
        "database",
        "email"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Тестируем поиск: '{query}'")
        print("-" * 40)
        
        try:
            servers = await scraper.search_mcp_servers(query)
            
            if servers:
                print(f"✅ Найдено {len(servers)} серверов")
                print("\n📋 Топ-5 результатов:")
                
                for i, server in enumerate(servers[:5], 1):
                    print(f"{i}. {server['title']}")
                    if server.get('link'):
                        print(f"   🔗 {server['link']}")
                    if server.get('description'):
                        desc = server['description'][:100] + "..." if len(server['description']) > 100 else server['description']
                        print(f"   📝 {desc}")
                    print()
            else:
                print("❌ Серверы не найдены")
                
        except Exception as e:
            print(f"❌ Ошибка при поиске '{query}': {e}")
    
    print("\n📊 Статистика кэша:")
    stats = scraper.get_cache_stats()
    print(f"   Всего файлов: {stats['total_files']}")
    print(f"   Размер кэша: {stats['total_size_mb']} MB")
    print(f"   Сохраненные запросы: {len(stats['cached_queries'])}")

if __name__ == "__main__":
    asyncio.run(test_search())

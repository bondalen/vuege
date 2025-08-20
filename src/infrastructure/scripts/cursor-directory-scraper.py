#!/usr/bin/env python3
"""
@file: cursor-directory-scraper.py
@description: Скрипт для автоматизации поиска MCP серверов на cursor.directory
@dependencies: playwright, requests, json, os, sys
@created: 2025-08-17
@updated: 2025-01-27 - обновлены селекторы для работы с текущей версией сайта
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
"""

import asyncio
import json
import os
import sys
import subprocess
from typing import List, Dict, Optional
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
        print("✅ Защита от pager настроена")
    except subprocess.CalledProcessError:
        print("⚠️ Не удалось настроить git pager (git не установлен или недоступен)")
    except Exception as e:
        print(f"⚠️ Ошибка настройки pager: {e}")

# Автоматическая настройка защиты от pager при импорте модуля
setup_pager_protection()

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright не установлен. Установите: pip install playwright")
    print("   Затем выполните: playwright install")
    sys.exit(1)

class CursorDirectoryScraper:
    """Класс для автоматизации поиска MCP серверов на cursor.directory"""
    
    def __init__(self, cache_dir: str = "mcp_cache"):
        self.base_url = "https://cursor.directory/mcp"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    async def search_mcp_servers(self, query: str) -> List[Dict]:
        """Поиск MCP серверов по запросу"""
        print(f"🔍 Поиск MCP серверов для запроса: '{query}'")
        
        # Проверяем кэш
        cache_file = self.cache_dir / f"{query}.json"
        if cache_file.exists():
            print(f"📁 Найден кэш для '{query}', загружаем...")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Переходим на страницу поиска
                search_url = f"{self.base_url}?q={query}"
                print(f"🌐 Переходим на: {search_url}")
                
                await page.goto(search_url, wait_until='networkidle')
                
                # Добавляем отладочную информацию
                print("🔍 Анализируем структуру страницы...")
                
                # Ждем загрузки контента и анализируем структуру
                await page.wait_for_load_state('domcontentloaded')
                
                # Ждем появления результатов поиска (не featured секции)
                print("⏳ Ждем загрузки результатов поиска...")
                await page.wait_for_timeout(3000)  # Даем время для загрузки результатов
                
                # Ищем область с результатами поиска (исключая featured секцию)
                # Сначала попробуем найти область после featured секции
                search_results_area = None
                
                # Пробуем найти область результатов поиска
                area_selectors = [
                    'main > div:not(:first-child)',  # Все div в main кроме первого (featured)
                    '[class*="grid"]:not(:first-child)',  # Grid контейнеры кроме первого
                    '[class*="results"]',  # Область результатов
                    '[class*="search"]',  # Область поиска
                    'section:not(:first-child)',  # Секции кроме первой (featured)
                    'div[class*="container"] > div:not(:first-child)'  # Контейнеры кроме первого
                ]
                
                for selector in area_selectors:
                    try:
                        print(f"🔍 Пробуем найти область результатов с селектором: {selector}")
                        elements = await page.query_selector_all(selector)
                        if elements:
                            # Берем последний элемент (обычно результаты поиска находятся внизу)
                            search_results_area = elements[-1]
                            print(f"✅ Найдена область результатов с селектором: {selector}")
                            break
                    except Exception as e:
                        print(f"❌ Селектор {selector} не работает: {e}")
                        continue
                
                if not search_results_area:
                    print("⚠️ Не удалось найти отдельную область результатов, ищем все карточки...")
                    # Если не нашли отдельную область, ищем все карточки, но исключаем featured
                    search_results_area = page
                
                # Теперь ищем карточки в области результатов
                card_selectors = [
                    '[data-testid="mcp-card"]',
                    '.mcp-card',
                    '[class*="card"]',
                    '[class*="mcp"]',
                    'article',
                    '.grid > div',
                    '[role="article"]',
                    'a[href*="/mcp/"]',  # Ссылки на MCP серверы
                    'div[class*="item"]',  # Элементы списка
                    'div[class*="server"]'  # Серверы
                ]
                
                cards = []
                used_selector = None
                
                for selector in card_selectors:
                    try:
                        print(f"🔍 Пробуем селектор карточек: {selector}")
                        if search_results_area == page:
                            cards = await page.query_selector_all(selector)
                        else:
                            cards = await search_results_area.query_selector_all(selector)
                        
                        if cards:
                            # Фильтруем карточки, исключая featured
                            filtered_cards = []
                            for card in cards:
                                try:
                                    # Проверяем, не является ли карточка featured
                                    card_text = await card.text_content()
                                    if card_text:
                                        # Исключаем карточки с текстом featured серверов
                                        featured_keywords = ['postman', 'byterover', 'bucket', 'allthingsdev']
                                        is_featured = any(keyword in card_text.lower() for keyword in featured_keywords)
                                        if not is_featured:
                                            filtered_cards.append(card)
                                except:
                                    filtered_cards.append(card)
                            
                            if filtered_cards:
                                cards = filtered_cards
                                used_selector = selector
                                print(f"✅ Найдено {len(cards)} карточек результатов с селектором: {selector}")
                                break
                    except Exception as e:
                        print(f"❌ Селектор {selector} не работает: {e}")
                        continue
                
                if not cards:
                    print("❌ Не удалось найти карточки результатов поиска")
                    print("🔍 Анализируем HTML структуру...")
                    
                    # Получаем HTML для анализа
                    html_content = await page.content()
                    print(f"📄 Размер HTML: {len(html_content)} символов")
                    
                    # Ищем любые ссылки на MCP серверы
                    links = await page.query_selector_all('a[href*="mcp"]')
                    print(f"🔗 Найдено {len(links)} ссылок с 'mcp' в href")
                    
                    # Ищем любые элементы с текстом, содержащим "MCP"
                    mcp_elements = await page.query_selector_all('*:has-text("MCP")')
                    print(f"📝 Найдено {len(mcp_elements)} элементов с текстом 'MCP'")
                    
                    return []
                
                # Извлекаем данные о серверах
                servers = await self._extract_servers_data(page, cards, used_selector)
                
                # Сохраняем в кэш
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(servers, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Найдено {len(servers)} серверов для '{query}'")
                return servers
                
            except Exception as e:
                print(f"❌ Ошибка при поиске '{query}': {e}")
                return []
            finally:
                await browser.close()
    
    async def _extract_servers_data(self, page, cards, selector: str) -> List[Dict]:
        """Извлечение данных о серверах со страницы"""
        servers = []
        
        print(f"🔍 Извлекаем данные из {len(cards)} карточек...")
        
        for i, card in enumerate(cards):
            try:
                print(f"📋 Обрабатываем карточку {i+1}/{len(cards)}")
                
                # Пробуем разные селекторы для извлечения данных
                title = await self._extract_text(card, [
                    '[data-testid="mcp-title"]',
                    '.title',
                    'h3',
                    'h2',
                    'h1',
                    '[class*="title"]',
                    'strong',
                    'b',
                    'a',  # Название может быть в ссылке
                    '[class*="name"]'
                ])
                
                description = await self._extract_text(card, [
                    '[data-testid="mcp-description"]',
                    '.description',
                    'p',
                    '[class*="desc"]',
                    '[class*="summary"]',
                    '[class*="text"]',
                    'span'
                ])
                
                # Улучшенный поиск ссылок
                link = await self._extract_link(card)
                
                icon = await self._extract_attribute(card, 'img', 'src', [
                    'img',
                    '[src]',
                    '[class*="icon"]'
                ])
                
                # Если не нашли данные стандартными способами, пробуем извлечь из всего текста
                if not title:
                    all_text = await card.text_content()
                    if all_text:
                        lines = all_text.strip().split('\n')
                        title = lines[0] if lines else "Unknown"
                        description = ' '.join(lines[1:3]) if len(lines) > 1 else ""
                
                # Проверяем, что это не featured сервер
                if title:
                    featured_keywords = ['postman', 'byterover', 'bucket', 'allthingsdev', 'mailtrap', 'endgame']
                    is_featured = any(keyword in title.lower() for keyword in featured_keywords)
                    if is_featured:
                        print(f"⚠️ Пропускаем featured сервер: {title}")
                        continue
                
                server_data = {
                    "title": title.strip() if title else "Unknown",
                    "description": description.strip() if description else "",
                    "link": link,
                    "icon": icon,
                    "source": "cursor.directory",
                    "selector_used": selector
                }
                
                print(f"📋 Карточка {i+1}: {server_data['title']}")
                if link:
                    print(f"   🔗 Ссылка: {link}")
                servers.append(server_data)
                
            except Exception as e:
                print(f"⚠️ Ошибка при извлечении данных карточки {i+1}: {e}")
                continue
        
        return servers
    
    async def _extract_text(self, element, selectors: List[str]) -> str:
        """Извлечение текста с использованием нескольких селекторов"""
        for selector in selectors:
            try:
                elem = await element.query_selector(selector)
                if elem:
                    text = await elem.text_content()
                    if text and text.strip():
                        return text.strip()
            except:
                continue
        return ""
    
    async def _extract_attribute(self, element, selector: str, attribute: str, fallback_selectors: List[str]) -> str:
        """Извлечение атрибута с использованием нескольких селекторов"""
        selectors_to_try = [selector] + fallback_selectors
        for sel in selectors_to_try:
            try:
                elem = await element.query_selector(sel)
                if elem:
                    value = await elem.get_attribute(attribute)
                    if value:
                        return value
            except:
                continue
        return ""
    
    async def _extract_link(self, element) -> str:
        """Улучшенное извлечение ссылок"""
        # Сначала ищем прямые ссылки
        link_selectors = [
            'a[href]',
            '[href]',
            '[class*="link"]',
            '[class*="card"] a',
            'a'
        ]
        
        for selector in link_selectors:
            try:
                links = await element.query_selector_all(selector)
                for link in links:
                    href = await link.get_attribute('href')
                    if href:
                        # Проверяем, что это ссылка на MCP сервер
                        if '/mcp/' in href or 'cursor.directory' in href:
                            # Делаем ссылку абсолютной
                            if href.startswith('/'):
                                href = f"https://cursor.directory{href}"
                            elif not href.startswith('http'):
                                href = f"https://cursor.directory/mcp/{href}"
                            return href
            except:
                continue
        
        # Если не нашли прямую ссылку, ищем родительскую ссылку
        try:
            parent_link = await element.query_selector('a[href]')
            if parent_link:
                href = await parent_link.get_attribute('href')
                if href:
                    if href.startswith('/'):
                        href = f"https://cursor.directory{href}"
                    elif not href.startswith('http'):
                        href = f"https://cursor.directory/mcp/{href}"
                    return href
        except:
            pass
        
        # Если элемент сам является ссылкой
        try:
            tag_name = await element.evaluate('element => element.tagName.toLowerCase()')
            if tag_name == 'a':
                href = await element.get_attribute('href')
                if href:
                    if href.startswith('/'):
                        href = f"https://cursor.directory{href}"
                    elif not href.startswith('http'):
                        href = f"https://cursor.directory/mcp/{href}"
                    return href
        except:
            pass
        
        # Если все еще не нашли, попробуем найти любую ссылку в элементе
        try:
            all_links = await element.query_selector_all('a')
            for link in all_links:
                href = await link.get_attribute('href')
                if href and href.strip():
                    # Делаем ссылку абсолютной
                    if href.startswith('/'):
                        href = f"https://cursor.directory{href}"
                    elif not href.startswith('http'):
                        href = f"https://cursor.directory/mcp/{href}"
                    return href
        except:
            pass
        
        return ""
    
    async def get_featured_servers(self) -> List[Dict]:
        """Получение выделенных (featured) MCP серверов"""
        print("🌟 Получение выделенных MCP серверов...")
        
        cache_file = self.cache_dir / "featured.json"
        if cache_file.exists():
            print("📁 Найден кэш featured серверов, загружаем...")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(self.base_url, wait_until='networkidle')
                
                print("🔍 Анализируем структуру главной страницы...")
                
                # Пробуем разные селекторы для featured секции
                featured_selectors = [
                    '[data-testid="featured-mcp"]',
                    '.featured',
                    '[class*="featured"]',
                    '[class*="hero"]',
                    '.hero',
                    'section'
                ]
                
                featured_section = None
                for selector in featured_selectors:
                    try:
                        featured_section = await page.query_selector(selector)
                        if featured_section:
                            print(f"✅ Найдена featured секция с селектором: {selector}")
                            break
                    except:
                        continue
                
                if not featured_section:
                    print("❌ Не удалось найти featured секцию")
                    return []
                
                # Извлекаем featured серверы
                featured = await self._extract_featured_data(page, featured_section)
                
                # Сохраняем в кэш
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(featured, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Найдено {len(featured)} featured серверов")
                return featured
                
            except Exception as e:
                print(f"❌ Ошибка при получении featured серверов: {e}")
                return []
            finally:
                await browser.close()
    
    async def _extract_featured_data(self, page, featured_section) -> List[Dict]:
        """Извлечение данных о featured серверах"""
        featured = []
        
        # Ищем карточки в featured секции
        cards = await featured_section.query_selector_all('*')
        
        for card in cards:
            try:
                title = await self._extract_text(card, ['h1', 'h2', 'h3', 'strong', 'b'])
                description = await self._extract_text(card, ['p', 'span'])
                link = await self._extract_attribute(card, 'a', 'href', ['a'])
                
                if title and title.strip():
                    featured.append({
                        "title": title.strip(),
                        "description": description.strip() if description else "",
                        "link": link,
                        "source": "cursor.directory",
                        "type": "featured"
                    })
            except Exception as e:
                continue
        
        return featured
    
    def list_cached_queries(self) -> List[str]:
        """Список сохраненных запросов в кэше"""
        queries = []
        for file in self.cache_dir.glob("*.json"):
            if file.name != "featured.json":
                queries.append(file.stem)
        return sorted(queries)
    
    def get_cache_stats(self) -> Dict:
        """Получение статистики кэша"""
        files = list(self.cache_dir.glob("*.json"))
        total_files = len(files)
        total_size = sum(f.stat().st_size for f in files)
        
        file_info = []
        for file in files:
            file_info.append({
                "name": file.name,
                "size": file.stat().st_size
            })
        
        return {
            "cache_dir": str(self.cache_dir),
            "total_files": total_files,
            "total_size": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "files": file_info,
            "cached_queries": self.list_cached_queries()
        }
    def clear_cache(self) -> bool:
        """Очистка кэша"""
        try:
            if self.cache_dir.exists():
                for file_path in self.cache_dir.glob("*.json"):
                    file_path.unlink()
                print(f"✅ Кэш очищен: {self.cache_dir}")
                return True
        except Exception as e:
            print(f"❌ Ошибка при очистке кэша: {e}")
            return False


async def main():
    """Основная функция"""
    scraper = CursorDirectoryScraper()
    
    if len(sys.argv) < 2:
        print("📖 Использование:")
        print("  python cursor-directory-scraper.py search <query>")
        print("  python cursor-directory-scraper.py featured")
        print("  python cursor-directory-scraper.py cache")
        print("  python cursor-directory-scraper.py stats")
        print("\n📝 Примеры:")
        print("  python cursor-directory-scraper.py search terminal")
        print("  python cursor-directory-scraper.py search java")
        print("  python cursor-directory-scraper.py search database")
        return
    
    command = sys.argv[1]
    
    if command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        servers = await scraper.search_mcp_servers(query)
        
        if servers:
            print(f"\n📋 Результаты поиска для '{query}':")
            for i, server in enumerate(servers, 1):
                print(f"\n{i}. {server['title']}")
                print(f"   Описание: {server['description']}")
                print(f"   Ссылка: {server['link']}")
                if server.get('featured'):
                    print(f"   🌟 Featured сервер")
    
    elif command == "featured":
        featured = await scraper.get_featured_servers()
        
        if featured:
            print(f"\n🌟 Выделенные MCP серверы:")
            for i, server in enumerate(featured, 1):
                print(f"\n{i}. {server['title']}")
                print(f"   Описание: {server['description']}")
                print(f"   Ссылка: {server['link']}")
    
    elif command == "cache":
        queries = scraper.list_cached_queries()
        if queries:
            print("📁 Сохраненные запросы в кэше:")
            for query in queries:
                print(f"  - {query}")
        else:
            print("📁 Кэш пуст")
    
    elif command == "stats":
        stats = scraper.get_cache_stats()
        print("📊 Статистика кэша:")
        print(f"  Всего файлов: {stats['total_files']}")
        print(f"  Общий размер: {stats['total_size_mb']} MB")
        print(f"  Сохраненные запросы: {len(stats['cached_queries'])}")
        if stats['cached_queries']:
            print("  Список запросов:")
            for query in stats['cached_queries']:
                print(f"    - {query}")
    
    else:
        print("❌ Неизвестная команда. Используйте: search, featured, cache, stats")

if __name__ == "__main__":
    asyncio.run(main())

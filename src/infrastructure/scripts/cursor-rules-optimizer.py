#!/usr/bin/env python3

"""
@file: cursor-rules-optimizer.py
@description: Python-скрипт для анализа и оптимизации файла правил проекта
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: pathlib, re, datetime
@created: 2025-08-20
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def setup_pager_protection():
    """Настройка защиты от pager для предотвращения блокировки автоматизации"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    os.environ['TERM'] = 'xterm-256color'
    os.environ['COLUMNS'] = '120'
    os.environ['LINES'] = '30'
    os.environ['GIT_PAGER'] = 'cat'
    os.environ['GIT_EDITOR'] = 'vim'

# Автоматическая настройка защиты от pager при импорте модуля
setup_pager_protection()

class CursorRulesOptimizer:
    """Оптимизатор файла правил проекта"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.current_time = datetime.now()
        
    def analyze_rules_file(self, file_path: str = ".cursorrules") -> Dict:
        """Анализ файла правил"""
        full_path = self.project_root / file_path
        
        if not full_path.exists():
            return {"error": f"Файл {file_path} не найден"}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Анализ размера
        lines = content.split('\n')
        total_lines = len(lines)
        total_chars = len(content)
        total_bytes = len(content.encode('utf-8'))
        
        # Анализ структуры
        sections = self._extract_sections(content)
        critical_rules = self._extract_critical_rules(content)
        duplicate_content = self._find_duplicates(content)
        
        return {
            "file_path": str(full_path),
            "size": {
                "lines": total_lines,
                "characters": total_chars,
                "bytes": total_bytes,
                "kilobytes": total_bytes / 1024
            },
            "structure": {
                "sections": sections,
                "critical_rules": critical_rules,
                "duplicates": duplicate_content
            },
            "recommendations": self._generate_recommendations(total_lines, total_bytes, sections)
        }
    
    def _extract_sections(self, content: str) -> List[Dict]:
        """Извлечение секций из файла правил"""
        sections = []
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        for i, line in enumerate(lines):
            # Поиск заголовков секций
            if line.startswith('## ') or line.startswith('# '):
                if current_section:
                    sections.append({
                        "title": current_section,
                        "start_line": current_section_start,
                        "end_line": i - 1,
                        "lines": len(current_content),
                        "content": '\n'.join(current_content)
                    })
                
                current_section = line.strip('# ').strip()
                current_section_start = i + 1
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Добавляем последнюю секцию
        if current_section:
            sections.append({
                "title": current_section,
                "start_line": current_section_start,
                "end_line": len(lines) - 1,
                "lines": len(current_content),
                "content": '\n'.join(current_content)
            })
        
        return sections
    
    def _extract_critical_rules(self, content: str) -> List[str]:
        """Извлечение критических правил"""
        critical_patterns = [
            r'🚨.*?КРИТИЧЕСКОЕ.*?НАПОМИНАНИЕ.*?',
            r'НИКОГДА.*?не выполняй.*?',
            r'ВСЕГДА.*?добавляй.*?',
            r'ОБЯЗАТЕЛЬНО.*?',
            r'КРИТИЧЕСКИ.*?ВАЖНО.*?'
        ]
        
        critical_rules = []
        for pattern in critical_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            critical_rules.extend(matches)
        
        return critical_rules
    
    def _find_duplicates(self, content: str) -> List[Dict]:
        """Поиск дублирующегося контента"""
        lines = content.split('\n')
        duplicates = []
        
        # Поиск повторяющихся блоков
        for i in range(len(lines) - 5):
            block = '\n'.join(lines[i:i+5])
            if len(block.strip()) > 20:  # Игнорируем короткие блоки
                count = content.count(block)
                if count > 1:
                    duplicates.append({
                        "block": block[:100] + "..." if len(block) > 100 else block,
                        "count": count,
                        "first_occurrence": i
                    })
        
        return duplicates
    
    def _generate_recommendations(self, lines: int, bytes: int, sections: List[Dict]) -> List[str]:
        """Генерация рекомендаций по оптимизации"""
        recommendations = []
        
        # Рекомендации по размеру
        if lines > 300:
            recommendations.append(f"⚠️ Файл слишком большой ({lines} строк). Рекомендуется сократить до 200-300 строк")
        
        if bytes > 50 * 1024:  # 50KB
            recommendations.append(f"⚠️ Файл превышает рекомендуемый размер ({bytes/1024:.1f}KB). Рекомендуется сократить до 30-50KB")
        
        # Рекомендации по структуре
        if len(sections) < 3:
            recommendations.append("⚠️ Мало секций. Рекомендуется разделить на логические блоки")
        
        # Рекомендации по критическим правилам
        critical_sections = [s for s in sections if 'критич' in s['title'].lower()]
        if not critical_sections:
            recommendations.append("⚠️ Отсутствуют критические правила. Рекомендуется добавить секцию с критическими правилами")
        
        # Рекомендации по модульности
        if lines > 200:
            recommendations.append("✅ Рекомендуется создать модульную систему правил")
            recommendations.append("✅ Разделить на отдельные файлы по категориям")
            recommendations.append("✅ Создать основной файл с ссылками на модули")
        
        return recommendations
    
    def create_optimized_structure(self) -> Dict:
        """Создание оптимизированной структуры правил"""
        structure = {
            "main_file": {
                "name": ".cursorrules",
                "target_size": "200-300 строк",
                "content": "Критические правила + ссылки на модули"
            },
            "modules": [
                {
                    "name": ".cursorrules-critical",
                    "description": "Критические правила безопасности",
                    "status": "Создан"
                },
                {
                    "name": ".cursorrules-development",
                    "description": "Правила разработки",
                    "status": "Создан"
                },
                {
                    "name": ".cursorrules-documentation",
                    "description": "Правила документирования",
                    "status": "Требует создания"
                },
                {
                    "name": ".cursorrules-automation",
                    "description": "Правила автоматизации",
                    "status": "Требует создания"
                },
                {
                    "name": ".cursorrules-mcp",
                    "description": "Правила работы с MCP серверами",
                    "status": "Требует создания"
                },
                {
                    "name": ".cursorrules-terminal",
                    "description": "Правила работы с терминалом",
                    "status": "Требует создания"
                },
                {
                    "name": ".cursorrules-git",
                    "description": "Правила работы с Git",
                    "status": "Требует создания"
                },
                {
                    "name": ".cursorrules-python",
                    "description": "Правила работы с Python",
                    "status": "Требует создания"
                }
            ]
        }
        
        return structure
    
    def generate_optimization_report(self) -> str:
        """Генерация отчета по оптимизации"""
        # Анализ текущего файла
        analysis = self.analyze_rules_file()
        
        if "error" in analysis:
            return f"❌ Ошибка анализа: {analysis['error']}"
        
        # Создание структуры
        structure = self.create_optimized_structure()
        
        report = f"""
🔍 ОТЧЕТ ПО ОПТИМИЗАЦИИ ФАЙЛА ПРАВИЛ
Дата: {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}

📊 АНАЛИЗ ТЕКУЩЕГО ФАЙЛА:
   Файл: {analysis['file_path']}
   Размер: {analysis['size']['lines']} строк, {analysis['size']['kilobytes']:.1f}KB
   Секций: {len(analysis['structure']['sections'])}
   Критических правил: {len(analysis['structure']['critical_rules'])}

📋 РЕКОМЕНДАЦИИ:
"""
        
        for rec in analysis['recommendations']:
            report += f"   {rec}\n"
        
        report += f"""
🏗️ ПРЕДЛАГАЕМАЯ СТРУКТУРА:

📄 Основной файл: {structure['main_file']['name']}
   Целевой размер: {structure['main_file']['target_size']}
   Содержимое: {structure['main_file']['content']}

📦 Модули:
"""
        
        for module in structure['modules']:
            status_icon = "✅" if module['status'] == "Создан" else "⏳"
            report += f"   {status_icon} {module['name']} - {module['description']} ({module['status']})\n"
        
        report += f"""
🎯 ПЛАН ОПТИМИЗАЦИИ:

1. Создать оптимизированный основной файл (.cursorrules-optimized)
2. Разделить правила по модулям
3. Создать систему динамической загрузки
4. Протестировать читаемость Cursor AI
5. Внедрить новую структуру

📈 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ:
   - Сокращение размера основного файла на 60-70%
   - Полное чтение правил Cursor AI
   - Модульная и гибкая система
   - Улучшение производительности
"""
        
        return report

def main():
    """Основная функция"""
    optimizer = CursorRulesOptimizer()
    
    print("=== CURSOR RULES OPTIMIZER ===")
    print(optimizer.generate_optimization_report())

if __name__ == "__main__":
    main()

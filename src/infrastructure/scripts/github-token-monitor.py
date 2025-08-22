#!/usr/bin/env python3
"""
Мониторинг использования GitHub Personal Access Token
Отслеживает валидность, использование и подозрительную активность
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class GitHubTokenMonitor:
    def __init__(self):
        self.token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.log_file = os.path.expanduser('~/.github-api.log')
        self.rate_limit_file = os.path.expanduser('~/.github-rate-limit.json')
        
    def log_activity(self, message: str, level: str = "INFO"):
        """Логирование активности"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} [{level}] {message}"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
        
        print(f"📝 {log_entry}")
    
    def check_rate_limit(self) -> Dict[str, Any]:
        """Проверка лимитов API"""
        try:
            response = requests.get(f'{self.base_url}/rate_limit', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.log_activity(f"Ошибка проверки лимитов: {response.status_code}", "ERROR")
                return {}
        except Exception as e:
            self.log_activity(f"Ошибка проверки лимитов: {e}", "ERROR")
            return {}
    
    def check_token_validity(self) -> bool:
        """Проверка валидности токена"""
        try:
            response = requests.get(f'{self.base_url}/user', headers=self.headers)
            
            if response.status_code == 200:
                user_data = response.json()
                self.log_activity(f"Токен валиден. Пользователь: {user_data['login']}")
                return True
            elif response.status_code == 401:
                self.log_activity("Токен невалиден (401 Bad credentials)", "ERROR")
                return False
            else:
                self.log_activity(f"Неожиданный ответ API: {response.status_code}", "WARNING")
                return False
                
        except Exception as e:
            self.log_activity(f"Ошибка проверки токена: {e}", "ERROR")
            return False
    
    def check_repository_access(self, owner: str, repo: str) -> bool:
        """Проверка доступа к репозиторию"""
        try:
            response = requests.get(f'{self.base_url}/repos/{owner}/{repo}', headers=self.headers)
            
            if response.status_code == 200:
                repo_data = response.json()
                self.log_activity(f"Доступ к репозиторию {owner}/{repo} подтвержден")
                return True
            elif response.status_code == 404:
                self.log_activity(f"Репозиторий {owner}/{repo} не найден", "WARNING")
                return False
            elif response.status_code == 403:
                self.log_activity(f"Нет доступа к репозиторию {owner}/{repo}", "ERROR")
                return False
            else:
                self.log_activity(f"Неожиданный ответ при проверке репозитория: {response.status_code}", "WARNING")
                return False
                
        except Exception as e:
            self.log_activity(f"Ошибка проверки репозитория: {e}", "ERROR")
            return False
    
    def analyze_usage_patterns(self) -> Dict[str, Any]:
        """Анализ паттернов использования"""
        try:
            # Читаем лог файл
            if not os.path.exists(self.log_file):
                return {"error": "Лог файл не найден"}
            
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            
            # Анализируем последние 24 часа
            now = datetime.now()
            day_ago = now - timedelta(days=1)
            
            recent_activity = []
            api_calls = 0
            errors = 0
            
            for line in lines:
                try:
                    # Парсим временную метку
                    timestamp_str = line[:19]  # "YYYY-MM-DD HH:MM:SS"
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    
                    if timestamp >= day_ago:
                        recent_activity.append(line.strip())
                        
                        if "API request" in line:
                            api_calls += 1
                        elif "ERROR" in line:
                            errors += 1
                            
                except ValueError:
                    continue
            
            return {
                "recent_activity_count": len(recent_activity),
                "api_calls_24h": api_calls,
                "errors_24h": errors,
                "recent_activity": recent_activity[-10:]  # Последние 10 записей
            }
            
        except Exception as e:
            return {"error": f"Ошибка анализа: {e}"}
    
    def check_suspicious_activity(self) -> Dict[str, Any]:
        """Проверка подозрительной активности"""
        analysis = self.analyze_usage_patterns()
        
        if "error" in analysis:
            return analysis
        
        suspicious = []
        
        # Проверяем количество API вызовов
        if analysis["api_calls_24h"] > 1000:
            suspicious.append(f"Высокая активность: {analysis['api_calls_24h']} вызовов за 24 часа")
        
        # Проверяем количество ошибок
        if analysis["errors_24h"] > 10:
            suspicious.append(f"Много ошибок: {analysis['errors_24h']} ошибок за 24 часа")
        
        # Проверяем паттерны использования
        for activity in analysis["recent_activity"]:
            if "delete" in activity.lower() or "remove" in activity.lower():
                suspicious.append(f"Подозрительная активность: {activity}")
        
        return {
            "suspicious_activity": suspicious,
            "analysis": analysis
        }
    
    def generate_report(self) -> str:
        """Генерация отчета"""
        report = []
        report.append("🔍 ОТЧЕТ МОНИТОРИНГА GITHUB TOKEN")
        report.append("=" * 50)
        
        # Проверка валидности токена
        if self.check_token_validity():
            report.append("✅ Токен валиден")
        else:
            report.append("❌ Токен невалиден")
            return "\n".join(report)
        
        # Проверка доступа к репозиторию
        if self.check_repository_access("bondalen", "vuege"):
            report.append("✅ Доступ к репозиторию подтвержден")
        else:
            report.append("❌ Нет доступа к репозиторию")
        
        # Проверка лимитов API
        rate_limit = self.check_rate_limit()
        if rate_limit:
            core = rate_limit.get('resources', {}).get('core', {})
            remaining = core.get('remaining', 0)
            limit = core.get('limit', 0)
            reset_time = datetime.fromtimestamp(core.get('reset', 0))
            
            report.append(f"📊 Лимиты API: {remaining}/{limit} (сброс: {reset_time.strftime('%H:%M:%S')})")
            
            if remaining < 100:
                report.append("⚠️  Мало запросов осталось!")
        
        # Анализ подозрительной активности
        suspicious = self.check_suspicious_activity()
        if suspicious.get("suspicious_activity"):
            report.append("🚨 ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ:")
            for activity in suspicious["suspicious_activity"]:
                report.append(f"   - {activity}")
        else:
            report.append("✅ Подозрительной активности не обнаружено")
        
        # Статистика использования
        analysis = suspicious.get("analysis", {})
        if "api_calls_24h" in analysis:
            report.append(f"📈 Статистика за 24 часа:")
            report.append(f"   - API вызовов: {analysis['api_calls_24h']}")
            report.append(f"   - Ошибок: {analysis['errors_24h']}")
        
        report.append("=" * 50)
        report.append(f"Отчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report)

def main():
    """Основная функция"""
    if not os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'):
        print("❌ GitHub токен не настроен")
        sys.exit(1)
    
    monitor = GitHubTokenMonitor()
    
    # Логируем запуск мониторинга
    monitor.log_activity("Запуск мониторинга GitHub токена")
    
    # Генерируем и выводим отчет
    report = monitor.generate_report()
    print(report)
    
    # Сохраняем отчет в файл
    report_file = f"~/github-token-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(os.path.expanduser(report_file), 'w') as f:
        f.write(report)
    
    print(f"\n📄 Отчет сохранен в: {report_file}")

if __name__ == "__main__":
    main()
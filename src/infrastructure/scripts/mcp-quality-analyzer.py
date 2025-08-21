#!/usr/bin/env python3
"""
@file: mcp-quality-analyzer.py
@description: Анализатор качества MCP серверов с оценкой по звездам, скачиваниям и активности
@dependencies: requests, json, os, sys, asyncio, aiohttp
@created: 2025-01-27
@pager-protection: Встроенная защита от pager
"""

import asyncio
import json
import os
import sys
import subprocess
import requests
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta

def setup_pager_protection():
    """Настройка защиты от pager"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    
    try:
        subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        pass

setup_pager_protection()

@dataclass
class MCPQualityMetrics:
    """Метрики качества MCP сервера"""
    name: str
    stars: int = 0
    forks: int = 0
    downloads: int = 0
    last_commit: Optional[str] = None
    issues: int = 0
    open_issues: int = 0
    quality_score: float = 0.0
    stability_rating: str = "Unknown"
    recommendation: str = "Unknown"

class MCPQualityAnalyzer:
    """Анализатор качества MCP серверов"""
    
    def __init__(self):
        self.github_api_base = "https://api.github.com"
        self.npm_api_base = "https://registry.npmjs.org"
        self.pypi_api_base = "https://pypi.org/pypi"
        
    async def analyze_github_repo(self, repo_url: str) -> MCPQualityMetrics:
        """Анализ GitHub репозитория"""
        try:
            # Извлекаем owner/repo из URL
            if "github.com" in repo_url:
                parts = repo_url.split("github.com/")[-1].split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1].split("#")[0].split("?")[0]
                    
                    # GitHub API запрос
                    api_url = f"{self.github_api_base}/repos/{owner}/{repo}"
                    response = requests.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        metrics = MCPQualityMetrics(
                            name=f"{owner}/{repo}",
                            stars=data.get('stargazers_count', 0),
                            forks=data.get('forks_count', 0),
                            last_commit=data.get('updated_at'),
                            issues=data.get('open_issues_count', 0),
                            open_issues=data.get('open_issues_count', 0)
                        )
                        
                        # Вычисляем качество
                        metrics.quality_score = self._calculate_quality_score(metrics)
                        metrics.stability_rating = self._get_stability_rating(metrics)
                        metrics.recommendation = self._get_recommendation(metrics)
                        
                        return metrics
                        
        except Exception as e:
            print(f"❌ Ошибка анализа GitHub репозитория {repo_url}: {e}")
            
        return MCPQualityMetrics(name=repo_url)
    
    async def analyze_npm_package(self, package_name: str) -> MCPQualityMetrics:
        """Анализ NPM пакета"""
        try:
            api_url = f"{self.npm_api_base}/{package_name}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                latest = data.get('dist-tags', {}).get('latest', {})
                version_data = data.get('versions', {}).get(latest, {})
                
                metrics = MCPQualityMetrics(
                    name=package_name,
                    downloads=version_data.get('downloads', 0),
                    last_commit=version_data.get('time', {}).get('modified')
                )
                
                # Проверяем GitHub репозиторий если есть
                repository = version_data.get('repository', {})
                if repository and 'github.com' in str(repository):
                    github_metrics = await self.analyze_github_repo(str(repository))
                    metrics.stars = github_metrics.stars
                    metrics.forks = github_metrics.forks
                    metrics.issues = github_metrics.issues
                    metrics.open_issues = github_metrics.open_issues
                
                metrics.quality_score = self._calculate_quality_score(metrics)
                metrics.stability_rating = self._get_stability_rating(metrics)
                metrics.recommendation = self._get_recommendation(metrics)
                
                return metrics
                
        except Exception as e:
            print(f"❌ Ошибка анализа NPM пакета {package_name}: {e}")
            
        return MCPQualityMetrics(name=package_name)
    
    async def analyze_pypi_package(self, package_name: str) -> MCPQualityMetrics:
        """Анализ PyPI пакета"""
        try:
            api_url = f"{self.pypi_api_base}/{package_name}/json"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                info = data.get('info', {})
                
                metrics = MCPQualityMetrics(
                    name=package_name,
                    downloads=info.get('downloads', 0),
                    last_commit=info.get('upload_time')
                )
                
                # Проверяем GitHub репозиторий если есть
                project_urls = info.get('project_urls', {})
                for url in project_urls.values():
                    if 'github.com' in str(url):
                        github_metrics = await self.analyze_github_repo(str(url))
                        metrics.stars = github_metrics.stars
                        metrics.forks = github_metrics.forks
                        metrics.issues = github_metrics.issues
                        metrics.open_issues = github_metrics.open_issues
                        break
                
                metrics.quality_score = self._calculate_quality_score(metrics)
                metrics.stability_rating = self._get_stability_rating(metrics)
                metrics.recommendation = self._get_recommendation(metrics)
                
                return metrics
                
        except Exception as e:
            print(f"❌ Ошибка анализа PyPI пакета {package_name}: {e}")
            
        return MCPQualityMetrics(name=package_name)
    
    def _calculate_quality_score(self, metrics: MCPQualityMetrics) -> float:
        """Вычисление оценки качества (0-100)"""
        score = 0.0
        
        # GitHub метрики (60% веса)
        if metrics.stars > 0:
            score += min(metrics.stars / 100, 30)  # Максимум 30 баллов за звезды
        if metrics.forks > 0:
            score += min(metrics.forks / 50, 15)   # Максимум 15 баллов за форки
        if metrics.issues > 0:
            score += min(10 - (metrics.open_issues / metrics.issues * 10), 10)  # Меньше открытых issues = лучше
        if metrics.last_commit:
            try:
                last_commit_date = datetime.fromisoformat(metrics.last_commit.replace('Z', '+00:00'))
                days_since = (datetime.now(last_commit_date.tzinfo) - last_commit_date).days
                if days_since < 30:
                    score += 5  # Активная разработка
                elif days_since < 90:
                    score += 3  # Умеренная активность
                elif days_since < 365:
                    score += 1  # Низкая активность
            except:
                pass
        
        # Downloads метрики (40% веса)
        if metrics.downloads > 0:
            score += min(metrics.downloads / 1000, 40)  # Максимум 40 баллов за скачивания
        
        return min(score, 100.0)
    
    def _get_stability_rating(self, metrics: MCPQualityMetrics) -> str:
        """Определение рейтинга стабильности"""
        if metrics.quality_score >= 80:
            return "Excellent"
        elif metrics.quality_score >= 60:
            return "Good"
        elif metrics.quality_score >= 40:
            return "Fair"
        elif metrics.quality_score >= 20:
            return "Poor"
        else:
            return "Unknown"
    
    def _get_recommendation(self, metrics: MCPQualityMetrics) -> str:
        """Рекомендация по использованию"""
        if metrics.quality_score >= 80:
            return "Strongly Recommended"
        elif metrics.quality_score >= 60:
            return "Recommended"
        elif metrics.quality_score >= 40:
            return "Use with caution"
        elif metrics.quality_score >= 20:
            return "Not recommended"
        else:
            return "Unknown quality"
    
    async def analyze_current_servers(self) -> Dict[str, MCPQualityMetrics]:
        """Анализ текущих установленных MCP серверов"""
        print("🔍 Анализируем качество текущих MCP серверов...")
        
        # Список серверов для анализа
        servers_to_analyze = {
            "terminal-controller": "terminal-controller-mcp",
            "git-mcp": "git-mcp",
            "github-mcp": "github-mcp",
            "docker-mcp": "docker-mcp",
            "jira-mcp": "jira-mcp",
            "postgres-mcp": "postgres-mcp"
        }
        
        results = {}
        
        for server_name, package_name in servers_to_analyze.items():
            print(f"\n📊 Анализируем {server_name}...")
            
            # Пробуем разные источники
            metrics = None
            
            # Сначала PyPI
            try:
                metrics = await self.analyze_pypi_package(package_name)
                if metrics.quality_score > 0:
                    print(f"✅ Найден на PyPI")
            except:
                pass
            
            # Затем NPM
            if not metrics or metrics.quality_score == 0:
                try:
                    metrics = await self.analyze_npm_package(package_name)
                    if metrics.quality_score > 0:
                        print(f"✅ Найден на NPM")
                except:
                    pass
            
            # GitHub прямой поиск
            if not metrics or metrics.quality_score == 0:
                try:
                    github_url = f"https://github.com/search?q={package_name}+mcp"
                    metrics = await self.analyze_github_repo(github_url)
                except:
                    pass
            
            results[server_name] = metrics or MCPQualityMetrics(name=package_name)
            
            # Выводим результаты
            print(f"   Звезды: {metrics.stars}")
            print(f"   Скачивания: {metrics.downloads}")
            print(f"   Оценка качества: {metrics.quality_score:.1f}/100")
            print(f"   Стабильность: {metrics.stability_rating}")
            print(f"   Рекомендация: {metrics.recommendation}")
        
        return results
    
    async def find_better_alternatives(self, current_servers: Dict[str, MCPQualityMetrics]) -> Dict[str, List[MCPQualityMetrics]]:
        """Поиск лучших альтернатив для проблемных серверов"""
        print("\n🔍 Ищем лучшие альтернативы для проблемных серверов...")
        
        alternatives = {}
        
        # Критерии для поиска альтернатив
        problematic_servers = {
            name: metrics for name, metrics in current_servers.items() 
            if metrics.quality_score < 40 or metrics.stability_rating in ["Poor", "Unknown"]
        }
        
        for server_name, metrics in problematic_servers.items():
            print(f"\n🔍 Ищем альтернативы для {server_name} (качество: {metrics.quality_score:.1f})...")
            
            # Поиск альтернатив
            alternatives[server_name] = []
            
            # Популярные альтернативы
            if server_name == "git-mcp":
                alternatives[server_name].extend([
                    await self.analyze_github_repo("https://github.com/modelcontextprotocol/server-git"),
                    await self.analyze_pypi_package("git-mcp-server"),
                ])
            elif server_name == "github-mcp":
                alternatives[server_name].extend([
                    await self.analyze_github_repo("https://github.com/modelcontextprotocol/server-github"),
                    await self.analyze_pypi_package("github-mcp-server"),
                ])
            elif server_name == "terminal-controller":
                alternatives[server_name].extend([
                    await self.analyze_github_repo("https://github.com/rinardnick/mcp-terminal"),
                    await self.analyze_npm_package("@rinardnick/mcp-terminal"),
                ])
        
        return alternatives

async def main():
    """Основная функция"""
    analyzer = MCPQualityAnalyzer()
    
    # Анализируем текущие серверы
    current_servers = await analyzer.analyze_current_servers()
    
    # Ищем альтернативы
    alternatives = await analyzer.find_better_alternatives(current_servers)
    
    # Сохраняем результаты
    results = {
        "current_servers": {name: {
            "stars": metrics.stars,
            "downloads": metrics.downloads,
            "quality_score": metrics.quality_score,
            "stability_rating": metrics.stability_rating,
            "recommendation": metrics.recommendation
        } for name, metrics in current_servers.items()},
        "alternatives": {name: [{
            "name": alt.name,
            "stars": alt.stars,
            "downloads": alt.downloads,
            "quality_score": alt.quality_score,
            "stability_rating": alt.stability_rating,
            "recommendation": alt.recommendation
        } for alt in alts] for name, alts in alternatives.items()}
    }
    
    # Сохраняем в файл
    output_file = "mcp_quality_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Результаты сохранены в {output_file}")
    
    # Выводим рекомендации
    print("\n📋 РЕКОМЕНДАЦИИ:")
    for server_name, metrics in current_servers.items():
        if metrics.quality_score < 40:
            print(f"❌ {server_name}: Низкое качество ({metrics.quality_score:.1f}/100)")
            if server_name in alternatives:
                best_alt = max(alternatives[server_name], key=lambda x: x.quality_score)
                print(f"   💡 Лучшая альтернатива: {best_alt.name} ({best_alt.quality_score:.1f}/100)")
        else:
            print(f"✅ {server_name}: Хорошее качество ({metrics.quality_score:.1f}/100)")

if __name__ == "__main__":
    asyncio.run(main())

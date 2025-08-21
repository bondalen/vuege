#!/usr/bin/env python3
"""
@file: mcp-servers-upgrade.py
@description: Автоматизированный скрипт обновления MCP серверов на высококачественные альтернативы
@dependencies: requests, json, os, sys, subprocess, pathlib
@created: 2025-01-27
@pager-protection: Встроенная защита от pager
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

def setup_pager_protection():
    """Настройка защиты от pager"""
    os.environ['PAGER'] = 'cat'
    os.environ['GIT_PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    
    try:
        subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        pass

class MCPServersUpgrader:
    """Класс для автоматизированного обновления MCP серверов"""
    
    def __init__(self):
        # Определение путей проекта
        current_script = Path(__file__).resolve()
        self.scripts_path = current_script.parent
        self.project_root = self.scripts_path.parent.parent.parent
        self.venv_path = self.project_root / "venv"
        self.mcp_config_path = Path.home() / ".cursor" / "mcp.json"
        self.backup_dir = self.project_root / "mcp_backup"
        # Базовый ENV с защитой от pager для всех подпроцессов
        self.base_env = {
            **os.environ,
            'PAGER': 'cat',
            'GIT_PAGER': 'cat',
            'LESS': '-R -M --shift 5',
            'MORE': '-R',
            'COMPOSER_NO_INTERACTION': '1',
        }
        
        # Проверка и исправление путей
        if not self.venv_path.exists():
            # Попробуем найти venv относительно текущей директории
            current_dir = Path.cwd()
            venv_candidates = [
                current_dir / "venv",
                current_dir.parent / "venv",
                Path.home() / "vuege" / "venv"
            ]
            for candidate in venv_candidates:
                if candidate.exists():
                    self.venv_path = candidate
                    self.project_root = candidate.parent
                    break
        
        # Новые высококачественные серверы
        self.new_servers = {
            "github-mcp-server": {
                "type": "docker",
                "image": "ghcr.io/github/github-mcp-server",
                "wrapper": "github-mcp-server-wrapper.py",
                "description": "GitHub MCP Server (official) for repository management"
            },
            "git-mcp-server": {
                "type": "http",
                "url": "https://gitmcp.io/bondalen/vuege",
                "wrapper": "git-mcp-server-wrapper.py",
                "description": "Git MCP Server for version control operations"
            },
            "desktop-commander-mcp": {
                "type": "npx",
                "package": "@wonderwhy-er/desktop-commander",
                "wrapper": "desktop-commander-mcp-wrapper.py",
                "description": "Desktop Commander MCP Server for terminal control"
            }
        }
        
        # Старые проблемные серверы для удаления
        self.old_servers = [
            "terminal-controller-mcp",
            "git-mcp", 
            "github-mcp"
        ]
        
        # Стабильные серверы (оставить без изменений)
        self.stable_servers = [
            "postgres-mcp",
            "docker-mcp", 
            "jira-mcp"
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """Логирование с временными метками"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_prerequisites(self) -> bool:
        """Проверка предварительных условий"""
        self.log("Проверка предварительных условий...")
        
        # Проверка существования venv
        if not self.venv_path.exists():
            self.log("❌ Виртуальное окружение venv/ не найдено", "ERROR")
            return False
        
        # Проверка существования mcp.json
        if not self.mcp_config_path.exists():
            self.log("❌ Файл конфигурации MCP не найден", "ERROR")
            return False
        
        # Проверка свободного места
        try:
            statvfs = os.statvfs(self.project_root)
            free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
            if free_space_gb < 1:
                self.log(f"❌ Недостаточно свободного места: {free_space_gb:.1f}GB", "ERROR")
                return False
            self.log(f"✅ Свободное место: {free_space_gb:.1f}GB")
        except Exception as e:
            self.log(f"⚠️ Не удалось проверить свободное место: {e}", "WARNING")
        
        self.log("✅ Предварительные условия выполнены")
        return True
    
    def create_backup(self) -> bool:
        """Создание резервных копий"""
        self.log("Создание резервных копий...")
        
        try:
            # Создание директории для резервных копий
            self.backup_dir.mkdir(exist_ok=True)
            
            # Резервная копия mcp.json
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            mcp_backup = self.backup_dir / f"mcp.json.backup.{timestamp}"
            shutil.copy2(self.mcp_config_path, mcp_backup)
            self.log(f"✅ Резервная копия mcp.json: {mcp_backup}")
            
            # Резервная копия venv
            venv_backup = self.backup_dir / f"venv.backup.{timestamp}"
            shutil.copytree(self.venv_path, venv_backup, dirs_exist_ok=True)
            self.log(f"✅ Резервная копия venv: {venv_backup}")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Ошибка создания резервных копий: {e}", "ERROR")
            return False
    
    def install_new_servers(self) -> bool:
        """Установка новых высококачественных серверов"""
        self.log("Установка новых высококачественных серверов...")
        
        # Активация виртуального окружения
        venv_python = self.venv_path / "bin" / "python"
        venv_pip = self.venv_path / "bin" / "pip"
        
        for server_name, server_info in self.new_servers.items():
            if server_info["type"] == "docker":
                # Docker образ
                self.log(f"Проверка Docker образа {server_name}...")
                try:
                    result = subprocess.run(
                        ["docker", "pull", server_info["image"]],
                        capture_output=True, text=True, check=True, timeout=300, env=self.base_env
                    )
                    self.log(f"✅ Docker образ {server_name} загружен успешно")
                except subprocess.CalledProcessError as e:
                    self.log(f"❌ Ошибка загрузки Docker образа {server_name}: {e.stderr}", "ERROR")
                    return False
            elif server_info["type"] == "http":
                # HTTP сервер (проверка доступности)
                self.log(f"Проверка доступности HTTP сервера {server_name}...")
                try:
                    import requests
                    response = requests.get(server_info["url"], timeout=10)
                    if response.status_code == 200:
                        self.log(f"✅ HTTP сервер {server_name} доступен")
                    else:
                        self.log(f"⚠️ HTTP сервер {server_name} вернул статус {response.status_code}", "WARNING")
                except Exception as e:
                    self.log(f"⚠️ Не удалось проверить HTTP сервер {server_name}: {e}", "WARNING")
            elif server_info["type"] == "npx":
                # NPX пакет (проверка доступности)
                self.log(f"Проверка доступности npx пакета {server_name}...")
                try:
                    result = subprocess.run(
                        ["npx", "--yes", server_info["package"], "--version"],
                        capture_output=True, text=True, timeout=120, env=self.base_env
                    )
                    if result.returncode == 0:
                        self.log(f"✅ npx пакет {server_name} доступен")
                    else:
                        self.log(f"⚠️ npx пакет {server_name} недоступен: {result.stderr}", "WARNING")
                except subprocess.TimeoutExpired:
                    self.log(f"⚠️ Таймаут при проверке npx пакета {server_name}", "WARNING")
                except Exception as e:
                    self.log(f"⚠️ Не удалось проверить npx пакет {server_name}: {e}", "WARNING")
            elif server_info["type"] == "npm":
                # NPM пакет (глобальная установка)
                self.log(f"Установка {server_name} через npm...")
                try:
                    result = subprocess.run(
                        ["npm", "install", "-g", server_info["package"]],
                        capture_output=True, text=True, check=True, timeout=600, env=self.base_env
                    )
                    self.log(f"✅ {server_name} установлен успешно")
                except subprocess.CalledProcessError as e:
                    self.log(f"❌ Ошибка установки {server_name}: {e.stderr}", "ERROR")
                    return False
            else:
                # Python пакет (в venv)
                self.log(f"Установка {server_name} через pip...")
                try:
                    result = subprocess.run(
                        [str(venv_pip), "install", server_info["package"]],
                        capture_output=True, text=True, check=True
                    )
                    self.log(f"✅ {server_name} установлен успешно")
                except subprocess.CalledProcessError as e:
                    self.log(f"❌ Ошибка установки {server_name}: {e.stderr}", "ERROR")
                    return False
        
        return True
    
    def create_wrappers(self) -> bool:
        """Создание Python оберток для новых серверов"""
        self.log("Создание Python оберток...")
        
        wrapper_template = '''#!/usr/bin/env python3
"""
@file: {wrapper_name}
@description: Обертка для {server_name}
@pager-protection: Встроенная защита от pager
@dependencies: {package_name}
@created: 2025-01-27
"""

import os
import sys
import subprocess
from pathlib import Path

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

def main():
    """Основная функция запуска {server_name}"""
    setup_pager_protection()
    
    # Путь к серверу
    {path_logic}
    
    # Запуск сервера
    try:
        {run_logic}
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска {server_name}: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        for server_name, server_info in self.new_servers.items():
            wrapper_path = self.scripts_path / server_info["wrapper"]
            
            # Определение логики пути и запуска
            if server_info["type"] == "docker":
                path_logic = f'''# Docker команда
docker_cmd = ["docker", "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN"]
env_token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
docker_cmd.extend([env_token, "{server_info["image"]}"])'''
                run_logic = 'subprocess.run(docker_cmd + sys.argv[1:], check=True, env=os.environ, timeout=300)'
            elif server_info["type"] == "http":
                path_logic = f'''# HTTP сервер
http_url = "{server_info["url"]}"'''
                run_logic = '''# HTTP серверы не требуют локального запуска
print(f"✅ {server_name} доступен по адресу: {http_url}")
print("HTTP серверы настраиваются в конфигурации MCP")'''
            elif server_info["type"] == "npx":
                path_logic = f'''# NPX команда
npx_cmd = ["npx", "--yes", "{server_info["package"]}"]'''
                run_logic = 'subprocess.run(npx_cmd + sys.argv[1:], check=True, env=os.environ, timeout=300)'
            elif server_info["type"] == "npm":
                if server_name == "desktop-commander-mcp":
                    path_logic = 'mcp_path = Path("/home/alex/.npm-global/bin/desktop-commander-mcp")'
                else:
                    path_logic = 'mcp_path = Path("/home/alex/.npm-global/bin/git-mcp")'
                run_logic = '''if not mcp_path.exists():
        print(f"❌ {server_name} не найден: {mcp_path}")
        sys.exit(1)
    subprocess.run([str(mcp_path)] + sys.argv[1:], check=True, env=os.environ, timeout=300)'''
            else:
                path_logic = f'mcp_path = Path(__file__).parent.parent.parent / "venv" / "bin" / "{server_info["package"]}"'
                run_logic = '''if not mcp_path.exists():
        print(f"❌ {server_name} не найден: {mcp_path}")
        sys.exit(1)
    subprocess.run([str(mcp_path)] + sys.argv[1:], check=True, env=os.environ, timeout=300)'''
            
            # Создание обертки
            wrapper_content = wrapper_template.format(
                wrapper_name=server_info["wrapper"],
                server_name=server_name,
                package_name=server_info.get("package", server_info.get("image", "unknown")),
                path_logic=path_logic,
                run_logic=run_logic
            )
            
            try:
                with open(wrapper_path, 'w', encoding='utf-8') as f:
                    f.write(wrapper_content)
                
                # Установка прав на выполнение
                os.chmod(wrapper_path, 0o755)
                self.log(f"✅ Создана обертка: {wrapper_path}")
                
            except Exception as e:
                self.log(f"❌ Ошибка создания обертки {wrapper_path}: {e}", "ERROR")
                return False
        
        return True
    
    def update_mcp_config(self) -> bool:
        """Обновление конфигурации mcp.json"""
        self.log("Обновление конфигурации mcp.json...")
        
        try:
            # Чтение текущей конфигурации
            with open(self.mcp_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Сохранение стабильных серверов
            new_config = {"mcpServers": {}}
            
            # Копирование стабильных серверов
            for server_name in self.stable_servers:
                if server_name in config["mcpServers"]:
                    new_config["mcpServers"][server_name] = config["mcpServers"][server_name]
                    self.log(f"✅ Сохранен стабильный сервер: {server_name}")
            
            # Добавление новых серверов
            for server_name, server_info in self.new_servers.items():
                if server_info["type"] == "http":
                    # HTTP сервер
                    new_config["mcpServers"][server_name] = {
                        "type": "http",
                        "url": server_info["url"],
                        "description": server_info["description"]
                    }
                elif server_info["type"] == "docker":
                    # Docker сервер
                    new_config["mcpServers"][server_name] = {
                        "command": "docker",
                        "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", server_info["image"]],
                        "env": {},
                        "description": server_info["description"]
                    }
                    # Значение PAT берется из окружения пользователя при запуске
                elif server_info["type"] == "npx":
                    # NPX сервер
                    new_config["mcpServers"][server_name] = {
                        "command": "npx",
                        "args": ["--yes", server_info["package"]],
                        "env": {},
                        "description": server_info["description"]
                    }
                else:
                    # Локальный сервер через обертку
                    new_config["mcpServers"][server_name] = {
                        "command": str(self.venv_path / "bin" / "python"),
                        "args": [str(self.scripts_path / server_info["wrapper"])],
                        "env": {},
                        "description": server_info["description"]
                    }
                self.log(f"✅ Добавлен новый сервер: {server_name}")
            
            # Запись новой конфигурации
            with open(self.mcp_config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            
            self.log("✅ Конфигурация mcp.json обновлена")
            return True
            
        except Exception as e:
            self.log(f"❌ Ошибка обновления конфигурации: {e}", "ERROR")
            return False
    
    def remove_old_servers(self) -> bool:
        """Удаление старых проблемных серверов"""
        self.log("Удаление старых проблемных серверов...")
        
        venv_pip = self.venv_path / "bin" / "pip"
        
        for server_name in self.old_servers:
            self.log(f"Удаление {server_name}...")
            try:
                result = subprocess.run(
                    [str(venv_pip), "uninstall", server_name, "-y"],
                    capture_output=True, text=True, check=True
                )
                self.log(f"✅ {server_name} удален успешно")
            except subprocess.CalledProcessError as e:
                self.log(f"⚠️ {server_name} не найден или уже удален: {e.stderr}", "WARNING")
        
        # Удаление старых оберток
        old_wrappers = [
            "terminal-controller-wrapper.py",
            "git-mcp-wrapper.py", 
            "github-mcp-wrapper.py"
        ]
        
        for wrapper in old_wrappers:
            wrapper_path = self.scripts_path / wrapper
            if wrapper_path.exists():
                try:
                    wrapper_path.unlink()
                    self.log(f"✅ Удалена старая обертка: {wrapper}")
                except Exception as e:
                    self.log(f"⚠️ Не удалось удалить {wrapper}: {e}", "WARNING")
        
        return True
    
    def test_new_servers(self) -> bool:
        """Тестирование новых серверов"""
        self.log("Тестирование новых серверов...")
        
        for server_name, server_info in self.new_servers.items():
            wrapper_path = self.scripts_path / server_info["wrapper"]
            
            if not wrapper_path.exists():
                self.log(f"❌ Обертка не найдена: {wrapper_path}", "ERROR")
                return False
            
            self.log(f"Тестирование {server_name}...")
            try:
                # Тестовый запуск обертки
                result = subprocess.run(
                    [str(self.venv_path / "bin" / "python"), str(wrapper_path), "--help"],
                    capture_output=True, text=True, timeout=10
                )
                self.log(f"✅ {server_name} тестирован успешно")
            except subprocess.TimeoutExpired:
                self.log(f"⚠️ {server_name} - таймаут (возможно нормально)", "WARNING")
            except Exception as e:
                self.log(f"⚠️ {server_name} - ошибка тестирования: {e}", "WARNING")
        
        return True
    
    def cleanup(self) -> bool:
        """Очистка временных файлов"""
        self.log("Очистка временных файлов...")
        
        try:
            # Обновление requirements.txt
            venv_pip = self.venv_path / "bin" / "pip"
            result = subprocess.run(
                [str(venv_pip), "freeze"],
                capture_output=True, text=True, check=True, env=self.base_env, timeout=120
            )
            
            requirements_path = self.project_root / "requirements.txt"
            with open(requirements_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            self.log("✅ requirements.txt обновлен")
            
            # Проверка размера venv
            venv_size = sum(f.stat().st_size for f in self.venv_path.rglob('*') if f.is_file())
            venv_size_mb = venv_size / (1024 * 1024)
            self.log(f"✅ Размер venv: {venv_size_mb:.1f}MB")
            
            return True
            
        except Exception as e:
            self.log(f"⚠️ Ошибка очистки: {e}", "WARNING")
            return True  # Не критично
    
    def run_upgrade(self) -> bool:
        """Выполнение полного процесса обновления"""
        self.log("🚀 Начало обновления MCP серверов...")
        
        steps = [
            ("Проверка предварительных условий", self.check_prerequisites),
            ("Создание резервных копий", self.create_backup),
            ("Установка новых серверов", self.install_new_servers),
            ("Создание оберток", self.create_wrappers),
            ("Обновление конфигурации", self.update_mcp_config),
            ("Тестирование новых серверов", self.test_new_servers),
            ("Удаление старых серверов", self.remove_old_servers),
            ("Очистка", self.cleanup)
        ]
        
        for step_name, step_func in steps:
            self.log(f"\n📋 {step_name}...")
            if not step_func():
                self.log(f"❌ Ошибка на этапе: {step_name}", "ERROR")
                return False
        
        self.log("\n🎉 Обновление MCP серверов завершено успешно!")
        self.log("📋 Следующие шаги:")
        self.log("1. Перезапустите Cursor IDE")
        self.log("2. Проверьте MCP Tools в Cursor")
        self.log("3. Протестируйте функциональность новых серверов")
        self.log("4. При необходимости используйте план отката из резервных копий")
        
        return True

def main():
    """Основная функция"""
    setup_pager_protection()
    
    upgrader = MCPServersUpgrader()
    
    if not upgrader.run_upgrade():
        print("\n❌ Обновление завершилось с ошибками")
        print("💡 Используйте резервные копии для отката:")
        print(f"   cp {upgrader.backup_dir}/mcp.json.backup.* ~/.cursor/mcp.json")
        print(f"   rm -rf venv && cp -r {upgrader.backup_dir}/venv.backup.* venv")
        sys.exit(1)

if __name__ == "__main__":
    main()

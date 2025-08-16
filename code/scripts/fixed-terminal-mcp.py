#!/usr/bin/env python3
"""
Fixed Terminal MCP Server
Исправленный MCP сервер для выполнения терминальных команд
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
)

# Создаем MCP сервер
server = Server("terminal-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """Возвращает список доступных инструментов"""
    return ListToolsResult(
        tools=[
            Tool(
                name="execute_command",
                description="Выполняет команду в терминале",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Команда для выполнения"
                        },
                        "working_directory": {
                            "type": "string",
                            "description": "Рабочая директория (опционально)"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Таймаут в секундах (по умолчанию 30)"
                        }
                    },
                    "required": ["command"]
                }
            ),
            Tool(
                name="run_script",
                description="Выполняет bash скрипт",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "script": {
                            "type": "string",
                            "description": "Содержимое bash скрипта"
                        },
                        "working_directory": {
                            "type": "string",
                            "description": "Рабочая директория (опционально)"
                        }
                    },
                    "required": ["script"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Обрабатывает вызов инструментов"""
    
    if name == "execute_command":
        command = arguments.get("command", "")
        working_dir = arguments.get("working_directory", None)
        timeout = arguments.get("timeout", 30)
        
        try:
            # Выполняем команду
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=working_dir,
                timeout=timeout
            )
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Команда: {command}\n"
                               f"Код возврата: {result.returncode}\n"
                               f"Вывод:\n{result.stdout}\n"
                               f"Ошибки:\n{result.stderr}"
                    }
                ]
            )
            
        except subprocess.TimeoutExpired:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Ошибка: Команда '{command}' превысила таймаут ({timeout} секунд)"
                    }
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Ошибка выполнения команды '{command}': {str(e)}"
                    }
                ]
            )
    
    elif name == "run_script":
        script = arguments.get("script", "")
        working_dir = arguments.get("working_directory", None)
        
        try:
            # Создаем временный файл со скриптом
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(script)
                script_path = f.name
            
            # Делаем файл исполняемым
            os.chmod(script_path, 0o755)
            
            # Выполняем скрипт
            result = subprocess.run(
                [script_path],
                capture_output=True,
                text=True,
                cwd=working_dir,
                timeout=30
            )
            
            # Удаляем временный файл
            os.unlink(script_path)
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Скрипт выполнен\n"
                               f"Код возврата: {result.returncode}\n"
                               f"Вывод:\n{result.stdout}\n"
                               f"Ошибки:\n{result.stderr}"
                    }
                ]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Ошибка выполнения скрипта: {str(e)}"
                    }
                ]
            )
    
    else:
        return CallToolResult(
            content=[
                {
                    "type": "text",
                    "text": f"Неизвестный инструмент: {name}"
                }
            ]
        )

async def main():
    """Главная функция"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="terminal-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())



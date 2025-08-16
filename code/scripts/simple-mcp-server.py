#!/usr/bin/env python3
"""
Simple MCP Server
Максимально простой MCP сервер для выполнения команд
"""

import asyncio
import subprocess
import sys
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, Tool

server = Server("terminal-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    return ListToolsResult(
        tools=[
            Tool(
                name="run_command",
                description="Выполняет команду в терминале",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Команда для выполнения"}
                    },
                    "required": ["command"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "run_command":
        command = arguments.get("command", "")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"Команда: {command}\nКод: {result.returncode}\nВывод:\n{result.stdout}\nОшибки:\n{result.stderr}"
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"Ошибка: {str(e)}"}]
            )
    
    return CallToolResult(content=[{"type": "text", "text": f"Неизвестный инструмент: {name}"}])

async def main():
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

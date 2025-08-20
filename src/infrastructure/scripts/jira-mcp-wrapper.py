#!/usr/bin/env python3
"""
@file: jira-mcp-wrapper.py
@description: Python обертка для JIRA MCP Server
@dependencies: subprocess, sys, os
@created: 2025-01-27
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
"""

import sys
import os
import subprocess

def setup_pager_protection():
    """Настройка защиты от pager для предотвращения блокировки автоматизации"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'

def main():
    try:
        # Настройка защиты от pager
        setup_pager_protection()
        
        # Запускаем JIRA MCP Server через npx
        cmd = ["npx", "jira-mcp"]
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: JIRA MCP Server failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("ERROR: npx not found. Please install Node.js and npm", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


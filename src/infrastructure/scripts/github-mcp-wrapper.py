#!/usr/bin/env python3
"""
@file: github-mcp-wrapper.py
@description: Python обертка для GitHub MCP Server
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
        
        # Запускаем GitHub MCP Server через npx
        cmd = ["npx", "github-mcp-custom"]
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: GitHub MCP Server failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("ERROR: npx not found. Please install Node.js and npm", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


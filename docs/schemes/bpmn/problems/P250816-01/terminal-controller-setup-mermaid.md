# Terminal Controller Setup - Mermaid BPMN

```mermaid
graph TD
    A[Start] --> B[Установка пакета terminal-controller<br/>через pip в виртуальное окружение]
    B --> C[Создание обертки terminal-controller-wrapper.py<br/>для корректного запуска MCP сервера]
    C --> D[Настройка конфигурации MCP<br/>в ~/.cursor/mcp.json с использованием обертки]
    D --> E[Перезапуск Cursor IDE<br/>для применения новой конфигурации]
    E --> F[Результат: terminal-controller появился<br/>в MCP Tools с зеленой точкой<br/>и стал доступен для использования]
    F --> G[End]
    
    style A fill:#90EE90
    style G fill:#FFB6C1
    style B fill:#E1F5FE
    style C fill:#E1F5FE
    style D fill:#E1F5FE
    style E fill:#E1F5FE
    style F fill:#E8F5E8
```

## Описание процесса:

1. **Start Event**: Начало процесса установки
2. **Task 1**: Установка пакета через pip
3. **Task 2**: Создание Python обертки
4. **Task 3**: Настройка конфигурации MCP
5. **Task 4**: Перезапуск IDE
6. **End Event**: Успешная установка

## Технические детали:

- **Виртуальное окружение**: Python venv
- **Пакет**: terminal-controller
- **Обертка**: terminal-controller-wrapper.py
- **Конфигурация**: ~/.cursor/mcp.json
- **Результат**: Зеленая точка в MCP Tools





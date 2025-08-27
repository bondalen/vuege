# Устранение неполадок MCP серверов в Cursor

## Проблема P250827-01: Недоступность команды start_process

### Описание проблемы
Команда `start_process` отображается как доступная в интерфейсе Cursor MCP Tools Settings для `desktop-commander-mcp`, но фактически недоступна при попытке использования.

### Диагностика
1. **Проверка версии**: Убедитесь, что установлена актуальная версия `@wonderwhy-er/desktop-commander`
2. **Проверка статистики**: Команда `start_process` должна быть в статистике использования
3. **Проверка документации**: Команда описана в [официальной документации](https://github.com/wonderwhy-er/DesktopCommanderMCP)

### Решение проблемы

#### Шаг 1: Обновление MCP сервера
```bash
npm update -g @wonderwhy-er/desktop-commander
```

#### Шаг 2: Перезапуск Cursor
1. Полностью закройте Cursor
2. Убедитесь, что все процессы Cursor завершены
3. Запустите Cursor заново

#### Шаг 3: Перезапуск MCP сервера в Cursor
1. Откройте настройки Cursor (Ctrl+,)
2. Перейдите в раздел "MCP Tools Settings"
3. Отключите `desktop-commander-mcp`
4. Сохраните настройки
5. Включите `desktop-commander-mcp` снова
6. Сохраните настройки

#### Шаг 4: Проверка инициализации
1. Откройте новый чат в Cursor
2. Проверьте доступность команды `start_process`
3. Если команда недоступна, повторите шаги 2-3

### Альтернативные решения

#### Вариант 1: Переустановка MCP сервера
```bash
npm uninstall -g @wonderwhy-er/desktop-commander
npm install -g @wonderwhy-er/desktop-commander
```

#### Вариант 2: Очистка кэша Cursor
1. Закройте Cursor
2. Удалите папку кэша: `~/.cursor-server/data/User/workspaceStorage/`
3. Запустите Cursor заново

#### Вариант 3: Проверка конфигурации
1. Проверьте файл конфигурации Cursor
2. Убедитесь, что MCP сервер правильно настроен
3. Проверьте права доступа к файлам

### Профилактика
1. Регулярно обновляйте MCP серверы
2. Перезапускайте Cursor после обновлений
3. Проверяйте доступность команд после изменений конфигурации

### Полезные ссылки
- [DesktopCommanderMCP GitHub](https://github.com/wonderwhy-er/DesktopCommanderMCP)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Cursor MCP Settings](https://docs.cursor.com/ai/mcp)

### Статус решения
- ✅ Проблема диагностирована
- ✅ Найдена причина (проблема инициализации MCP сервера)
- 🔄 Решение в процессе тестирования
- ⏳ Требуется подтверждение работоспособности




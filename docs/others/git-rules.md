# Правила работы с git командами в проекте Vuege

## Проблема
Git команды (log, status, diff) по умолчанию используют pager (less), который останавливает автоматическое выполнение команд и требует ручного вмешательства.

## Решение

### 1. Глобальная настройка pager
Установлен глобальный pager как `cat`:
```bash
git config --global core.pager cat
```

### 2. Алиасы для git команд
Созданы алиасы в `~/.bash_aliases`:

#### Основные алиасы без pager:
- `gitlog` - `git --no-pager log`
- `gitdiff` - `git --no-pager diff`
- `gitstatus` - `git status --porcelain`
- `gitbranch` - `git --no-pager branch`

#### Полезные сокращения:
- `gs` - `git status`
- `ga` - `git add`
- `gc` - `git commit`
- `gp` - `git push`
- `gl` - `git log --oneline -10`
- `gd` - `git diff`
- `gco` - `git checkout`
- `gb` - `git branch`
- `gf` - `git fetch`
- `gm` - `git merge`

### 3. Рекомендуемые команды для автоматизации

#### Для получения статуса (машинно-читаемый формат):
```bash
git status --porcelain
```

#### Для просмотра логов без pager:
```bash
git log --no-pager
# или
git --no-pager log
```

#### Для просмотра различий без pager:
```bash
git diff --no-pager
# или
git --no-pager diff
```

#### Для получения только имен измененных файлов:
```bash
git diff --name-only
```

### 4. Флаги для избежания pager

#### --no-pager
Отключает pager для конкретной команды:
```bash
git --no-pager log
git --no-pager diff
git --no-pager show
```

#### --porcelain
Для машинно-читаемого вывода:
```bash
git status --porcelain
```

#### --oneline
Для компактного вывода логов:
```bash
git log --oneline
```

### 5. Автоматизация в скриптах

#### Пример скрипта автоматизации:
```bash
#!/bin/bash
echo "=== Автоматизация git команд ==="

# Статус репозитория
echo "Статус:"
git status --porcelain

# Последние коммиты
echo "Последние коммиты:"
git log --oneline -5

# Измененные файлы
echo "Измененные файлы:"
git diff --name-only
```

### 6. Проверка настроек

#### Проверить глобальный pager:
```bash
git config --global --list | grep pager
```

#### Проверить алиасы:
```bash
alias | grep git
```

### 7. Troubleshooting

#### Если pager все еще открывается:
1. Проверьте настройки: `git config --global --list | grep pager`
2. Убедитесь, что установлен: `core.pager=cat`
3. Используйте флаг `--no-pager` для конкретной команды

#### Если алиасы не работают:
1. Проверьте файл: `cat ~/.bash_aliases`
2. Загрузите алиасы: `source ~/.bash_aliases`
3. Перезапустите терминал

### 8. Интеграция с Cursor IDE

Все настройки применяются автоматически в Cursor IDE, так как он использует системный терминал.

### 9. Безопасность

- Настройки pager не влияют на безопасность
- Алиасы только упрощают работу
- Все команды выполняются с теми же правами

---

## История изменений
- 2025-08-15: Создана документация по правилам работы с git
- 2025-08-15: Настроен глобальный pager как cat
- 2025-08-15: Созданы алиасы для git команд
- 2025-08-15: Протестирована автоматизация git команд

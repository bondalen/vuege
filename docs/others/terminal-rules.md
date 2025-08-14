# Правила работы с терминалом в проекте Vuege

## Избежание pager в git командах

### Проблема
Команды git (log, status, diff) открывают pager (less), который требует интерактивного взаимодействия и останавливает автоматическое выполнение.

### Решение

#### 1. Глобальная настройка git
```bash
git config --global core.pager cat
```

#### 2. Использование флагов для конкретных команд
```bash
# Вместо git log
git log --oneline -5 --no-pager

# Вместо git status
git status --porcelain

# Вместо git diff
git diff --no-pager
```

#### 3. Перенаправление вывода
```bash
git log | cat
git status | cat
git diff | cat
```

### Рекомендуемые команды для автоматизации

#### Проверка статуса
```bash
git status --porcelain
```

#### Просмотр логов
```bash
git log --oneline -5 --no-pager
```

#### Проверка синхронизации
```bash
git fetch
git status --porcelain
```

### Правила для разработки

1. **Всегда используйте `--no-pager`** для git log
2. **Используйте `--porcelain`** для git status в скриптах
3. **Перенаправляйте вывод** с помощью `| cat` при необходимости
4. **Настройте глобальный pager** как `cat` для автоматизации

---

## История
- 2025-08-14: Созданы правила для избежания pager в git командах
- 2025-08-14: Настроен глобальный pager как cat

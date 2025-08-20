# Настройка SSH подключения к GitHub

## Обзор

Данный документ описывает настройку и использование SSH подключения к GitHub для проекта Vuege.

## Текущее состояние

✅ **SSH подключение настроено и работает**
- SSH ключи: `id_ed25519_github` и `id_ed25519_auto`
- Remote URL: `git@github.com:bondalen/vuege.git`
- Автоматический скрипт: `src/infrastructure/scripts/setup-ssh-agent.sh`

## Быстрый старт

### Автоматическая настройка
```bash
# Запуск автоматического скрипта настройки
./src/infrastructure/scripts/setup-ssh-agent.sh
```

### Ручная настройка
```bash
# 1. Запуск SSH агента
eval "$(ssh-agent -s)"

# 2. Добавление ключей
ssh-add ~/.ssh/id_ed25519_github
ssh-add ~/.ssh/id_ed25519_auto

# 3. Тестирование подключения
ssh -T git@github.com
```

## Проверка статуса

### SSH агент
```bash
# Проверка запущенного агента
ssh-add -l

# Ожидаемый вывод:
# 256 SHA256:KeGFqcWDH5cbqJNcoCyg5MI7cmkVz7OIVuyed+E8qAk alex@vuege (ED25519)
# 256 SHA256:aeUTKdQy4LgniCIup4J8RtrRRFlsjsdx+M3jFuwKAZE alex@vuege-auto (ED25519)
```

### GitHub подключение
```bash
# Тест подключения к GitHub
ssh -T git@github.com

# Ожидаемый вывод:
# Hi bondalen! You've successfully authenticated, but GitHub does not provide shell access.
```

### Git remote
```bash
# Проверка настроенного remote
git remote -v

# Ожидаемый вывод:
# origin  git@github.com:bondalen/vuege.git (fetch)
# origin  git@github.com:bondalen/vuege.git (push)
```

## Решение проблем

### Проблема: "Permission denied (publickey)"
**Причина**: SSH ключ не добавлен в GitHub или SSH агент не запущен

**Решение**:
1. Проверить SSH агент: `ssh-add -l`
2. Если агент не запущен: `eval "$(ssh-agent -s)"`
3. Добавить ключ: `ssh-add ~/.ssh/id_ed25519_github`
4. Проверить ключ в GitHub: Settings → SSH and GPG keys

### Проблема: "Could not open a connection to your authentication agent"
**Причина**: SSH агент не запущен

**Решение**:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github
```

### Проблема: Git операции требуют пароль
**Причина**: Используется HTTPS вместо SSH

**Решение**:
```bash
# Переключить на SSH
git remote set-url origin git@github.com:bondalen/vuege.git

# Проверить
git remote -v
```

## Автоматизация

### Автоматический запуск при старте терминала
Добавить в `~/.bashrc`:
```bash
# SSH агент для проекта Vuege
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519_github 2>/dev/null
fi
```

### Использование в скриптах
```bash
#!/bin/bash
# Проверка SSH агента перед git операциями
if ! ssh-add -l &>/dev/null; then
    echo "SSH агент не запущен, запускаем..."
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519_github
fi
```

## Безопасность

### Права доступа к ключам
```bash
# Проверить права
ls -la ~/.ssh/id_ed25519_github

# Исправить если нужно
chmod 600 ~/.ssh/id_ed25519_github
chmod 644 ~/.ssh/id_ed25519_github.pub
```

### Ротация ключей
Рекомендуется периодически обновлять SSH ключи:
1. Создать новый ключ: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Добавить в GitHub
3. Обновить в проекте
4. Удалить старый ключ

## Связанные документы

- [Основная документация проекта](../main/project.md)
- [Журнал изменений](../main/changelog.md)
- [Отслеживание задач](../main/tasktracker.md)

## Контакты

При возникновении проблем с SSH подключением:
1. Проверить данный документ
2. Запустить автоматический скрипт настройки
3. Создать issue в проекте с описанием проблемы

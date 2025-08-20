# Чек-лист защиты от pager в терминальных командах

## Назначение
Документ содержит список команд, которые могут вызвать pager, и способы их безопасного использования в автоматизации.

## Порядок формирования записи в файле
- Каждая команда должна содержать: исходную команду, безопасную версию, описание проблемы
- Группировка по категориям: Git, Python/Pip, Системные команды, Сетевые команды
- Приоритет: Критический/Высокий/Средний/Низкий
- Статус: Актуальна/Решена/Потеряла актуальность

## Список команд с защитой от pager

### Git команды

#### Критический приоритет

**git log**
- ❌ Проблемная: `git log`
- ✅ Безопасная: `git log | cat` или `git log --no-pager`
- 📝 Описание: Отображает историю коммитов через pager

**git diff**
- ❌ Проблемная: `git diff`
- ✅ Безопасная: `git diff | cat` или `git diff --no-pager`
- 📝 Описание: Показывает различия между коммитами через pager

**git show**
- ❌ Проблемная: `git show <commit>`
- ✅ Безопасная: `git show <commit> | cat` или `git show --no-pager <commit>`
- 📝 Описание: Отображает содержимое коммита через pager

**git status**
- ❌ Проблемная: `git status`
- ✅ Безопасная: `git status --porcelain` (машинно-читаемый формат)
- 📝 Описание: Может вызвать pager при длинном выводе

#### Высокий приоритет

**git branch**
- ❌ Проблемная: `git branch -a`
- ✅ Безопасная: `git branch -a | cat`
- 📝 Описание: Список веток может быть длинным

**git tag**
- ❌ Проблемная: `git tag`
- ✅ Безопасная: `git tag | cat`
- 📝 Описание: Список тегов может быть длинным

### Python/Pip команды

#### Критический приоритет

**pip list**
- ❌ Проблемная: `pip list`
- ✅ Безопасная: `pip list | cat`
- 📝 Описание: Список установленных пакетов через pager

**pip show**
- ❌ Проблемная: `pip show <package>`
- ✅ Безопасная: `pip show <package> | cat`
- 📝 Описание: Информация о пакете через pager

**pip search**
- ❌ Проблемная: `pip search <query>`
- ✅ Безопасная: `pip search <query> | cat`
- 📝 Описание: Поиск пакетов через pager

**python -m module --help**
- ❌ Проблемная: `python -m pip --help`
- ✅ Безопасная: `python -m pip --help | cat`
- 📝 Описание: Справка модуля через pager

### Системные команды

#### Высокий приоритет

**less**
- ❌ Проблемная: `less <file>`
- ✅ Безопасная: `cat <file>` или `less -R <file>`
- 📝 Описание: Встроенный pager

**more**
- ❌ Проблемная: `more <file>`
- ✅ Безопасная: `cat <file>` или `more -R <file>`
- 📝 Описание: Встроенный pager

**man**
- ❌ Проблемная: `man <command>`
- ✅ Безопасная: `man <command> | cat`
- 📝 Описание: Справочная страница через pager

**find**
- ❌ Проблемная: `find . -name "*.py"`
- ✅ Безопасная: `find . -name "*.py" | cat`
- 📝 Описание: Может выдать много результатов

**grep**
- ❌ Проблемная: `grep -r "pattern" .`
- ✅ Безопасная: `grep -r "pattern" . | cat`
- 📝 Описание: Может найти много совпадений

### Сетевые команды

#### Средний приоритет

**curl**
- ❌ Проблемная: `curl -s "https://api.example.com/data"`
- ✅ Безопасная: `curl -s "https://api.example.com/data" | cat`
- 📝 Описание: Длинный JSON/HTML ответ может вызвать pager

**wget**
- ❌ Проблемная: `wget -qO- "https://api.example.com/data"`
- ✅ Безопасная: `wget -qO- "https://api.example.com/data" | cat`
- 📝 Описание: Длинный ответ может вызвать pager

## Глобальные настройки

### Git настройки
```bash
# Отключить pager для всех git команд
git config --global core.pager cat

# Проверить настройки
git config --global --list | grep pager
```

### Переменные окружения
```bash
# Установить переменные для предотвращения pager
export PAGER=cat
export LESS=-R
export MORE=-R

# Добавить в ~/.bashrc для постоянного эффекта
echo 'export PAGER=cat' >> ~/.bashrc
echo 'export LESS=-R' >> ~/.bashrc
echo 'export MORE=-R' >> ~/.bashrc
```

## Автоматизация

### Использование wrapper-скрипта
```bash
# Запуск команды через безопасный wrapper
./src/infrastructure/scripts/safe-command-wrapper.sh "git log --oneline"

# Настройка окружения
./src/infrastructure/scripts/safe-command-wrapper.sh
```

### Функция в bash
```bash
# Добавить в ~/.bashrc
safe_cmd() {
    local cmd="$*"
    if [[ "$cmd" == *"git log"* ]] || [[ "$cmd" == *"git diff"* ]] || [[ "$cmd" == *"pip list"* ]]; then
        eval "$cmd | cat"
    else
        eval "$cmd"
    fi
}
```

## Правила автоматизации

1. **Всегда добавляйте `| cat`** к командам, которые могут вызвать pager
2. **Используйте `--no-pager`** флаг где доступен
3. **Используйте `--porcelain`** для машинно-читаемого вывода
4. **Проверяйте длину вывода** перед выполнением команд
5. **Тестируйте команды** в автоматическом режиме

## Мониторинг

### Команды для проверки настроек
```bash
# Проверить git pager
git config --global core.pager

# Проверить переменные окружения
echo "PAGER: $PAGER"
echo "LESS: $LESS"
echo "MORE: $MORE"

# Проверить настройки терминала
stty -a | grep -E "(rows|columns)"
```

### Логирование проблем
- Записывайте все случаи блокировки pager
- Документируйте команды, которые вызвали проблемы
- Обновляйте чек-лист новыми проблемными командами

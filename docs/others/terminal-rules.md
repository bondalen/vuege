# Правила работы с терминалом в проекте Vuege

## Систематическое решение проблемы с pager

### Проблема
При выполнении терминальных команд в автоматическом режиме часто возникают проблемы с pager (less, more, git log, pip list и др.), которые блокируют выполнение команд и требуют ручного вмешательства. Это критически влияет на автоматизацию процессов разработки.

### Системное решение

#### 1. Глобальные настройки git
```bash
# Отключить pager для всех git команд
git config --global core.pager cat

# Проверить настройки
git config --global --list | grep pager
```

#### 2. Переменные окружения
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

#### 3. Использование wrapper-скрипта
```bash
# Запуск команды через безопасный wrapper
./src/infrastructure/scripts/safe-command-wrapper.sh "git log --oneline"

# Настройка окружения
./src/infrastructure/scripts/safe-command-wrapper.sh
```

### Критические команды с защитой от pager

#### Git команды
```bash
# ❌ Проблемные команды
git log
git diff
git show
git status

# ✅ Безопасные команды
git log | cat
git diff | cat
git show | cat
git status --porcelain
```

#### Python/Pip команды
```bash
# ❌ Проблемные команды
pip list
pip show <package>
pip search <query>
python -m module --help

# ✅ Безопасные команды
pip list | cat
pip show <package> | cat
pip search <query> | cat
python -m module --help | cat
```

#### Системные команды
```bash
# ❌ Проблемные команды
less <file>
more <file>
man <command>
find . -name "*.py"
grep -r "pattern" .

# ✅ Безопасные команды
cat <file>
cat <file>
man <command> | cat
find . -name "*.py" | cat
grep -r "pattern" . | cat
```

### Автоматизация

#### Функция в bash
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

#### Правила автоматизации
1. **Всегда добавляйте `| cat`** к командам, которые могут вызвать pager
2. **Используйте `--no-pager`** флаг где доступен
3. **Используйте `--porcelain`** для машинно-читаемого вывода
4. **Проверяйте длину вывода** перед выполнением команд
5. **Тестируйте команды** в автоматическом режиме

### Мониторинг и диагностика

#### Команды для проверки настроек
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

#### Логирование проблем
- Записывайте все случаи блокировки pager
- Документируйте команды, которые вызвали проблемы
- Обновляйте чек-лист новыми проблемными командами

### Документация
- **[Чек-лист защиты от pager](docs/others/pager-protection-checklist.md)** - полный список команд
- **[Safe Command Wrapper](src/infrastructure/scripts/safe-command-wrapper.sh)** - автоматический wrapper
- **[Проблема P250817-02](docs/main/problems.md)** - детальное описание проблемы

---

## История
- 2025-08-14: Созданы правила для избежания pager в git командах
- 2025-08-14: Настроен глобальный pager как cat
- 2025-08-15: Систематическое решение проблемы с pager
  - Создан wrapper-скрипт для безопасного выполнения команд
  - Создан чек-лист защиты от pager
  - Обновлены правила работы с терминалом
  - Добавлены переменные окружения и функции bash

# АНАЛИЗ БОЛЬШИХ ФАЙЛОВ В ИСТОРИИ GIT

## 🔍 ПОИСК БОЛЬШИХ ФАЙЛОВ

### Команды для анализа:

```bash
# Поиск самых больших файлов в истории
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort --numeric-sort --key=2 | tail -10

# Анализ размера объектов
git count-objects -vH

# Поиск больших файлов по размеру
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print substr($0,6)}' | sort -k2nr | head -10

# Анализ размера .git директории
du -sh .git
du -sh .git/objects
du -sh .git/objects/pack
```

## 📊 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ

### Типичные большие файлы в проектах:
- **node_modules/** - зависимости Node.js
- **target/** - сборка Maven
- ***.jar, *.war** - Java артефакты
- ***.zip, *.tar.gz** - архивы
- ***.mp3, *.mp4** - медиа файлы
- ***.log** - логи
- **venv/** - виртуальное окружение

## 🚨 КРИТИЧЕСКИЕ ФАЙЛЫ

### Файлы, которые НЕ должны быть в Git:
- **node_modules/** - зависимости
- **target/** - сборка
- ***.jar, *.war** - артефакты
- ***.log** - логи
- **venv/** - виртуальное окружение
- ***.tmp, *.temp** - временные файлы

### Файлы, которые МОГУТ быть большими:
- **Документация** - PDF, изображения
- **Тестовые данные** - большие JSON/XML
- **Конфигурационные файлы** - большие YAML/JSON
- **Миграции БД** - большие SQL файлы

## 🛠️ РЕШЕНИЯ

### 1. Удаление из истории
```bash
# Удаление файла из всей истории
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch PATH_TO_FILE' --prune-empty --tag-name-filter cat -- --all

# Очистка после удаления
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 2. Оптимизация объектов
```bash
# Упаковка объектов
git gc --aggressive

# Удаление неиспользуемых объектов
git prune

# Полная очистка
git gc --prune=now --aggressive
```

### 3. Профилактика
```bash
# Настройка .gitignore
# Ограничение размера файлов
# Pre-commit hooks
```

## 📋 ПЛАН АНАЛИЗА

1. **Запустить команды анализа** для поиска больших файлов
2. **Определить критические файлы** для удаления
3. **Выполнить очистку** истории при необходимости
4. **Оптимизировать объекты** Git
5. **Настроить профилактику** для будущего

## 🎯 ЦЕЛИ

- **Сокращение размера .git** на 50-80%
- **Улучшение производительности** Git операций
- **Предотвращение** будущего раздутия
- **Оптимизация** хранения объектов
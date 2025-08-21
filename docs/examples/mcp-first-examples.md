# Практические примеры подхода "MCP первый"

## 🎯 Цель документа

Этот файл содержит практические примеры использования подхода "MCP первый" в повседневной работе с проектом Vuege.

## 📋 Примеры по категориям

### 🔍 Анализ проекта

#### Задача: Изучить структуру проекта
```python
# MCP подход (ПРИОРИТЕТ)
list_dir("src")
list_dir("docs")
read_file("README.md", should_read_entire_file=True, start_line_one_indexed=1, end_line_one_indexed_inclusive=50)

# Терминальный подход (АЛЬТЕРНАТИВА)
ls -la src/ | cat
ls -la docs/ | cat
head -50 README.md | cat
```

#### Задача: Найти все файлы конфигурации
```python
# MCP подход (ПРИОРИТЕТ)
file_search("config")
file_search("application.yml")
grep_search("spring:", include_pattern="*.yml")

# Терминальный подход (АЛЬТЕРНАТИВА)
find . -name "*config*" | cat
find . -name "*.yml" | cat
grep -r "spring:" --include="*.yml" . | cat
```

### 📝 Работа с документацией

#### Задача: Создать новый документ
```python
# MCP подход (ПРИОРИТЕТ)
edit_file("docs/new-feature.md", """
# Новая функция

## Описание
Описание новой функции проекта.

## Использование
Примеры использования функции.

## Технические детали
Детали реализации.
""")

# Терминальный подход (АЛЬТЕРНАТИВА)
cat > docs/new-feature.md << 'EOF'
# Новая функция

## Описание
Описание новой функции проекта.

## Использование
Примеры использования функции.

## Технические детали
Детали реализации.
EOF
```

#### Задача: Обновить существующий документ
```python
# MCP подход (ПРИОРИТЕТ)
search_replace("старая версия", "новая версия")
search_replace("устаревшая информация", "актуальная информация")

# Терминальный подход (АЛЬТЕРНАТИВА)
sed -i 's/старая версия/новая версия/g' docs/file.md
sed -i 's/устаревшая информация/актуальная информация/g' docs/file.md
```

### 🔧 Разработка

#### Задача: Анализ кодовой базы
```python
# MCP подход (ПРИОРИТЕТ)
codebase_search("конфигурация базы данных")
codebase_search("GraphQL схема")
grep_search("TODO", include_pattern="*.java")
grep_search("FIXME", include_pattern="*.py")

# Терминальный подход (АЛЬТЕРНАТИВА)
grep -r "database" src/ --include="*.java" | cat
grep -r "GraphQL" src/ --include="*.java" | cat
grep -r "TODO" src/ --include="*.java" | cat
grep -r "FIXME" src/ --include="*.py" | cat
```

#### Задача: Создание нового компонента
```python
# MCP подход (ПРИОРИТЕТ)
edit_file("src/frontend/components/NewComponent.vue", """
<template>
  <div class="new-component">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: 'NewComponent',
  props: {
    title: String,
    description: String
  }
}
</script>

<style scoped>
.new-component {
  padding: 1rem;
}
</style>
""")

# Терминальный подход (АЛЬТЕРНАТИВА)
cat > src/frontend/components/NewComponent.vue << 'EOF'
<template>
  <div class="new-component">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: 'NewComponent',
  props: {
    title: String,
    description: String
  }
}
</script>

<style scoped>
.new-component {
  padding: 1rem;
}
</style>
EOF
```

### 🌿 Git операции

#### Задача: Анализ изменений
```python
# MCP подход (ПРИОРИТЕТ)
# Использование git-mcp сервера для безопасных операций
# Автоматический анализ изменений через MCP tools

# Терминальный подход (АЛЬТЕРНАТИВА)
git status --porcelain | cat
git diff --name-only | cat
git log --oneline -10 | cat
```

#### Задача: Создание коммита
```python
# MCP подход (ПРИОРИТЕТ)
# Использование git-mcp для создания коммитов
# Автоматическое добавление файлов через MCP

# Терминальный подход (АЛЬТЕРНАТИВА)
git add .
git commit -m "Добавлен новый компонент"
```

### 🔍 Отладка и диагностика

#### Задача: Поиск ошибок в логах
```python
# MCP подход (ПРИОРИТЕТ)
grep_search("ERROR", include_pattern="*.log")
grep_search("Exception", include_pattern="*.log")
codebase_search("проблема блокировки терминала")

# Терминальный подход (АЛЬТЕРНАТИВА)
grep -r "ERROR" logs/ --include="*.log" | cat
grep -r "Exception" logs/ --include="*.log" | cat
grep -r "блокировка" docs/ --include="*.md" | cat
```

#### Задача: Анализ конфигурации
```python
# MCP подход (ПРИОРИТЕТ)
read_file("src/backend/application.yml", should_read_entire_file=True, start_line_one_indexed=1, end_line_one_indexed_inclusive=100)
read_file(".env", should_read_entire_file=True, start_line_one_indexed=1, end_line_one_indexed_inclusive=50)

# Терминальный подход (АЛЬТЕРНАТИВА)
head -100 src/backend/application.yml | cat
head -50 .env | cat
```

## 🎯 Шаблоны решений

### Шаблон для новых задач:
```python
# 1. Анализ через MCP
list_dir("relevant-directory")
codebase_search("ключевые слова")
read_file("config-file.yml", should_read_entire_file=False, start_line_one_indexed=1, end_line_one_indexed_inclusive=50)

# 2. Действия через MCP (если возможно)
edit_file("result-file.md", "результат анализа")
search_replace("old-content", "new-content")

# 3. Действия через терминал (если необходимо)
run_terminal_cmd("pip install package-name", is_background=False)
run_terminal_cmd("docker run container", is_background=False)
```

### Шаблон для отладки:
```python
# 1. Диагностика через MCP
read_file("config-file.yml", should_read_entire_file=True, start_line_one_indexed=1, end_line_one_indexed_inclusive=100)
grep_search("ERROR", include_pattern="*.log")

# 2. Поиск проблем через MCP
codebase_search("проблема блокировки терминала")
grep_search("TODO", include_pattern="*.py")

# 3. Исправление через MCP или терминал
search_replace("problematic-line", "fixed-line")
run_terminal_cmd("restart-service", is_background=False)
```

## 📊 Сравнение эффективности

### Время выполнения (примеры):
- **MCP поиск файлов**: ~0.5 сек
- **Терминальный поиск**: ~1.0 сек + защита от pager
- **MCP чтение файла**: ~0.3 сек
- **Терминальное чтение**: ~0.8 сек + защита от pager

### Безопасность:
- **MCP**: Встроенная защита от pager
- **Терминал**: Требует ручной защиты

### Удобство:
- **MCP**: Естественный язык, интеграция с IDE
- **Терминал**: Требует знания команд

## 🎯 Рекомендации

### Начните с:
1. **Файловых операций** - чтение, создание, редактирование
2. **Поиска** - семантический и точный поиск
3. **Анализа** - изучение структуры проекта

### Постепенно добавьте:
1. **Git операции** - через git-mcp сервер
2. **Системные операции** - через desktop-commander-mcp
3. **Сложную автоматизацию** - комбинируя MCP и терминал

### Избегайте:
- Использования терминала для простых файловых операций
- Игнорирования встроенной защиты MCP серверов
- Смешивания подходов без четкой стратегии

---

*Этот документ является практическим руководством по применению подхода "MCP первый" в проекте Vuege.*

# Основная документация проекта Vuege

Добро пожаловать в документацию проекта Vuege! Эта папка содержит всю необходимую документацию для понимания, разработки и поддержки проекта.

## 📁 Структура документации

```
docs/
├── README.md                    # Навигация по документации
├── main/                        # Основная документация
│   ├── README.md               # Этот файл - описание основных документов
│   ├── project.md              # Архитектура и описание проекта
│   ├── diary.md                # Дневник разработки
│   ├── changelog.md            # Журнал изменений
│   ├── tasktracker.md          # Отслеживание задач
│   └── qa.md                   # Вопросы и ответы
└── others/                     # Вспомогательная документация
    ├── README.md               # Описание вспомогательных документов
    ├── ssh-setup.md            # Настройка SSH-агента
    ├── date-helper.md          # Помощник по работе с датами
    ├── postgres-mcp-setup.md   # Настройка PostgreSQL MCP Server
    ├── universal-container-setup.md # Настройка универсального контейнера
    ├── spring-boot-setup-guide.md # Руководство по настройке Spring Boot
    ├── git-rules.md            # Правила работы с git
    ├── pdf-reporting-solution.md # Решение для PDF-отчетности
    └── quasar-deployment.md    # Развертывание Quasar Framework
```

## 🎯 Основная документация (`main/`)

Четыре ключевых документа для понимания проекта:

- **[project.md](project.md)** - Архитектура, технологический стек, доменная модель
- **[diary.md](diary.md)** - Дневник разработки и технических решений
- **[changelog.md](changelog.md)** - Журнал всех изменений проекта
- **[tasktracker.md](tasktracker.md)** - Управление задачами проекта
- **[qa.md](qa.md)** - Вопросы и ответы по проекту

## 🛠️ Вспомогательная документация (`others/`)

Документы для поддержки процесса разработки:

- **[ssh-setup.md](../others/ssh-setup.md)** - Настройка автоматической аутентификации
- **[date-helper.md](../others/date-helper.md)** - Стандарты работы с датами
- **[postgres-mcp-setup.md](../others/postgres-mcp-setup.md)** - Настройка PostgreSQL MCP Server
- **[universal-container-setup.md](../others/universal-container-setup.md)** - Настройка Docker контейнера
- **[spring-boot-setup-guide.md](../others/spring-boot-setup-guide.md)** - Руководство по настройке Spring Boot
- **[git-rules.md](../others/git-rules.md)** - Правила работы с git командами
- **[pdf-reporting-solution.md](../others/pdf-reporting-solution.md)** - Решение для PDF-отчетности
- **[quasar-deployment.md](../others/quasar-deployment.md)** - Развертывание Quasar Framework

## 🚀 Быстрый старт

### Для новых участников проекта:

1. **Начните с [project.md](project.md)** - изучите архитектуру и технологический стек
2. **Изучите [diary.md](diary.md)** - поймите процесс принятия решений
3. **Настройте среду разработки** - используйте [ssh-setup.md](../others/ssh-setup.md)
4. **Изучите задачи** - ознакомьтесь с [tasktracker.md](tasktracker.md)

### Для разработчиков:

1. **Следите за [changelog.md](changelog.md)** - отслеживайте изменения
2. **Консультируйтесь с [qa.md](qa.md)** - ищите ответы на вопросы
3. **Используйте [date-helper.md](../others/date-helper.md)** - следуйте стандартам документирования

### Для DevOps/Инфраструктуры:

1. **Настройте PostgreSQL** - используйте [postgres-mcp-setup.md](../others/postgres-mcp-setup.md)
2. **Настройте контейнеры** - используйте [universal-container-setup.md](../others/universal-container-setup.md)
3. **Настройте безопасность** - используйте [ssh-setup.md](../others/ssh-setup.md)

## 📋 Процесс обновления документации

При внесении изменений в проект обязательно обновляйте соответствующую документацию:

| Тип изменения | Основные документы | Вспомогательные документы |
|---------------|-------------------|---------------------------|
| **Новые функции** | changelog.md | tasktracker.md |
| **Архитектурные изменения** | project.md, diary.md | - |
| **Технические решения** | diary.md | - |
| **Новые вопросы** | qa.md | - |
| **Настройки среды** | - | соответствующие setup-документы |
| **Новые задачи** | - | tasktracker.md |
| **Стандарты** | - | date-helper.md |

## 🔍 Поиск информации

### По темам:
- **Архитектура** → [project.md](project.md)
- **Изменения** → [changelog.md](changelog.md)
- **Решения** → [diary.md](diary.md)
- **Вопросы** → [qa.md](qa.md)
- **Задачи** → [tasktracker.md](tasktracker.md)
- **Настройки** → соответствующие setup-документы в [others/](../others/)

### По ролям:
- **Архитектор** → [project.md](project.md), [diary.md](diary.md)
- **Разработчик** → [changelog.md](changelog.md), [qa.md](qa.md)
- **DevOps** → setup-документы в [others/](../others/)
- **Менеджер** → [tasktracker.md](tasktracker.md)

## 📝 Стандарты документирования

- **Даты**: формат YYYY-MM-DD (см. [date-helper.md](../others/date-helper.md))
- **Ссылки**: относительные пути к файлам
- **Структура**: четкое разделение на разделы
- **Обновления**: регулярное обновление при изменениях

## 🤝 Вклад в документацию

При добавлении новой документации:

1. **Все новые документы размещаются в папке `others/`**
2. Основные документы (`main/`) остаются неизменными: project.md, diary.md, changelog.md, tasktracker.md, qa.md
3. Обновите README файлы с описанием нового документа
4. Добавьте ссылки в соответствующие README файлы

## 📊 Статистика документации

- **Основных документов**: 5
- **Вспомогательных документов**: 8
- **Общий объем**: ~60KB текста
- **Последнее обновление**: 2025-08-15

---

*Документация проекта Vuege - полное руководство по разработке и поддержке*

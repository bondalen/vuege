# Настройка GitHub Personal Access Token для MCP сервера

## 🎯 Цель
Настроить GitHub Personal Access Token для полноценной работы GitHub MCP Server.

## 🚀 Новый подход: Desktop Commander MCP

**ВАЖНО**: В этом проекте мы используем Desktop Commander MCP сервер вместо прямого терминала для предотвращения проблем с pager и блокировкой терминалов.

### Преимущества Desktop Commander MCP:
- ✅ **Безопасность**: Нет риска блокировки терминала
- ✅ **Надежность**: Встроенная защита от pager
- ✅ **Удобство**: Автоматическое управление файлами и командами
- ✅ **Производительность**: Оптимизированные операции

## 📋 Пошаговая инструкция

### Шаг 1: Создание Personal Access Token

1. **Перейдите на GitHub:**
   - Откройте [GitHub Settings](https://github.com/settings)
   - Войдите в свой аккаунт

2. **Создайте новый токен:**
   - Перейдите в [Personal Access Tokens → Tokens (classic)](https://github.com/settings/tokens)
   - Нажмите "Generate new token (classic)"

3. **Настройте токен:**
   - **Note**: `Vuege MCP Server`
   - **Expiration**: Выберите срок действия (рекомендуется 90 дней)
   - **Scopes**: Выберите необходимые права:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
     - ✅ `write:packages` (Upload packages to GitHub Package Registry)
     - ✅ `delete:packages` (Delete packages from GitHub Package Registry)
     - ✅ `admin:org` (Full control of orgs and teams)
     - ✅ `admin:public_key` (Full control of user public keys)
     - ✅ `admin:repo_hook` (Full control of repository hooks)
     - ✅ `admin:org_hook` (Full control of organization hooks)
     - ✅ `gist` (Create gists)
     - ✅ `notifications` (Access notifications)
     - ✅ `user` (Update all user data)
     - ✅ `delete_repo` (Delete repositories)
     - ✅ `write:discussion` (Create and edit discussions)
     - ✅ `admin:enterprise` (Full control of enterprises)
     - ✅ `write:packages` (Upload packages to GitHub Package Registry)
     - ✅ `read:packages` (Download packages from GitHub Package Registry)
     - ✅ `delete:packages` (Delete packages from GitHub Package Registry)
     - ✅ `admin:gpg_key` (Full control of GPG keys)
     - ✅ `admin:ssh_signing_key` (Full control of SSH signing keys)

4. **Скопируйте токен:**
   - Нажмите "Generate token"
   - **ВАЖНО**: Скопируйте токен сразу (он больше не будет показан)

### Шаг 2: Настройка токена (Desktop Commander MCP)

#### Вариант 1: Автоматическая настройка через скрипт
```bash
# Запустите скрипт настройки
./src/infrastructure/scripts/setup-github-token.sh
```

#### Вариант 2: Ручная настройка в .env файле
Обновите файл `.env` в корне проекта:
```bash
# Добавьте строку с вашим токеном
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_actual_token_here
```

#### Вариант 3: Настройка в переменной окружения
```bash
# Временная настройка (для текущей сессии)
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_actual_token_here"

# Постоянная настройка
echo 'export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_actual_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Шаг 3: Проверка настройки

#### Автоматическое тестирование
```bash
# Запустите тест GitHub MCP сервера
python src/infrastructure/scripts/test-github-mcp.py
```

#### Ожидаемый результат:
```
🚀 Тестирование GitHub MCP сервера
==================================================
🔍 Проверка GitHub токена...
✅ GitHub токен найден: ghp_1234567...
✅ Токен валиден! Пользователь: bondalen

🔍 Проверка конфигурации MCP...
✅ GitHub MCP сервер настроен в конфигурации

🧪 Тестирование GitHub API...
1. Получение информации о пользователе...
   ✅ Пользователь: bondalen
2. Получение списка репозиториев...
   ✅ Найдено репозиториев: 15
3. Проверка доступа к репозиторию vuege...
   ✅ Репозиторий: bondalen/vuege

==================================================
📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:
GitHub токен: ✅
Конфигурация MCP: ✅
GitHub API: ✅

🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
GitHub MCP сервер готов к использованию
```

## 🔒 Безопасность

### Важные правила:
1. **Никогда не коммитьте токен в репозиторий**
2. **Используйте переменные окружения или .env файл**
3. **Регулярно обновляйте токен**
4. **Ограничивайте права токена минимально необходимыми**

### Проверка безопасности:
```bash
# Проверьте, что токен не в коде
grep -r "ghp_" . --exclude-dir=venv --exclude-dir=.git
```

## 🚨 Устранение проблем

### Проблема: "GitHub токен не настроен"
**Решение:**
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_actual_token_here"
```

### Проблема: "Bad credentials"
**Решение:**
- Проверьте правильность токена
- Убедитесь, что токен не истёк
- Проверьте права токена

### Проблема: "Not found"
**Решение:**
- Проверьте название репозитория
- Убедитесь в правах доступа к репозиторию

### Проблема: "Desktop Commander MCP не работает"
**Решение:**
- Перезапустите Cursor IDE
- Проверьте конфигурацию MCP в `~/.cursor/mcp.json`
- Убедитесь, что Desktop Commander MCP сервер активен

## 📊 Мониторинг

### Проверка статуса токена:
```bash
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
     https://api.github.com/user
```

### Проверка прав токена:
```bash
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
     https://api.github.com/user/repos
```

## 🎯 Результат

После правильной настройки:
- ✅ GitHub MCP Server будет полностью функционален
- ✅ Можно создавать issues, коммиты, pull requests
- ✅ Доступны все операции с репозиторием
- ✅ Автоматизация GitHub операций через MCP
- ✅ Безопасная работа без риска блокировки терминала

## 🔧 Инструменты

### Скрипты настройки:
- `./src/infrastructure/scripts/setup-github-token.sh` - настройка токена
- `./src/infrastructure/scripts/test-github-mcp.py` - тестирование

### Конфигурационные файлы:
- `~/.cursor/mcp.json` - конфигурация MCP серверов
- `.env` - переменные окружения проекта

---

**Создано**: 2025-08-21  
**Обновлено**: 2025-08-22 (Desktop Commander MCP)  
**Статус**: Готово к использованию  
**Приоритет**: Высокий
# Vuege Frontend

Frontend приложение для системы учета организационных единиц Vuege.

## Технологии

- **Vue.js 3.4.21** - Прогрессивный JavaScript фреймворк
- **Quasar 2.18.2** - Vue.js фреймворк для создания приложений
- **Vue Router 4.3.0** - Официальный роутер для Vue
- **Apollo Client** - GraphQL клиент
- **TypeScript** - Типизированный JavaScript
- **Vite** - Быстрый сборщик

## Структура проекта

```
src/
├── components/     # Vue компоненты
├── pages/         # Страницы приложения
├── router/        # Конфигурация роутера
├── stores/        # Состояние приложения
├── types/         # TypeScript типы
├── utils/         # Утилиты
├── main.ts        # Точка входа
└── style.css      # Глобальные стили
```

## Разработка

### Установка зависимостей
```bash
npm install
```

### Запуск в режиме разработки
```bash
npm run dev
```

### Сборка для продакшена
```bash
npm run build
```

### Линтинг
```bash
npm run lint
```

### Форматирование кода
```bash
npm run format
```

## Интеграция с Backend

Frontend интегрирован с Spring Boot backend через:
- **GraphQL API** - основной API
- **Proxy настройки** - для разработки
- **Единый JAR** - для продакшена

## Развертывание

Frontend автоматически собирается и включается в единый JAR файл через frontend-maven-plugin.

## Структура проекта

Frontend находится в папке `src/app/frontend/` для корректной работы с Maven ресурсами плагином.
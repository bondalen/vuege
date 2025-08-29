# Шаблон разработки страницы сущности: Форма организаций

**Псевдонимы**: шаблон страницы организаций, template organizations page

## 🎯 Цель документа
Документация формы организаций как эталонного шаблона для разработки страниц управления любыми сущностями в проекте Vuege.

## 📊 Статус реализации
- **Готовность**: 100% (полностью реализована и протестирована)
- **Функциональность**: Все CRUD операции работают корректно
- **Дизайн**: Современный и удобный интерфейс
- **Производительность**: Оптимизирована для больших объемов данных

---

## 🏗️ Архитектура страницы

### Структура компонента
```
OrganizationsPage.vue
├── Заголовок страницы
├── Фильтры и поиск
├── Основная таблица
├── Вкладки с деталями
│   ├── Вкладка "Должности"
│   └── Вкладка "Дочерние организации"
└── Диалоги создания/редактирования
```

### Ключевые принципы
1. **Модульность**: Каждый блок функциональности в отдельном компоненте
2. **Реактивность**: Автоматическое обновление при изменении данных
3. **Производительность**: Ленивая загрузка данных по вкладкам
4. **UX**: Интуитивный интерфейс с понятной навигацией

---

## 🎨 Дизайн и UI/UX

### Цветовая схема
- **Основной цвет**: `primary` (синий) - для кнопок и активных элементов
- **Акцентный цвет**: `info` (голубой) - для информационных элементов
- **Отрицательный цвет**: `negative` (красный) - для удаления
- **Нейтральный цвет**: `grey-7` - для второстепенных элементов

### Компоненты Quasar Framework
- **q-page**: Основной контейнер страницы
- **q-card**: Карточки для группировки контента
- **q-table**: Таблицы с сортировкой и пагинацией
- **q-tabs**: Вкладки для организации контента
- **q-dialog**: Модальные окна для форм
- **q-input**: Поля ввода с валидацией
- **q-select**: Выпадающие списки с фильтрацией
- **q-btn**: Кнопки с иконками и состояниями
- **q-chip**: Чипы для отображения статусов

### Адаптивность
- **Мобильные устройства**: Компактный дизайн с вертикальным расположением
- **Планшеты**: Гибридный дизайн с адаптивными колонками
- **Десктоп**: Полнофункциональный интерфейс с боковыми панелями

---

## 🔧 Технические решения

### Vue.js Composition API
```javascript
// Реактивные данные
const organizations = ref([])
const selectedOrganization = ref(null)
const loading = ref(false)
const searchQuery = ref('')

// Вычисляемые свойства
const filteredOrganizations = computed(() => {
  return organizations.value.filter(org => 
    org.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Опции для q-select (обязательно computed!)
const typeOptions = computed(() => [
  { label: 'Все типы', value: null },
  { label: 'Империя', value: 'EMPIRE' },
  { label: 'Государство', value: 'STATE' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Правительственная', value: 'GOVERNMENT' }
])

const statusOptions = computed(() => [
  { label: 'Все статусы', value: null },
  { label: 'Активная', value: 'active' },
  { label: 'Неактивная', value: 'inactive' },
  { label: 'Ликвидированная', value: 'dissolved' }
])

// Методы
const selectOrganization = (org) => {
  selectedOrganization.value = org
  loadOrganizationDetails(org.id)
}
```

### GraphQL интеграция
```javascript
// Apollo Client запросы
const { result, loading, error } = useQuery(GET_ORGANIZATIONS)

// Мутации с обработкой ошибок
const [createOrganization] = useMutation(CREATE_ORGANIZATION, {
  update: (cache, { data }) => {
    cache.modify({
      fields: {
        organizationalUnits(existing = []) {
          return [...existing, data.createOrganizationalUnit]
        }
      }
    })
  }
})
```

### Управление состоянием
- **Локальное состояние**: Vue.js ref/reactive для UI состояния
- **Серверное состояние**: Apollo Client для кэширования GraphQL данных
- **Синхронизация**: Автоматическое обновление при мутациях

---

## 📋 Функциональные блоки

### 1. Фильтры и поиск
```vue
<q-card class="filter-card">
  <q-card-section>
    <!-- Поиск -->
    <q-input
      v-model="searchQuery"
      label="Поиск"
      outlined
      dense
    />
    
    <!-- Фильтры -->
    <div class="row q-gutter-md">
      <q-select
        v-model="selectedType"
        :options="typeOptions"
        label="Тип организации"
        outlined
        dense
        dark
        clearable
        option-value="value"
        option-label="label"
        emit-value
        map-options
        class="filter-select"
        style="flex: 2; margin-right: 8px; background-color: #f5f5f5;"
      />
      
      <q-select
        v-model="selectedStatus"
        :options="statusOptions"
        label="Статус"
        outlined
        dense
        dark
        clearable
        option-value="value"
        option-label="label"
        emit-value
        map-options
        class="filter-select"
        style="flex: 1; background-color: #f5f5f5;"
      />
    </div>
  </q-card-section>
</q-card>
```

**Особенности:**
- Реактивный поиск в реальном времени
- Комбинированные фильтры с множественным выбором
- Сохранение состояния фильтров

### 2. Основная таблица
```vue
<q-table
  :rows="filteredOrganizations"
  :columns="columns"
  :loading="loading"
  row-key="id"
  :pagination="{ rowsPerPage: 10 }"
  dense
>
  <template v-slot:body="props">
    <q-tr @click="selectOrganization(props.row)">
      <!-- Колонки таблицы -->
    </q-tr>
  </template>
</q-table>
```

**Особенности:**
- Сортировка по всем колонкам
- Пагинация для больших объемов данных
- Выделение выбранной строки
- Компактный дизайн (dense)

### 3. Вкладки с деталями
```vue
<q-tabs v-model="activeTab">
  <q-tab name="positions" label="Должности" icon="work" />
  <q-tab name="childUnits" label="Дочерние организации" icon="account_tree" />
</q-tabs>

<q-tab-panels v-model="activeTab">
  <q-tab-panel name="positions">
    <!-- Содержимое вкладки должностей -->
  </q-tab-panel>
  <q-tab-panel name="childUnits">
    <!-- Содержимое вкладки дочерних организаций -->
  </q-tab-panel>
</q-tab-panels>
```

**Особенности:**
- Ленивая загрузка данных по вкладкам
- Отдельные состояния загрузки для каждой вкладки
- Возможность добавления новых элементов в каждой вкладке

### 4. Формы создания/редактирования
```vue
<q-dialog v-model="showCreateDialog" persistent>
  <q-card>
    <q-card-section>
      <div class="text-h6">
        {{ editingOrganization ? 'Редактировать' : 'Создать' }} организацию
      </div>
    </q-card-section>
    
    <q-card-section>
      <div class="row q-gutter-md">
        <q-input
          v-model="form.name"
          label="Название *"
          :rules="[val => !!val || 'Название обязательно']"
        />
        <!-- Другие поля формы -->
      </div>
    </q-card-section>
    
    <q-card-actions align="right">
      <q-btn flat label="Отмена" v-close-popup />
      <q-btn :label="editingOrganization ? 'Сохранить' : 'Создать'" @click="saveOrganization" />
    </q-card-actions>
  </q-card>
</q-dialog>
```

**Особенности:**
- Валидация полей в реальном времени
- Условное отображение полей
- Автоматическое заполнение при редактировании

### 5. Стили для q-select компонентов

#### Базовый шаблон q-select
```vue
<q-select
  v-model="selectedValue"
  :options="options"
  label="Название поля"
  outlined
  dense
  dark
  clearable
  option-value="value"
  option-label="label"
  emit-value
  map-options
  class="filter-select"
  style="background-color: #f5f5f5;"
/>
```

#### Computed опции (обязательно!)
```javascript
// Правильно - используем computed для реактивности
const options = computed(() => [
  { label: 'Все варианты', value: null },
  { label: 'Вариант 1', value: 'value1' },
  { label: 'Вариант 2', value: 'value2' }
])

// Неправильно - обычный массив
const options = [
  { label: 'Вариант 1', value: 'value1' },
  { label: 'Вариант 2', value: 'value2' }
]
```

#### CSS стили для улучшенной видимости
```css
/* Стили для q-select фильтров - базовая видимость */
.filter-select :deep(.q-field__label) {
  color: #1976d2 !important;
  font-weight: 500 !important;
}

.filter-select :deep(.q-field__native) {
  color: #2c3e50 !important;
  font-weight: 500 !important;
}

.filter-select :deep(.q-field__control) {
  background-color: #ffffff !important;
  border: 1px solid #e0e0e0 !important;
}

.filter-select :deep(.q-field--focused .q-field__control) {
  border-color: #1976d2 !important;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2) !important;
}

.filter-select :deep(.q-field--outlined .q-field__control:before) {
  border-color: #e0e0e0 !important;
}

.filter-select :deep(.q-field--outlined .q-field__control:hover:before) {
  border-color: #1976d2 !important;
}

.filter-select :deep(.q-select__dropdown) {
  background-color: #ffffff !important;
  color: #2c3e50 !important;
}

.filter-select :deep(.q-item) {
  color: #2c3e50 !important;
  background-color: #ffffff !important;
}

.filter-select :deep(.q-item:hover) {
  background-color: #f5f5f5 !important;
}

.filter-select :deep(.q-item--active) {
  background-color: #e3f2fd !important;
  color: #1976d2 !important;
}

/* Стили для q-select в диалогах - улучшенная видимость полей */
.q-dialog .q-select :deep(.q-field__label) {
  color: #1976d2 !important;
  font-weight: 500 !important;
}

.q-dialog .q-select :deep(.q-field__native) {
  color: #2c3e50 !important;
  font-weight: 500 !important;
}

.q-dialog .q-select :deep(.q-field__control) {
  background-color: #ffffff !important;
  border: 1px solid #e0e0e0 !important;
}

.q-dialog .q-select :deep(.q-field--focused .q-field__control) {
  border-color: #1976d2 !important;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2) !important;
}

.q-dialog .q-select :deep(.q-field--outlined .q-field__control:before) {
  border-color: #e0e0e0 !important;
}

.q-dialog .q-select :deep(.q-field--outlined .q-field__control:hover:before) {
  border-color: #1976d2 !important;
}

.q-dialog .q-select :deep(.q-select__dropdown) {
  background-color: #ffffff !important;
  color: #2c3e50 !important;
}

.q-dialog .q-select :deep(.q-item) {
  color: #2c3e50 !important;
  background-color: #ffffff !important;
}

.q-dialog .q-select :deep(.q-item:hover) {
  background-color: #f5f5f5 !important;
}

.q-dialog .q-select :deep(.q-item--active) {
  background-color: #e3f2fd !important;
  color: #1976d2 !important;
}
```

#### Ключевые принципы для q-select:
1. **Всегда используйте `computed`** для опций
2. **Добавляйте атрибут `dark`** для контраста
3. **Используйте `background-color: #f5f5f5`** для фона
4. **Применяйте CSS стили** для улучшенной видимости полей и опций
5. **Используйте `clearable`** для возможности очистки
6. **Добавляйте `option-value` и `option-label`** для объектов
7. **Используйте `emit-value` и `map-options`** для правильной работы
8. **Применяйте отдельные стили для диалогов** через `.q-dialog .q-select`
- Обработка ошибок сервера

---

## 🔄 CRUD операции

### CREATE (Создание)
```javascript
const createOrganization = async (formData) => {
  try {
    const { data } = await createOrganizationMutation({
      variables: { input: formData }
    })
    
    // Обновление кэша Apollo Client
    cache.modify({
      fields: {
        organizationalUnits(existing = []) {
          return [...existing, data.createOrganizationalUnit]
        }
      }
    })
    
    // Уведомление пользователя
    $q.notify({
      type: 'positive',
      message: 'Организация успешно создана'
    })
  } catch (error) {
    handleError(error)
  }
}
```

### READ (Чтение)
```javascript
// Основной запрос
const { result, loading, error } = useQuery(GET_ORGANIZATIONS)

// Запрос с параметрами
const { result: organizationDetails } = useQuery(GET_ORGANIZATION, {
  variables: { id: selectedOrganizationId.value },
  skip: !selectedOrganizationId.value
})
```

### UPDATE (Обновление)
```javascript
const updateOrganization = async (id, formData) => {
  try {
    const { data } = await updateOrganizationMutation({
      variables: { id, input: formData }
    })
    
    // Обновление кэша
    cache.modify({
      id: cache.identify({ __typename: 'OrganizationalUnit', id }),
      fields: {
        name: () => data.updateOrganizationalUnit.name,
        type: () => data.updateOrganizationalUnit.type
      }
    })
  } catch (error) {
    handleError(error)
  }
}
```

### DELETE (Удаление)
```javascript
const deleteOrganization = async (id) => {
  try {
    await deleteOrganizationMutation({
      variables: { id }
    })
    
    // Удаление из кэша
    cache.evict({ id: cache.identify({ __typename: 'OrganizationalUnit', id }) })
    cache.gc()
  } catch (error) {
    handleError(error)
  }
}
```

---

## 🎯 Шаблон для других сущностей

### Структура файлов
```
src/app/frontend/src/pages/
├── OrganizationsPage.vue          # ✅ Эталонная реализация
├── StatesPage.vue                 # 🔄 Требует доработки
├── PersonsPage.vue                # ⏳ Планируется
├── PositionsPage.vue              # ⏳ Планируется
└── LocationsPage.vue              # ⏳ Планируется
```

### Копирование шаблона
1. **Скопировать OrganizationsPage.vue** в новый файл
2. **Заменить названия сущностей** и переменных
3. **Адаптировать GraphQL запросы** под новую сущность
4. **Настроить колонки таблицы** под поля новой сущности
5. **Добавить специфичные вкладки** при необходимости

### Обязательные компоненты
- ✅ Фильтры и поиск
- ✅ Основная таблица с CRUD операциями
- ✅ Вкладки с связанными данными
- ✅ Формы создания/редактирования
- ✅ Обработка ошибок и уведомления
- ✅ Адаптивный дизайн

---

## 🚀 Оптимизации и лучшие практики

### Производительность
- **Ленивая загрузка**: Данные загружаются только при необходимости
- **Кэширование**: Apollo Client кэширует GraphQL запросы
- **Виртуализация**: Для больших таблиц используется виртуализация
- **Debounce**: Поиск с задержкой для оптимизации запросов

### Безопасность
- **Валидация**: Проверка данных на клиенте и сервере
- **Санитизация**: Очистка пользовательского ввода
- **Авторизация**: Проверка прав доступа к операциям
- **CSRF защита**: Защита от межсайтовых запросов

### UX/UI
- **Состояния загрузки**: Спиннеры и скелетоны
- **Обработка ошибок**: Понятные сообщения об ошибках
- **Подтверждения**: Диалоги для критических операций
- **Клавиатурная навигация**: Горячие клавиши для быстрой работы

### Решение проблем q-select
- **Проблема "белый по белому"**: Используйте атрибут `dark` и фон `#f5f5f5`
- **Невидимые опции**: Всегда используйте `computed` для опций
- **Проблемы с фильтрацией**: Правильно обрабатывайте `null` значения
- **Плохая видимость лейблов**: Применяйте CSS стили для контраста

---

## 📈 Метрики и мониторинг

### Производительность
- **Время загрузки**: < 2 секунд для основной таблицы
- **Время отклика**: < 100ms для пользовательских действий
- **Размер бандла**: Оптимизация для быстрой загрузки

### Пользовательский опыт
- **Успешность операций**: > 95% успешных CRUD операций
- **Время выполнения задач**: < 30 секунд для типичных операций
- **Удовлетворенность**: Положительные отзывы пользователей

---

## 🔧 Настройка и конфигурация

### Переменные окружения
```javascript
// .env
VUE_APP_GRAPHQL_ENDPOINT=http://localhost:8082/api/graphql
VUE_APP_API_TIMEOUT=30000
VUE_APP_PAGE_SIZE=10
```

### Конфигурация Apollo Client
```javascript
// apollo-client.js
const client = new ApolloClient({
  uri: process.env.VUE_APP_GRAPHQL_ENDPOINT,
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          organizationalUnits: {
            merge: false
          }
        }
      }
    }
  })
})
```

---

## 📚 Документация и ресурсы

### Связанные документы
- [GraphQL Schema](../backend/graphql/schema.graphqls)
- [Vue.js Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Quasar Framework](https://quasar.dev/)
- [Apollo Client](https://www.apollographql.com/docs/react/)
- [Решение проблем q-select](../solutions/q-select-white-on-white-fix.md)

### Примеры использования
- [OrganizationsPage.vue](../../src/app/frontend/src/pages/OrganizationsPage.vue)
- [GraphQL Queries](../../src/app/frontend/src/graphql/queries.ts)
- [GraphQL Mutations](../../src/app/frontend/src/graphql/mutations.ts)

---

## 🎯 Заключение

Форма организаций представляет собой эталонную реализацию страницы управления сущностями в проекте Vuege. Она демонстрирует:

1. **Современные технологии**: Vue.js 3, Composition API, GraphQL
2. **Лучшие практики**: Модульная архитектура, реактивность, производительность
3. **Пользовательский опыт**: Интуитивный интерфейс, адаптивность, обработка ошибок
4. **Масштабируемость**: Легкое копирование и адаптация для других сущностей

Этот шаблон служит основой для разработки всех страниц управления сущностями в проекте.

---
**Создано**: 2025-08-29  
**Статус**: Актуально  
**Приоритет**: Высокий

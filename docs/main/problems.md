# Долговременные проблемы проекта Vuege

**Псевдонимы**: файл проблем

Этот файл содержит учет проблем, которые не удалось решить в рамках одного чата и требуют долгосрочного решения.

## Порядок формирования записи в файле

### Система нумерации
Проблемы нумеруются по шаблону: **PYYMMDD-NN**
- **P** - префикс для обозначения проблемы (Problem)
- **YYMMDD** - дата выявления проблемы (год-месяц-день)
- **NN** - порядковый номер проблемы в течение дня (01, 02, 03...)

### Статусы проблем
- **Актуальна** - проблема требует решения
- **Решена** - проблема решена, но может повториться
- **Потеряла актуальность** - проблема больше не актуальна

### Приоритеты проблем
- **Критический** - блокирует работу проекта
- **Высокий** - существенно влияет на работу
- **Средний** - влияет на эффективность
- **Низкий** - не критично, но желательно решить

### Структура записи проблемы
```
## [PYYMMDD-NN] - Краткое описание проблемы

**Статус**: [Актуальна/Решена/Потеряла актуальность]
**Дата выявления**: YYYY-MM-DD
**Приоритет**: [Критический/Высокий/Средний/Низкий]

### Описание
Детальное описание проблемы и ее влияния на проект.

### Полезные ссылки
- Ссылки на альтернативные решения и ресурсы
- Ссылки на документацию и примеры
- Ссылки на связанные проекты и инструменты

### История решения
#### Чат N: [Название чата или "Чат не известен"]
##### Попытка N (YYYY-MM-DD)
**Действия**: Описание предпринятых действий
**Результат**: Полученные результаты
**Причина неудачи**: Анализ причин неудачи

### Инциденты
#### Инцидент N (YYYY-MM-DD)
```

---

## Актуальные проблемы

## [P250828-02] - Несоответствие веток в Git репозитории

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Высокий

### Описание
Локальный Git репозиторий использовал ветку `master`, в то время как документация и GitHub настроены на ветку `main`. Это приводило к созданию дополнительных веток и путанице в истории коммитов.

### Полезные ссылки
- [Git Branch Management](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management)
- [GitHub Default Branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/changing-the-default-branch)
- [Git Configuration](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)

### История решения
#### Чат 1: "Анализ и исправление проблемы веток в Git репозитории"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Настройка `git config --global init.defaultBranch main`
2. Переименование локальной ветки: `git branch -m master main`
3. Обновление скрипта синхронизации для автоматического переименования
4. Удаление старой ветки на GitHub: `git push origin --delete master`
5. Синхронизация с GitHub через обновленный алиас `run-sync-github.sh`

**Результат**: Проблема решена, все коммиты теперь в ветке `main`
**Статус**: Решена

### Техническое решение
1. **Настройка ветки по умолчанию**: `git config --global init.defaultBranch main`
2. **Переименование локальной ветки**: `git branch -m master main`
3. **Автоматическая проверка в скрипте синхронизации**:
   ```bash
   if git branch --show-current | grep -q "master"; then
       echo "🔧 Переименование ветки master в main..."
       git branch -m master main
   fi
   ```
4. **Удаление старой ветки на GitHub**: `git push origin --delete master`

### Профилактические меры
- Добавлена проверка ветки в скрипт синхронизации
- Обновлена документация по работе с GitHub
- Настроена ветка `main` по умолчанию в Git конфигурации

### Инциденты
#### Инцидент 1 (2025-08-28)
Обнаружено несоответствие: локальная ветка `master`, GitHub ветка `main`, документация указывает на `main`

---

## [P250817-02] - Проблема блокировки терминала из-за "проблемы pager"

**Статус**: Актуальна
**Дата выявления**: 2025-08-17
**Приоритет**: Критический

### Описание
При выполнении команд git в терминале происходит блокировка из-за активации pager (less/more). Это критически блокирует работу с проектом.

### Полезные ссылки
- [Git Pager Configuration](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration#_core_pager)
- [Desktop Commander MCP](https://github.com/desktop-commander/desktop-commander-mcp)
- [Robust Pager Protection Script](./robust-pager-protection.sh)

### История решения
#### Чат 1: "ЭТАП 10: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ И РАЗВЕРТЫВАНИЕ VUEGE"
##### Попытка 1 (2025-08-27)
**Действия**: Создан защитный скрипт robust-pager-protection.sh, настроены алиасы git
**Результат**: Проблема частично решена, но требует постоянного внимания
**Причина неудачи**: Проблема системного уровня, требует постоянной профилактики

### Инциденты
#### Инцидент 1 (2025-08-17)
Блокировка терминала при выполнении `git status` без флага `--porcelain`

---

## [P250825-01] - Проблема цикла чтения файлов в AI ассистенте

**Статус**: Актуальна
**Дата выявления**: 2025-08-25
**Приоритет**: Средний

### Описание
При работе с AI ассистентом происходит цикл чтения файлов, что приводит к неэффективности и потенциальным блокировкам.

### Полезные ссылки
- [Cursor IDE Documentation](https://cursor.sh/docs)
- [AI Assistant Best Practices](https://docs.cursor.sh/ai/chat)

### История решения
#### Чат 1: "ЭТАП 10: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ И РАЗВЕРТЫВАНИЕ VUEGE"
##### Попытка 1 (2025-08-27)
**Действия**: Использование desktop-commander-mcp для безопасной работы с файлами
**Результат**: Проблема частично решена
**Причина неудачи**: Проблема архитектурного уровня AI ассистента

---

## [P250827-01] - Проблема GraphQL мутаций в VUEGE

**Статус**: Актуальна
**Дата выявления**: 2025-08-27
**Приоритет**: Средний

### Описание
GraphQL мутации (CREATE, UPDATE, DELETE) возвращают INTERNAL_ERROR, что ограничивает функциональность системы. READ операции работают идеально.

### Полезные ссылки
- [Spring GraphQL Documentation](https://docs.spring.io/spring-graphql/docs/current/reference/html/)
- [GraphQL Mutations Best Practices](https://graphql.org/learn/queries/#mutations)
- [Spring Boot Validation](https://spring.io/guides/gs/validating-form-input/)

### История решения
#### Чат 1: "ЭТАП 10: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ И РАЗВЕРТЫВАНИЕ VUEGE"
##### Попытка 1 (2025-08-27)
**Действия**: CRUD тестирование выявило проблему с мутациями
**Результат**: Проблема идентифицирована, требуется доработка Backend
**Причина неудачи**: Недостаточная валидация и обработка ошибок в GraphQL контроллерах

### Инциденты
#### Инцидент 1 (2025-08-27)
Ошибка `INTERNAL ERROR for 44f6280c-1931-4c0c-113f-10c4e31034d4` при создании организационной единицы

---

## Решенные проблемы

## [P250817-01] - Проблема с Liquibase миграциями

**Статус**: Решена
**Дата выявления**: 2025-08-17
**Дата решения**: 2025-08-17
**Приоритет**: Критический

### Описание
Проблемы с выполнением Liquibase миграций при запуске Spring Boot приложения.

### История решения
#### Чат 1: "ЭТАП 2: Полное исправление Liquibase"
##### Попытка 1 (2025-08-17)
**Действия**: Исправлены SQL скрипты, добавлены недостающие поля, исправлена структура таблиц
**Результат**: Миграции выполняются успешно
**Статус**: Решена

---

## [P250825-02] - Проблема отображения опций в q-select компоненте

**Статус**: Решена
**Дата выявления**: 2025-08-25
**Дата решения**: 2025-08-27
**Приоритет**: Высокий

### Описание
В компоненте StatesPage.vue выпадающий список "Тип государства" (q-select) не отображал все доступные опции. При открытии выпадающего списка показывалась только одна опция (текущее выбранное значение) вместо всех 4 опций из массива stateTypes.

### Полезные ссылки
- [Quasar q-select Documentation](https://quasar.dev/vue-components/select)
- [Vue 3 Reactivity](https://vuejs.org/guide/extras/reactivity-in-depth.html)
- [Quasar Virtual Scrolling](https://quasar.dev/vue-components/select#virtual-scrolling)

### История решения
#### Чат 1: "ЭТАП 10: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ И РАЗВЕРТЫВАНИЕ VUEGE"
##### Попытка 1 (2025-08-27)
**Действия**: Добавлены параметры option-value="value", option-label="label", emit-value, map-options
**Результат**: Проблема не решена
**Причина неудачи**: Неправильная структура данных

##### Попытка 2 (2025-08-27)
**Действия**: Сделан массив stateTypes реактивным (ref())
**Результат**: Проблема не решена
**Причина неудачи**: Проблема не в реактивности

##### Попытка 3 (2025-08-27)
**Действия**: Использован computed для stateTypes, исправлены функции getStateTypeLabel и editState
**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Использован computed для stateTypes**:
   ```javascript
   const stateTypes = computed(() => [
     { label: 'Государство', value: 'STATE' },
     { label: 'Правительство', value: 'GOVERNMENT' },
     { label: 'Коммерческая', value: 'COMMERCIAL' },
     { label: 'Империя', value: 'EMPIRE' }
   ])
   ```

2. **Правильно настроены параметры q-select**:
   ```html
   <q-select
     v-model="form.type"
     :options="stateTypes"
     label="Тип государства"
     outlined
     dense
     class="q-mb-md"
     option-value="value"
     option-label="label"
     emit-value
     map-options
     clearable
   />
   ```

3. **Исправлены функции**:
   - `getStateTypeLabel` - использует `stateTypes.value`
   - `editState` - использует `stateTypes.value`

### Созданные тестовые страницы
- `/minimal-test` - минимальный тест q-select
- `/force-render-test` - тест принудительного рендеринга
- `/virtual-scroll-test` - тест отключения виртуального скроллинга
- `/string-test` - тест со строками
- `/qselect-test` - комплексный тест различных конфигураций

### Инциденты
#### Инцидент 1 (2025-08-27)
q-select отображал только одну опцию вместо всех четырех в выпадающем списке

#### Инцидент 2 (2025-08-28)
**Контекст**: Тестирование CRUD операций страницы "Организации"
**Симптомы**: 
- В комбобоксах страницы организаций при фильтрации по типу отображалась только активная организация
- При добавлении и редактировании организации в списках комбобоксов показывалась только одна опция
- Проблема аналогична ранее решенной P250825-02 на странице "Государства"

**Действия по решению**:
1. Изучение решения проблемы P250825-02 из документации
2. Применение аналогичного решения к странице организаций:
   - Замена q-select на HTML select (временное решение)
   - Использование computed для organizationTypes
   - Добавление вспомогательных методов getOrganizationTypeLabel(), getStatusLabel()
   - Отладочное логирование для диагностики
3. Тестирование исправлений:
   - Проверка фильтров "Тип организации" и "Статус"
   - Тестирование форм создания и редактирования
   - Проверка отображения в таблице

**Результат**: Проблема успешно решена, все комбобоксы отображают все доступные опции корректно

**Техническое решение**:
```javascript
// Использование computed для правильной реактивности
const organizationTypes = computed(() => [
  { label: 'Империя', value: 'EMPIRE' },
  { label: 'Государство', value: 'STATE' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  // ... остальные опции
])

// Вспомогательные методы для получения лейблов
const getOrganizationTypeLabel = (type: string): string => {
  const typeOption = organizationTypes.value.find(t => t.value === type)
  return typeOption ? typeOption.label : type
}
```

**HTML структура**:
```html
<!-- Временное решение: обычный HTML select -->
<div class="q-field q-field--outlined q-field--dense">
  <div class="q-field__control">
    <div class="q-field__control-container">
      <select v-model="form.type" class="q-field__native q-placeholder">
        <option value="">Выберите тип организации</option>
        <option value="EMPIRE">Империя</option>
        <!-- ... остальные опции -->
      </select>
    </div>
  </div>
  <div class="q-field__label">Тип организации *</div>
</div>
```

**Статус**: Решена ✅
**Влияние**: Улучшена пользовательская доступность страницы организаций
**Профилактика**: Создан шаблон решения для применения к другим страницам с аналогичными проблемами

---

## [P250825-03] - Неправильная кнопка при редактировании в форме "Государства"

**Статус**: Решена
**Дата выявления**: 2025-08-25
**Дата решения**: 2025-08-25
**Приоритет**: Высокий

### Описание
При редактировании записи в форме "Государства" показывалась кнопка "СОЗДАТЬ" вместо "СОХРАНИТЬ". Это приводило к созданию новой записи вместо обновления существующей.

### Полезные ссылки
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Quasar Dialog Documentation](https://quasar.dev/vue-components/dialog)

### История решения
#### Чат 1: "CRUD операции страницы 'Государства'"
##### Попытка 1 (2025-08-25)
**Действия**: Изменен порядок операций в функции editState() - сначала resetForm(), затем editingState.value = state
**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
```javascript
const editState = (state: any) => {
  // 1. Сначала сбрасываем форму
  resetForm()
  
  // 2. Затем устанавливаем режим редактирования
  editingState.value = state
  
  // 3. Заполняем форму данными
  form.name = state.name
  // ... остальные поля
}
```

### Инциденты
#### Инцидент 1 (2025-08-25)
При редактировании записи "Византийская империя" показывалась кнопка "СОЗДАТЬ" вместо "СОХРАНИТЬ"

---

## [P250825-04] - Удаление без подтверждения в форме "Государства"

**Статус**: Решена
**Дата выявления**: 2025-08-25
**Дата решения**: 2025-08-25
**Приоритет**: Критический

### Описание
При нажатии кнопки удаления запись удалялась сразу, не дожидаясь подтверждения пользователя. Диалог подтверждения и сообщение об успешном удалении появлялись одновременно.

### Полезные ссылки
- [Quasar Dialog API](https://quasar.dev/vue-components/dialog#api)
- [Vue 3 Async/Await](https://vuejs.org/guide/best-practices/async-await.html)

### История решения
#### Чат 1: "CRUD операции страницы 'Государства'"
##### Попытка 1 (2025-08-25)
**Действия**: Использование Promise с обработчиками событий .onOk(), .onCancel(), .onDismiss()
**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
```javascript
const confirmed = await new Promise((resolve) => {
  $q.dialog({
    title: 'Подтверждение удаления',
    message: `Вы уверены, что хотите удалить организацию "${state.name}"?`,
    ok: { label: 'Удалить', color: 'negative' },
    cancel: { label: 'Отмена', color: 'primary' },
    persistent: true
  }).onOk(() => {
    console.log('✅ Пользователь нажал "Удалить"')
    resolve(true)
  }).onCancel(() => {
    console.log('❌ Пользователь нажал "Отмена"')
    resolve(false)
  }).onDismiss(() => {
    console.log('❌ Диалог закрыт без ответа')
    resolve(false)
  })
})
```

### Инциденты
#### Инцидент 1 (2025-08-25)
Удаление записи "Тестовая организация" происходило без подтверждения пользователя

---

## [P250825-05] - Отсутствие поля исторического периода в форме "Государства"

**Статус**: Решена
**Дата выявления**: 2025-08-25
**Дата решения**: 2025-08-25
**Приоритет**: Средний

### Описание
В форме создания/редактирования отсутствовало поле для выбора исторического периода. Данные о периоде не сохранялись при создании/редактировании записей.

### Полезные ссылки
- [HTML Select Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select)
- [Vue 3 Form Handling](https://vuejs.org/guide/essentials/forms.html)

### История решения
#### Чат 1: "CRUD операции страницы 'Государства'"
##### Попытка 1 (2025-08-25)
**Действия**: Добавлен select с историческими периодами и автоматическое определение периода на основе даты основания
**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Добавление поля в форму**:
   ```html
   <select v-model="form.historicalPeriodId" aria-label="Исторический период">
     <option value="1">Раннее Средневековье (476-1000)</option>
     <option value="2">Высокое Средневековье (1000-1300)</option>
     <option value="3">Позднее Средневековье (1300-1492)</option>
     <option value="4">Новое время (1492-1789)</option>
     <option value="5">Новейшее время (1789-2025)</option>
   </select>
   ```

2. **Автоматическое определение периода**:
   ```javascript
   const foundedYear = parseInt(state.foundedDate?.substring(0, 4) || '1000');
   if (foundedYear < 1000) {
     form.historicalPeriodId = '1'; // Раннее Средневековье
   } else if (foundedYear < 1300) {
     form.historicalPeriodId = '2'; // Высокое Средневековье
   } else if (foundedYear < 1492) {
     form.historicalPeriodId = '3'; // Позднее Средневековье
   } else if (foundedYear < 1789) {
     form.historicalPeriodId = '4'; // Новое время
   } else {
     form.historicalPeriodId = '5'; // Новейшее время
   }
   ```

### Инциденты
#### Инцидент 1 (2025-08-25)
При создании записи "Византийская империя" не было возможности указать исторический период

---

## [P250828-10] - Проблема отображения опций в q-select компоненте страницы организаций

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Высокий

### Описание
В компоненте OrganizationsPage.vue выпадающие списки (q-select) не отображали все доступные опции. При открытии выпадающих списков показывалась только одна опция (текущее выбранное значение) вместо всех опций из массивов organizationTypes и statusOptions. Проблема затрагивала:
- Фильтр "Тип организации" на странице
- Фильтр "Статус" на странице  
- Поле "Тип организации" в форме создания/редактирования

### Полезные ссылки
- [Quasar q-select Documentation](https://quasar.dev/vue-components/select)
- [Vue 3 Reactivity](https://vuejs.org/guide/extras/reactivity-in-depth.html)
- [Решение проблемы P250825-02](./problems.md#p250825-02---проблема-отображения-опций-в-q-select-компоненте)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Изучение решения проблемы P250825-02 из документации
2. Применение аналогичного решения к странице организаций:
   - Замена q-select на HTML select (временное решение)
   - Использование computed для organizationTypes и statusOptions
   - Добавление вспомогательных методов getOrganizationTypeLabel(), getStatusLabel()
   - Отладочное логирование для диагностики
3. Тестирование исправлений

**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Использован computed для organizationTypes**:
   ```javascript
   const organizationTypes = computed(() => [
     { label: 'Империя', value: 'EMPIRE' },
     { label: 'Государство', value: 'STATE' },
     { label: 'Коммерческая', value: 'COMMERCIAL' },
     { label: 'Правительственная', value: 'GOVERNMENT' },
     { label: 'Некоммерческая', value: 'NON_PROFIT' },
     { label: 'Образовательная', value: 'EDUCATIONAL' },
     { label: 'Военная', value: 'MILITARY' },
     { label: 'Религиозная', value: 'RELIGIOUS' },
     { label: 'Другая', value: 'OTHER' }
   ])
   ```

2. **Замена q-select на HTML select**:
   ```html
   <!-- Временное решение: обычный HTML select -->
   <div class="q-field q-field--outlined q-field--dense">
     <div class="q-field__control">
       <div class="q-field__control-container">
         <select v-model="form.type" class="q-field__native q-placeholder">
           <option value="">Выберите тип организации</option>
           <option value="EMPIRE">Империя</option>
           <!-- ... остальные опции -->
         </select>
       </div>
     </div>
     <div class="q-field__label">Тип организации *</div>
   </div>
   ```

3. **Добавлены вспомогательные методы**:
   ```javascript
   const getOrganizationTypeLabel = (type: string): string => {
     const typeOption = organizationTypes.value.find(t => t.value === type)
     return typeOption ? typeOption.label : type
   }

   const getStatusLabel = (status: string): string => {
     const statusOption = statusOptions.value.find(s => s.value === status)
     return statusOption ? statusOption.label : status
   }
   ```

4. **Обновлены колонки таблицы**:
   ```javascript
   const columns = [
     { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
     { name: 'type', label: 'Тип', field: row => getOrganizationTypeLabel(row.type), sortable: true, align: 'left' },
     // ... остальные колонки
   ]
   ```

### Созданные улучшения
- Правильное отображение всех опций в выпадающих списках
- Человекочитаемые лейблы в таблице вместо кодов
- Отладочное логирование для диагностики проблем
- Шаблон решения для применения к другим страницам

### Инциденты
#### Инцидент 1 (2025-08-28)
**Контекст**: Тестирование CRUD операций страницы "Организации"
**Симптомы**: 
- В комбобоксах страницы организаций при фильтрации по типу отображалась только активная организация
- При добавлении и редактировании организации в списках комбобоксов показывалась только одна опция
- Проблема аналогична ранее решенной P250825-02 на странице "Государства"

**Действия по решению**:
1. Изучение решения проблемы P250825-02 из документации
2. Применение аналогичного решения к странице организаций
3. Тестирование исправлений

**Результат**: Проблема успешно решена, все комбобоксы отображают все доступные опции корректно
**Статус**: Решена ✅

---

## [P250828-11] - Несоответствие полей в GraphQL мутации создания организации

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Высокий

### Описание
При попытке создания организации возникала ошибка GraphQL: "The variables input contains a field name 'description' that is not defined for input object type 'OrganizationalUnitInput'". Frontend отправлял поля, которые не поддерживались Backend GraphQL схемой.

### Полезные ссылки
- [GraphQL Introspection](https://graphql.org/learn/introspection/)
- [Spring GraphQL Documentation](https://docs.spring.io/spring-graphql/docs/current/reference/html/)
- [GraphQL Input Types](https://graphql.org/learn/schema/#input-types)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Анализ GraphQL схемы Backend через introspection
2. Приведение полей input в соответствие с OrganizationalUnitInput
3. Удаление неподдерживаемого поля description
4. Добавление обязательных полей isFictional, historicalPeriodId
5. Исправление названий полей (locationId → location, parentOrganizationId → parentUnitId)

**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Анализ GraphQL схемы**:
   ```bash
   curl -X POST http://localhost:8082/api/graphql \
     -H "Content-Type: application/json" \
     -d '{"query": "query IntrospectionQuery { __schema { types { name inputFields { name type { name } } } } }"}' \
     | jq '.data.__schema.types[] | select(.name == "OrganizationalUnitInput")'
   ```

2. **Исправленный input для мутации**:
   ```javascript
   const input: any = {
     name: form.name.trim(),
     type: form.type,
     foundedDate: form.foundedDate,
     dissolvedDate: form.dissolvedDate || null,
     isFictional: form.isFictional,
     historicalPeriodId: '1', // По умолчанию раннее средневековье
     parentUnitId: form.parentOrganizationId || null
   }
   ```

3. **Обновленная форма**:
   ```html
   <!-- Убрано поле description, добавлен чекбокс isFictional -->
   <q-checkbox
     v-model="form.isFictional"
     label="Вымышленная организация"
     class="col-12"
   />
   ```

### Инциденты
#### Инцидент 1 (2025-08-28)
Ошибка GraphQL при создании организации из-за неподдерживаемого поля description

---

## [P250828-12] - Несоответствие enum значений OrganizationType между Frontend и Backend

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Высокий

### Описание
При попытке создания организации с типом "Некоммерческая" возникала ошибка GraphQL: "Invalid input for enum 'OrganizationType'. No value found for name 'NON_PROFIT'". Frontend использовал enum значения, которые не поддерживались Backend GraphQL схемой.

### Полезные ссылки
- [GraphQL Enum Types](https://graphql.org/learn/schema/#enumeration-types)
- [GraphQL Introspection](https://graphql.org/learn/introspection/)
- [Vue 3 Form Handling](https://vuejs.org/guide/essentials/forms.html)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Анализ enum OrganizationType через GraphQL introspection
2. Приведение enum значений в соответствие с Backend схемой
3. Удаление неподдерживаемых типов (NON_PROFIT, EDUCATIONAL, MILITARY, RELIGIOUS, OTHER)
4. Обновление форм и фильтров

**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Анализ enum через introspection**:
   ```bash
   curl -X POST http://localhost:8082/api/graphql \
     -H "Content-Type: application/json" \
     -d '{"query": "query IntrospectionQuery { __schema { types { name enumValues { name } } } }"}' \
     | jq '.data.__schema.types[] | select(.name == "OrganizationType")'
   ```

2. **Исправленный массив organizationTypes**:
   ```javascript
   const organizationTypes = computed(() => [
     { label: 'Империя', value: 'EMPIRE' },
     { label: 'Государство', value: 'STATE' },
     { label: 'Коммерческая', value: 'COMMERCIAL' },
     { label: 'Правительственная', value: 'GOVERNMENT' }
   ])
   ```

3. **Поддерживаемые Backend enum значения**:
   - `STATE` - Государство
   - `GOVERNMENT` - Правительственная  
   - `COMMERCIAL` - Коммерческая
   - `EMPIRE` - Империя

### Инциденты
#### Инцидент 1 (2025-08-28)
Ошибка GraphQL enum при создании организации с типом NON_PROFIT

---

## [P250828-13] - Неработающий поиск и фильтрация на странице организаций

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Средний

### Описание
Поиск и фильтрация на странице организаций не работали. Пользователи не могли искать организации по названию или фильтровать по типу. Проблема была в отсутствии клиентской фильтрации данных в computed свойстве.

### Полезные ссылки
- [Vue 3 Computed Properties](https://vuejs.org/guide/essentials/computed.html)
- [Quasar q-table Documentation](https://quasar.dev/vue-components/table)
- [Решение проблемы поиска на странице государств](./problems.md#p250825-02---проблема-отображения-опций-в-q-select-компоненте)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Анализ реализации поиска на странице государств
2. Применение паттерна клиентской фильтрации к странице организаций
3. Добавление фильтрации по названию, типу и статусу
4. Тестирование всех сценариев поиска

**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Добавлена клиентская фильтрация**:
   ```javascript
   const organizations = computed(() => {
     const data = result.value?.organizationalUnits || []
     
     // Фильтрация по поиску
     let filtered = data
     if (searchQuery.value) {
       filtered = filtered.filter(org => 
         org.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
         org.type.toLowerCase().includes(searchQuery.value.toLowerCase())
       )
     }
     
     // Фильтрация по типу
     if (selectedType.value) {
       filtered = filtered.filter(org => org.type === selectedType.value)
     }
     
     return filtered
   })
   ```

2. **Реализован поиск по названию** - регистронезависимый поиск
3. **Реализован поиск по типу** - поиск по enum значению
4. **Реализована фильтрация по типу** - точное совпадение
5. **Добавлена фильтрация по статусу** - с проверкой наличия поля

### Инциденты
#### Инцидент 1 (2025-08-28)
Поиск и фильтры не работали из-за отсутствия клиентской фильтрации в computed свойстве

---

## [P250828-14] - Отсутствие поля "Статус" в таблице и формах организаций

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Средний

### Описание
На странице организаций присутствовал фильтр по статусу, но поле "Статус" отсутствовало в таблице и формах создания/редактирования. Это создавало несоответствие в интерфейсе и затрудняло понимание пользователем текущего состояния организаций.

### Полезные ссылки
- [Vue 3 Computed Properties](https://vuejs.org/guide/essentials/computed.html)
- [Quasar q-table Documentation](https://quasar.dev/vue-components/table)
- [JavaScript Date Handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Анализ GraphQL API для определения доступных полей
2. Создание логики определения статуса на основе поля dissolvedDate
3. Добавление колонки "Статус" в таблицу организаций
4. Добавление поля "Статус" в формы создания/редактирования
5. Исправление фильтрации по статусу

**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Логика определения статуса**:
   ```javascript
   const getOrganizationStatus = (org: any): string => {
     const dissolvedDate = org.dissolvedDate || org.dissolvedDate
     
     if (dissolvedDate) {
       const dissolvedDateObj = new Date(dissolvedDate)
       const currentDate = new Date()
       
       if (dissolvedDateObj < currentDate) {
         return 'Ликвидированная'
       } else {
         return 'Неактивная'
       }
     }
     return 'Активная'
   }
   ```

2. **Добавлена колонка в таблицу**:
   ```javascript
   { name: 'status', label: 'Статус', field: row => getOrganizationStatus(row), sortable: true, align: 'center' }
   ```

3. **Добавлено поле в форму**:
   ```html
   <div class="q-field q-field--outlined q-field--dense col-12 col-sm-6">
     <div class="q-field__control">
       <div class="q-field__control-container">
         <div class="q-field__native q-placeholder" style="padding: 8px; color: #666;">
           {{ getOrganizationStatus(form) }}
         </div>
       </div>
     </div>
     <div class="q-field__label">Статус</div>
   </div>
   ```

4. **Исправлена фильтрация**:
   ```javascript
   if (selectedStatus.value) {
     filtered = filtered.filter(org => {
       const orgStatus = getOrganizationStatus(org)
       return orgStatus === getStatusLabel(selectedStatus.value!)
     })
   }
   ```

### Инциденты
#### Инцидент 1 (2025-08-28)
Фильтр по статусу присутствовал, но поле "Статус" отсутствовало в таблице и формах

---

## [P250828-15] - Невозможность изменения статуса в формах создания и редактирования организаций

**Статус**: Решена
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Средний

### Описание
В формах создания и редактирования организаций поле "Статус" отображалось как статичный текст, а не как редактируемый комбобокс. Пользователи не могли изменять статус организации, что ограничивало функциональность интерфейса.

### Полезные ссылки
- [Vue 3 Reactive Forms](https://vuejs.org/guide/essentials/forms.html)
- [Quasar q-select Documentation](https://quasar.dev/vue-components/select)
- [JavaScript Date Manipulation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Анализ текущего отображения поля "Статус" в формах
2. Создание опций статусов для форм (formStatusOptions)
3. Добавление поля status в реактивное состояние формы
4. Создание функций синхронизации между статусом и датой ликвидации
5. Замена статичного текста на комбобокс в формах
6. Добавление поля даты ликвидации для неактивных статусов

**Результат**: Проблема решена
**Статус**: Решена

### Техническое решение
1. **Опции статусов для форм**:
   ```javascript
   const formStatusOptions = computed(() => [
     { label: 'Активная', value: 'active' },
     { label: 'Неактивная', value: 'inactive' },
     { label: 'Ликвидированная', value: 'dissolved' }
   ])
   ```

2. **Поле статуса в форме**:
   ```javascript
   const form = reactive({
     // ... другие поля
     status: 'active' // Добавляем поле статуса
   })
   ```

3. **Функции синхронизации**:
   ```javascript
   // Обновление статуса при изменении даты ликвидации
   const updateStatusFromDissolvedDate = () => {
     if (!form.dissolvedDate) {
       form.status = 'active'
     } else {
       const dissolvedDate = new Date(form.dissolvedDate)
       const currentDate = new Date()
       
       if (dissolvedDate < currentDate) {
         form.status = 'dissolved'
       } else {
         form.status = 'inactive'
       }
     }
   }

   // Обновление даты ликвидации при изменении статуса
   const updateDissolvedDateFromStatus = () => {
     switch (form.status) {
       case 'active':
         form.dissolvedDate = ''
         break
       case 'inactive':
         const futureDate = new Date()
         futureDate.setFullYear(futureDate.getFullYear() + 1)
         form.dissolvedDate = futureDate.toISOString().split('T')[0]
         break
       case 'dissolved':
         const pastDate = new Date()
         pastDate.setFullYear(pastDate.getFullYear() - 1)
         form.dissolvedDate = pastDate.toISOString().split('T')[0]
         break
     }
   }
   ```

4. **Комбобокс статуса в форме**:
   ```html
   <select v-model="form.status" class="q-field__native q-placeholder" @change="updateDissolvedDateFromStatus">
     <option v-for="option in formStatusOptions" :key="option.value" :value="option.value">
       {{ option.label }}
     </option>
   </select>
   ```

5. **Поле даты ликвидации**:
   ```html
   <q-input
     v-if="form.status !== 'active'"
     v-model="form.dissolvedDate"
     label="Дата ликвидации"
     type="date"
     outlined
     dense
     class="col-12 col-sm-6"
     @update:model-value="updateStatusFromDissolvedDate"
   />
   ```

### Инциденты
#### Инцидент 1 (2025-08-28)
Поле "Статус" отображалось как статичный текст, а не как редактируемый комбобокс

---

## [P250828-01] - Общие проблемы CRUD операций на страницах сущностей

**Статус**: Актуальна
**Дата выявления**: 2025-08-28
**Приоритет**: Высокий

### Описание
Типичные проблемы, возникающие при реализации CRUD операций на страницах сущностей в Vue.js приложениях с Quasar Framework. Эти проблемы могут повторяться на разных страницах и требуют системного подхода к решению.

### Категории проблем

#### 1. **Проблемы отображения данных**
- Неправильное отображение опций в выпадающих списках
- Проблемы с реактивностью данных
- Ошибки в структуре таблиц и форм

#### 2. **Проблемы режимов работы форм**
- Неправильное различение режимов создания и редактирования
- Неправильные кнопки в диалогах (Создать/Сохранить)

---

## [P250828-16] - Проблема с отступами страниц в Quasar Framework

**Статус**: Решена ✅
**Дата выявления**: 2025-08-28
**Дата решения**: 2025-08-28
**Приоритет**: Высокий

### Описание
При попытке установить отступы 5px слева и справа для фреймов (карточек) на странице организаций отступы не изменялись, несмотря на применение различных CSS техник. Проблема была особенно критична для мобильных устройств, где большие отступы (32px) делали работу практически невозможной.

### Полезные ссылки
- [Quasar Framework CSS Addon Documentation](https://quasar.dev/style/spacing#breakpoint-aware-spacing)
- [Stack Overflow - Margin/Padding on mobile Quasar Framework](https://stackoverflow.com/questions/50948572/margin-padding-on-mobile-quasar-framework-vuejs/66727807#66727807)
- [CSS Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)

### История решения
#### Чат 1: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Добавление inline стилей с `!important` к карточкам
2. Использование CSS классов с `!important`
3. Применение специфичных селекторов для переопределения Quasar стилей

**Результат**: Проблема не решена
**Причина неудачи**: Quasar использует очень специфичные CSS правила, которые переопределяют пользовательские стили

##### Попытка 2 (2025-08-28)
**Действия**: 
1. Включение CSS Addon в Quasar конфигурации
2. Применение встроенных адаптивных классов Quasar
3. Использование классов q-pa-sm-md и q-ma-xs-sm

**Результат**: Частичное решение, но отступы все еще были большими
**Причина неудачи**: Проблема была в глобальных стилях #app

##### Попытка 3 (2025-08-28) - УСПЕШНАЯ
**Действия**: 
1. Анализ DevTools Elements panel показал проблему в глобальных стилях
2. Выявление `padding: 2rem` (32px) в `style.css` для `#app`
3. Изменение на `padding: 2px` в `style.css`
4. Добавление стилей для `q-layout` в `App.vue`
5. Применение `!important` для переопределения стилей

**Результат**: Проблема полностью решена ✅
**Техническое решение**: Изменение глобальных стилей в `style.css` и `App.vue`

### Технические попытки решения
1. **Inline стили с !important**:
   ```html
   <q-card style="margin-left: 5px !important; margin-right: 5px !important;">
   ```

2. **CSS классы с !important**:
   ```css
   .q-card.q-mx-xs {
     margin-left: 5px !important;
     margin-right: 5px !important;
   }
   ```

3. **Специфичные селекторы**:
   ```css
   div.q-page > div > .q-card {
     margin-left: 5px !important;
     margin-right: 5px !important;
   }
   ```

4. **Изменение класса страницы**:
   ```html
   <q-page class="q-pa-none" style="padding: 5px !important;">
   ```

### Возможные причины проблемы
1. **Высокая специфичность Quasar CSS** - фреймворк использует очень специфичные селекторы
2. **CSS-in-JS или динамические стили** - Quasar может применять стили программно
3. **Порядок загрузки CSS** - пользовательские стили загружаются раньше Quasar стилей
4. **Глобальные стили Quasar** - фреймворк может применять глобальные стили, которые переопределяют локальные

### Рекомендации для будущего решения
1. **Использование CSS Custom Properties** - переопределение CSS переменных Quasar
2. **Создание кастомных компонентов** - обертывание q-card в собственные компоненты
3. **Использование CSS Modules** - изоляция стилей от глобальных
4. **Анализ CSS специфичности** - использование инструментов для анализа приоритетов CSS
5. **Использование Quasar Theme Builder** - настройка темы через официальные инструменты

### Инциденты
#### Инцидент 1 (2025-08-28)
**Контекст**: Настройка отступов страницы организаций
**Симптомы**: 
- Отступы слева и справа не изменялись при применении CSS стилей
- Inline стили с `!important` не работали
- Специфичные селекторы не переопределяли Quasar стили

**Действия по решению**:
1. Применение inline стилей к карточкам
2. Использование CSS классов с `!important`
3. Применение специфичных селекторов
4. Изменение класса страницы
5. Упрощение CSS правил

**Результат**: Проблема не решена, требуется системное исследование
**Статус**: Актуальна ⚠️
- Проблемы с инициализацией данных формы

#### 3. **Проблемы подтверждения операций**
- Отсутствие подтверждения для критических операций
- Неправильная работа диалогов подтверждения
- Удаление без ожидания ответа пользователя

#### 4. **Проблемы валидации**
- Отсутствие валидации обязательных полей
- Неправильная обработка ошибок валидации
- Отсутствие обратной связи пользователю

#### 5. **Проблемы интеграции с Backend**
- Ошибки в GraphQL мутациях
- Проблемы с обработкой ответов API
- Отсутствие обработки ошибок сети

### Полезные ссылки
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Quasar Framework Documentation](https://quasar.dev/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Vue 3 Form Validation](https://vuejs.org/guide/essentials/forms.html#validation)

### Частные случаи (решенные проблемы)

#### P250825-02: Проблема отображения опций в q-select компоненте
- **Симптом**: q-select отображал только одну опцию вместо всех
- **Решение**: Использование computed для stateTypes, правильная настройка параметров

#### P250828-10: Проблема отображения опций в q-select компоненте страницы организаций
- **Симптом**: q-select отображал только одну опцию вместо всех в фильтрах и формах
- **Решение**: Замена q-select на HTML select, использование computed для organizationTypes

#### P250828-11: Несоответствие полей в GraphQL мутации создания организации
- **Симптом**: Ошибка GraphQL из-за неподдерживаемого поля description
- **Решение**: Приведение полей input в соответствие с OrganizationalUnitInput

#### P250828-12: Несоответствие enum значений OrganizationType
- **Симптом**: Ошибка GraphQL enum при использовании неподдерживаемых типов
- **Решение**: Приведение enum значений в соответствие с Backend схемой

#### P250828-13: Неработающий поиск и фильтрация на странице организаций
- **Симптом**: Поиск и фильтры не работали из-за отсутствия клиентской фильтрации
- **Решение**: Добавление клиентской фильтрации в computed свойство organizations

#### P250828-14: Отсутствие поля "Статус" в таблице и формах организаций
- **Симптом**: Фильтр по статусу присутствовал, но поле "Статус" отсутствовало в интерфейсе
- **Решение**: Создание логики определения статуса на основе поля dissolvedDate

#### P250828-15: Невозможность изменения статуса в формах создания и редактирования организаций
- **Симптом**: Поле "Статус" отображалось как статичный текст, а не как редактируемый комбобокс
- **Решение**: Добавление комбобокса для выбора статуса с автоматической синхронизацией даты ликвидации

#### P250825-03: Неправильная кнопка при редактировании
- **Симптом**: При редактировании показывалась кнопка "СОЗДАТЬ" вместо "СОХРАНИТЬ"
- **Решение**: Правильный порядок операций в editState()

#### P250825-04: Удаление без подтверждения
- **Симптом**: Удаление происходило сразу, не дожидаясь ответа пользователя
- **Решение**: Promise с обработчиками событий для диалога

#### P250825-05: Отсутствие поля исторического периода
- **Симптом**: В форме не было поля для выбора исторического периода
- **Решение**: Добавление select с автоматическим определением периода

### Чек-лист для проверки новых страниц

#### ✅ Отображение данных
- [ ] Выпадающие списки отображают все опции
- [ ] Таблицы корректно отображают данные
- [ ] Реактивность данных работает правильно

#### ✅ Режимы работы форм
- [ ] Правильное различение создания и редактирования
- [ ] Корректные кнопки в диалогах
- [ ] Правильная инициализация данных формы

#### ✅ Подтверждение операций
- [ ] Критические операции требуют подтверждения
- [ ] Диалоги подтверждения работают корректно
- [ ] Удаление ждет ответа пользователя

#### ✅ Валидация
- [ ] Обязательные поля проверяются
- [ ] Ошибки валидации отображаются пользователю
- [ ] Форма не отправляется при ошибках

#### ✅ Интеграция с Backend
- [ ] GraphQL мутации работают корректно
- [ ] Ошибки API обрабатываются
- [ ] Состояние загрузки отображается

### Технические решения (шаблоны)

#### 1. **Правильная настройка q-select**
```javascript
const options = computed(() => [
  { label: 'Опция 1', value: 'VALUE1' },
  { label: 'Опция 2', value: 'VALUE2' }
])

<q-select
  v-model="form.field"
  :options="options"
  option-value="value"
  option-label="label"
  emit-value
  map-options
/>
```

#### 2. **Правильный порядок операций редактирования**
```javascript
const editItem = (item: any) => {
  resetForm()           // 1. Сброс формы
  editingItem.value = item  // 2. Установка режима
  // Заполнение формы   // 3. Заполнение данными
}
```

#### 3. **Подтверждение критических операций**
```javascript
const confirmed = await new Promise((resolve) => {
  $q.dialog({...})
    .onOk(() => resolve(true))
    .onCancel(() => resolve(false))
    .onDismiss(() => resolve(false))
})
```

#### 4. **Валидация обязательных полей**
```javascript
const saveItem = async () => {
  if (!form.name.trim()) {
    $q.notify({
      type: 'negative',
      message: 'Название обязательно для заполнения'
    })
    return
  }
  // Сохранение
}
```

### История решения
#### Чат 1: "CRUD операции страницы 'Государства'"
##### Попытка 1 (2025-08-25)
**Действия**: Выявлены и решены 4 частные проблемы CRUD операций
**Результат**: Создан чек-лист и технические решения для предотвращения повторения
**Статус**: Актуальна (требует проверки на других страницах)

#### Чат 2: "Тестирование CRUD операций страницы 'Организации'"
##### Попытка 1 (2025-08-28)
**Действия**: 
1. Комплексное тестирование CRUD операций страницы организаций
2. Выявление и исправление проблемы P250828-10 с q-select компонентом
3. Применение решения проблемы P250825-02 к странице организаций
4. Создание инцидента и документации решения

**Результат**: Проблема P250828-10 решена, подтверждена эффективность системного подхода
**Статус**: Актуальна (требует проверки на остальных страницах)

### Инциденты
#### Инцидент 1 (2025-08-25)
Выявлены 4 критические проблемы на странице "Государства", требующие системного решения

#### Инцидент 2 (2025-08-28)
**Контекст**: Тестирование CRUD операций страницы "Организации"
**Симптомы**: 
- Повторение проблемы P250825-02 на странице организаций
- Неправильное отображение опций в q-select компонентах
- Проблемы с фильтрами и формами создания/редактирования

**Действия**: 
1. Применение решения проблемы P250825-02 к странице организаций
2. Создание проблемы P250828-10 для систематизации
3. Документирование решения и создание инцидента

**Результат**: Подтверждена эффективность системного подхода к решению CRUD проблем
**Статус**: Решена ✅

#### Инцидент 3 (2025-08-28)
**Контекст**: Тестирование создания организаций
**Симптомы**: 
- Ошибка GraphQL: "The variables input contains a field name 'description' that is not defined for input object type 'OrganizationalUnitInput'"
- Несоответствие полей между Frontend и Backend

**Действия**: 
1. Анализ GraphQL схемы Backend через introspection
2. Приведение полей input в соответствие с OrganizationalUnitInput
3. Удаление неподдерживаемого поля description
4. Добавление обязательных полей isFictional, historicalPeriodId

**Результат**: Проблема P250828-11 решена, создание организаций работает
**Статус**: Решена ✅

#### Инцидент 4 (2025-08-28)
**Контекст**: Тестирование создания организаций с разными типами
**Симптомы**: 
- Ошибка GraphQL: "Invalid input for enum 'OrganizationType'. No value found for name 'NON_PROFIT'"
- Несоответствие enum значений между Frontend и Backend

**Действия**: 
1. Анализ enum OrganizationType через GraphQL introspection
2. Приведение enum значений в соответствие с Backend схемой
3. Удаление неподдерживаемых типов (NON_PROFIT, EDUCATIONAL, MILITARY, RELIGIOUS, OTHER)
4. Обновление форм и фильтров

**Результат**: Проблема P250828-12 решена, все типы организаций работают
**Статус**: Решена ✅

#### Инцидент 5 (2025-08-28)
**Контекст**: Тестирование поиска и фильтрации на странице организаций
**Симптомы**: 
- Поиск по названию не работал
- Фильтры по типу организации не работали
- Отсутствие клиентской фильтрации данных

**Действия**: 
1. Анализ реализации поиска на странице государств
2. Применение паттерна клиентской фильтрации к странице организаций
3. Добавление фильтрации по названию, типу и статусу
4. Тестирование всех сценариев поиска

**Результат**: Проблема P250828-13 решена, поиск и фильтрация работают корректно
**Статус**: Решена ✅

#### Инцидент 6 (2025-08-28)
**Контекст**: Тестирование отображения статуса организаций
**Симптомы**: 
- Фильтр по статусу присутствовал, но поле "Статус" отсутствовало в таблице
- Поле "Статус" отсутствовало в формах создания/редактирования
- Несоответствие в интерфейсе

**Действия**: 
1. Анализ GraphQL API для определения доступных полей
2. Создание логики определения статуса на основе поля dissolvedDate
3. Добавление колонки "Статус" в таблицу организаций
4. Добавление поля "Статус" в формы
5. Исправление фильтрации по статусу

**Результат**: Проблема P250828-14 решена, поле "Статус" добавлено во все места интерфейса
**Статус**: Решена ✅

#### Инцидент 7 (2025-08-28)
**Контекст**: Тестирование редактирования статуса организаций
**Симптомы**: 
- Поле "Статус" отображалось как статичный текст в формах
- Невозможность изменения статуса организации
- Ограниченная функциональность интерфейса

**Действия**: 
1. Анализ текущего отображения поля "Статус" в формах
2. Создание опций статусов для форм (formStatusOptions)
3. Добавление поля status в реактивное состояние формы
4. Создание функций синхронизации между статусом и датой ликвидации
5. Замена статичного текста на комбобокс в формах
6. Добавление поля даты ликвидации для неактивных статусов

**Результат**: Проблема P250828-15 решена, пользователи могут изменять статус через комбобокс
**Статус**: Решена ✅

---

## Проблемы, потерявшие актуальность

## [P250817-03] - Проблема с Node.js версией

**Статус**: Потеряла актуальность
**Дата выявления**: 2025-08-17
**Дата закрытия**: 2025-08-17
**Приоритет**: Средний

### Описание
Устаревшая версия Node.js в проекте.

### История решения
#### Чат 1: "ЭТАП 3: Обновление Node.js"
##### Попытка 1 (2025-08-17)
**Действия**: Обновлен Node.js до версии 20+
**Результат**: Проблема решена
**Статус**: Потеряла актуальность
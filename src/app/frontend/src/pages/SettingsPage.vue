<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Настройки</h4>
        <p class="text-body1 text-grey-7">
          Конфигурация системы и пользовательские настройки
        </p>
      </div>
    </div>

    <div class="row q-gutter-lg">
      <!-- Общие настройки -->
      <q-card class="col-12 col-md-6">
        <q-card-section>
          <div class="text-h6">Общие настройки</div>
        </q-card-section>
        
        <q-card-section>
          <q-input
            v-model="settings.language"
            label="Язык интерфейса"
            outlined
            dense
            class="q-mb-md"
          >
            <template v-slot:append>
              <q-icon name="language" />
            </template>
          </q-input>
          
          <q-input
            v-model="settings.timezone"
            label="Часовой пояс"
            outlined
            dense
            class="q-mb-md"
          >
            <template v-slot:append>
              <q-icon name="schedule" />
            </template>
          </q-input>
          
          <q-input
            v-model="settings.dateFormat"
            label="Формат даты"
            outlined
            dense
            class="q-mb-md"
          >
            <template v-slot:append>
              <q-icon name="event" />
            </template>
          </q-input>
          
          <q-toggle
            v-model="settings.darkMode"
            label="Темная тема"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.notifications"
            label="Уведомления"
            color="primary"
            class="q-mb-md"
          />
        </q-card-section>
      </q-card>

      <!-- Настройки отображения -->
      <q-card class="col-12 col-md-6">
        <q-card-section>
          <div class="text-h6">Настройки отображения</div>
        </q-card-section>
        
        <q-card-section>
          <q-input
            v-model.number="settings.itemsPerPage"
            label="Элементов на странице"
            type="number"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-select
            v-model="settings.defaultSort"
            :options="sortOptions"
            label="Сортировка по умолчанию"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.showFilters"
            label="Показывать фильтры по умолчанию"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.autoRefresh"
            label="Автообновление данных"
            color="primary"
            class="q-mb-md"
          />
        </q-card-section>
      </q-card>

      <!-- Настройки API -->
      <q-card class="col-12 col-md-6">
        <q-card-section>
          <div class="text-h6">Настройки API</div>
        </q-card-section>
        
        <q-card-section>
          <q-input
            v-model="settings.apiUrl"
            label="URL API"
            outlined
            dense
            class="q-mb-md"
          >
            <template v-slot:append>
              <q-icon name="api" />
            </template>
          </q-input>
          
          <q-input
            v-model="settings.graphqlEndpoint"
            label="GraphQL endpoint"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-input
            v-model.number="settings.requestTimeout"
            label="Таймаут запросов (мс)"
            type="number"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.enableCaching"
            label="Включить кэширование"
            color="primary"
            class="q-mb-md"
          />
        </q-card-section>
      </q-card>

      <!-- Настройки безопасности -->
      <q-card class="col-12 col-md-6">
        <q-card-section>
          <div class="text-h6">Безопасность</div>
        </q-card-section>
        
        <q-card-section>
          <q-toggle
            v-model="settings.requireAuth"
            label="Требовать аутентификацию"
            color="primary"
            class="q-mb-md"
          />
          
          <q-input
            v-model.number="settings.sessionTimeout"
            label="Таймаут сессии (мин)"
            type="number"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.auditLog"
            label="Вести журнал аудита"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.dataEncryption"
            label="Шифрование данных"
            color="primary"
            class="q-mb-md"
          />
        </q-card-section>
      </q-card>
    </div>

    <!-- Кнопки действий -->
    <div class="row q-mt-lg">
      <div class="col-12 text-center">
        <q-btn
          color="primary"
          label="Сохранить настройки"
          @click="saveSettings"
          class="q-mr-md"
        />
        <q-btn
          color="secondary"
          label="Сбросить к умолчанию"
          @click="resetSettings"
          class="q-mr-md"
        />
        <q-btn
          color="negative"
          label="Очистить кэш"
          @click="clearCache"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

// Состояние
const loading = ref(false)

// Настройки
const settings = reactive({
  // Общие
  language: 'ru',
  timezone: 'Europe/Moscow',
  dateFormat: 'DD.MM.YYYY',
  darkMode: false,
  notifications: true,
  
  // Отображение
  itemsPerPage: 10,
  defaultSort: 'name',
  showFilters: true,
  autoRefresh: false,
  
  // API
  apiUrl: 'http://localhost:8080',
  graphqlEndpoint: '/graphql',
  requestTimeout: 30000,
  enableCaching: true,
  
  // Безопасность
  requireAuth: false,
  sessionTimeout: 30,
  auditLog: true,
  dataEncryption: false
})

// Опции
const sortOptions = [
  { label: 'По названию', value: 'name' },
  { label: 'По дате создания', value: 'createdAt' },
  { label: 'По дате обновления', value: 'updatedAt' },
  { label: 'По типу', value: 'type' }
]

// Методы
const loadSettings = async () => {
  loading.value = true
  try {
    // TODO: Загрузка настроек из localStorage или API
    const savedSettings = localStorage.getItem('vuege-settings')
    if (savedSettings) {
      Object.assign(settings, JSON.parse(savedSettings))
    }
  } catch (error) {
    console.error('Ошибка загрузки настроек:', error)
  } finally {
    loading.value = false
  }
}

const saveSettings = async () => {
  try {
    // TODO: Сохранение настроек
    localStorage.setItem('vuege-settings', JSON.stringify(settings))
    console.log('Настройки сохранены:', settings)
  } catch (error) {
    console.error('Ошибка сохранения настроек:', error)
  }
}

const resetSettings = () => {
  // TODO: Сброс к умолчанию
  console.log('Сброс настроек к умолчанию')
}

const clearCache = () => {
  // TODO: Очистка кэша
  console.log('Очистка кэша')
}

// Инициализация
onMounted(() => {
  loadSettings()
})
</script>
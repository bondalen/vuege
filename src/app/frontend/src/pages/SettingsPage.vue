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
          <q-select
            v-model="settings.language"
            :options="languageOptions"
            label="Язык интерфейса"
            outlined
            dense
            class="q-mb-md"
            @update:model-value="setLocale"
          >
            <template v-slot:append>
              <q-icon name="language" />
            </template>
          </q-select>
          
          <q-select
            v-model="settings.timezone"
            :options="timezoneOptions"
            label="Часовой пояс"
            outlined
            dense
            class="q-mb-md"
          >
            <template v-slot:append>
              <q-icon name="schedule" />
            </template>
          </q-select>
          
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
          
          <q-select
            v-model="settings.darkMode"
            :options="[
              { label: 'Светлая', value: false },
              { label: 'Темная', value: true }
            ]"
            label="Тема"
            outlined
            dense
            class="q-mb-md"
            @update:model-value="setTheme"
          >
            <template v-slot:append>
              <q-icon name="palette" />
            </template>
          </q-select>
          
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

    <!-- Дополнительные настройки -->
    <div class="row q-gutter-lg q-mt-lg">
      <!-- Дополнительные настройки -->
      <q-card class="col-12 col-md-6">
        <q-card-section>
          <div class="text-h6">Дополнительные настройки</div>
        </q-card-section>
        
        <q-card-section>
          <q-toggle
            v-model="settings.debugMode"
            label="Режим отладки"
            color="warning"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.analytics"
            label="Аналитика"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.telemetry"
            label="Телеметрия"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.autoSave"
            label="Автосохранение"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.compactMode"
            label="Компактный режим"
            color="primary"
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="settings.showBreadcrumbs"
            label="Показывать хлебные крошки"
            color="primary"
            class="q-mb-md"
          />
        </q-card-section>
      </q-card>

      <!-- Статистика -->
      <q-card class="col-12 col-md-6">
        <q-card-section>
          <div class="text-h6">Статистика</div>
        </q-card-section>
        
        <q-card-section>
          <div class="row q-gutter-md">
            <div class="col-6">
              <div class="text-caption text-grey-6">Настройки</div>
              <div class="text-h6">{{ settingsStats.totalSettings }}</div>
            </div>
            <div class="col-6">
              <div class="text-caption text-grey-6">Категории</div>
              <div class="text-h6">{{ settingsStats.categories }}</div>
            </div>
            <div class="col-6">
              <div class="text-caption text-grey-6">Размер кэша</div>
              <div class="text-h6">{{ formatFileSize(cacheStats.size) }}</div>
            </div>
            <div class="col-6">
              <div class="text-caption text-grey-6">Элементов в кэше</div>
              <div class="text-h6">{{ cacheStats.totalItems }}</div>
            </div>
          </div>
          
          <q-separator class="q-my-md" />
          
          <div class="text-caption text-grey-6">Текущая тема</div>
          <div class="text-body1">{{ currentTheme }}</div>
          
          <div class="text-caption text-grey-6 q-mt-md">Текущий язык</div>
          <div class="text-body1">{{ currentLanguage }}</div>
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
          :loading="loading"
          :disable="!settingsChanged"
          class="q-mr-md"
        />
        <q-btn
          color="secondary"
          label="Сбросить к умолчанию"
          @click="resetSettings"
          :loading="loading"
          class="q-mr-md"
        />
        <q-btn
          color="negative"
          label="Очистить кэш"
          @click="clearCache"
          :loading="loading"
          class="q-mr-md"
        />
        <q-btn
          color="info"
          label="Экспорт"
          @click="exportSettings"
          class="q-mr-md"
        />
        <q-btn
          color="warning"
          label="Импорт"
          @click="$refs.fileInput.click()"
        />
        <input
          ref="fileInput"
          type="file"
          accept=".json"
          style="display: none"
          @change="importSettings"
        />
      </div>
    </div>
    
    <!-- Индикатор изменений -->
    <div v-if="settingsChanged" class="row q-mt-md">
      <div class="col-12 text-center">
        <q-banner class="bg-warning text-white">
          <template v-slot:avatar>
            <q-icon name="warning" />
          </template>
          Есть несохраненные изменения. Не забудьте сохранить настройки.
        </q-banner>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { 
  useSettingsManager, 
  useNotificationManager, 
  useLoadingManager, 
  useCacheManager,
  useThemeManager,
  useI18nManager,
  formatDate,
  formatYear,
  formatFileSize
} from '@/utils'

// Quasar
const $q = useQuasar()

// Менеджеры
const { 
  addSetting, 
  getValue, 
  setValue, 
  saveSettings: saveSettingsToStorage,
  resetAllSettings,
  getStats: getSettingsStats
} = useSettingsManager()

const { 
  success: showSuccess, 
  error: showError, 
  loading: showLoadingNotification 
} = useNotificationManager()

const { show: showLoading, hide: hideLoading } = useLoadingManager()

const { clearCache: clearAppCache, getStats: getCacheStats } = useCacheManager()

const { setTheme, getCurrentTheme, getAvailableThemes } = useThemeManager()

const { setLocale, getLocale, getAvailableLocales } = useI18nManager()

// Состояние
const loading = ref(false)
const settingsChanged = ref(false)

// Настройки
const settings = reactive({
  // Общие
  language: 'ru',
  timezone: 'Europe/Moscow',
  dateFormat: 'DD.MM.YYYY',
  timeFormat: 'HH:mm',
  darkMode: false,
  notifications: true,
  autoSave: true,
  
  // Отображение
  itemsPerPage: 10,
  defaultSort: 'name',
  showFilters: true,
  autoRefresh: false,
  compactMode: false,
  showBreadcrumbs: true,
  
  // API
  apiUrl: 'http://localhost:8080',
  graphqlEndpoint: '/graphql',
  requestTimeout: 30000,
  enableCaching: true,
  cacheTimeout: 300000,
  retryAttempts: 3,
  
  // Безопасность
  requireAuth: false,
  sessionTimeout: 30,
  auditLog: true,
  dataEncryption: false,
  twoFactorAuth: false,
  
  // Дополнительные
  debugMode: false,
  analytics: true,
  telemetry: false
})

// Опции
const sortOptions = [
  { label: 'По названию', value: 'name' },
  { label: 'По дате создания', value: 'createdAt' },
  { label: 'По дате обновления', value: 'updatedAt' },
  { label: 'По типу', value: 'type' }
]

const languageOptions = [
  { label: 'Русский', value: 'ru' },
  { label: 'English', value: 'en' },
  { label: 'Deutsch', value: 'de' },
  { label: 'Français', value: 'fr' }
]

const timezoneOptions = [
  { label: 'Москва (UTC+3)', value: 'Europe/Moscow' },
  { label: 'Лондон (UTC+0)', value: 'Europe/London' },
  { label: 'Нью-Йорк (UTC-5)', value: 'America/New_York' },
  { label: 'Токио (UTC+9)', value: 'Asia/Tokyo' }
]

// Вычисляемые свойства
const currentTheme = computed(() => getCurrentTheme()?.name || 'light')
const availableThemes = computed(() => getAvailableThemes())
const currentLanguage = computed(() => getLocale())
const availableLanguages = computed(() => getAvailableLocales())

const settingsStats = computed(() => getSettingsStats())
const cacheStats = computed(() => getCacheStats())

// Методы
const loadSettings = async () => {
  loading.value = true
  showLoading({ message: 'Загрузка настроек...' })
  
  try {
    // Загружаем настройки из менеджера
    Object.keys(settings).forEach(key => {
      const value = getValue(key)
      if (value !== null) {
        settings[key] = value
      }
    })
    
    showSuccess('Настройки загружены')
  } catch (error) {
    console.error('Ошибка загрузки настроек:', error)
    showError('Ошибка загрузки настроек')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const saveSettings = async () => {
  loading.value = true
  showLoading({ message: 'Сохранение настроек...' })
  
  try {
    // Сохраняем настройки через менеджер
    Object.entries(settings).forEach(([key, value]) => {
      setValue(key, value)
    })
    
    // Применяем изменения
    await applySettings()
    
    // Сохраняем в хранилище
    saveSettingsToStorage()
    
    settingsChanged.value = false
    showSuccess('Настройки сохранены')
  } catch (error) {
    console.error('Ошибка сохранения настроек:', error)
    showError('Ошибка сохранения настроек')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const applySettings = async () => {
  // Применяем тему
  if (settings.darkMode) {
    setTheme('dark')
  } else {
    setTheme('light')
  }
  
  // Применяем язык
  setLocale(settings.language)
  
  // Применяем другие настройки
  if (settings.notifications) {
    // Включаем уведомления
  } else {
    // Отключаем уведомления
  }
  
  // Применяем настройки кэша
  if (!settings.enableCaching) {
    clearAppCache()
  }
}

const resetSettings = async () => {
  try {
    const confirmed = await $q.dialog({
      title: 'Подтверждение',
      message: 'Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?',
      cancel: true,
      persistent: true
    })
    
    if (confirmed) {
      loading.value = true
      showLoading({ message: 'Сброс настроек...' })
      
      resetAllSettings()
      
      // Перезагружаем настройки
      await loadSettings()
      
      showSuccess('Настройки сброшены к умолчанию')
    }
  } catch (error) {
    console.error('Ошибка сброса настроек:', error)
    showError('Ошибка сброса настроек')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const clearCache = async () => {
  try {
    const confirmed = await $q.dialog({
      title: 'Подтверждение',
      message: 'Вы уверены, что хотите очистить кэш?',
      cancel: true,
      persistent: true
    })
    
    if (confirmed) {
      loading.value = true
      showLoading({ message: 'Очистка кэша...' })
      
      clearAppCache()
      
      showSuccess('Кэш очищен')
    }
  } catch (error) {
    console.error('Ошибка очистки кэша:', error)
    showError('Ошибка очистки кэша')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const exportSettings = () => {
  try {
    const data = JSON.stringify(settings, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'vuege-settings.json'
    link.click()
    URL.revokeObjectURL(url)
    
    showSuccess('Настройки экспортированы')
  } catch (error) {
    console.error('Ошибка экспорта настроек:', error)
    showError('Ошибка экспорта настроек')
  }
}

const importSettings = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  
  try {
    const text = await file.text()
    const importedSettings = JSON.parse(text)
    
    Object.assign(settings, importedSettings)
    settingsChanged.value = true
    
    showSuccess('Настройки импортированы')
  } catch (error) {
    console.error('Ошибка импорта настроек:', error)
    showError('Ошибка импорта настроек')
  }
}

// Отслеживаем изменения настроек
const watchSettings = () => {
  Object.keys(settings).forEach(key => {
    if (settings[key] !== getValue(key)) {
      settingsChanged.value = true
    }
  })
}

// Инициализация
onMounted(() => {
  loadSettings()
  
  // Настраиваем автосохранение
  if (settings.autoSave) {
    setInterval(watchSettings, 5000) // Проверяем каждые 5 секунд
  }
})
</script>
import { createApp } from 'vue'
import { Quasar, Notify, Dialog, Loading } from 'quasar'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './router/routes'
import { createApolloClient } from './utils/apollo'
import { DefaultApolloClient } from '@vue/apollo-composable'

// Импорт утилит и менеджеров
import {
  getGlobalNotificationManager,
  getGlobalLoadingManager,
  getGlobalModalManager,
  getGlobalCacheManager,
  getGlobalEventManager,
  getGlobalI18nManager,
  getGlobalThemeManager,
  getGlobalSettingsManager,
  getGlobalApiClientManager
} from './utils'

// Import Quasar css
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/dist/quasar.css'

// Import app css
import './style.css'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create Apollo client
const apolloClient = createApolloClient()

// Инициализация глобальных менеджеров
const initializeManagers = () => {
  // Инициализируем API клиент
  const apiClientManager = getGlobalApiClientManager()
  
  // Инициализируем кэш
  const cacheManager = getGlobalCacheManager()
  
  // Инициализируем события
  const eventManager = getGlobalEventManager()
  
  // Инициализируем i18n
  const i18nManager = getGlobalI18nManager()
  i18nManager.addMessages('ru', {
    'app.title': 'Vuege',
    'app.description': 'Система управления данными',
    'common.save': 'Сохранить',
    'common.cancel': 'Отмена',
    'common.delete': 'Удалить',
    'common.edit': 'Редактировать',
    'common.create': 'Создать',
    'common.loading': 'Загрузка...',
    'common.error': 'Ошибка',
    'common.success': 'Успешно'
  })
  
  // Инициализируем темы
  const themeManager = getGlobalThemeManager()
  themeManager.addTheme({
    name: 'light',
    label: 'Светлая',
    colors: {
      primary: '#1976D2',
      secondary: '#26A69A',
      accent: '#9C27B0',
      dark: '#1D1D1D',
      darkPage: '#121212',
      positive: '#21BA45',
      negative: '#C10015',
      info: '#31CCEC',
      warning: '#F2C037',
      background: '#ffffff',
      surface: '#f5f5f5',
      text: '#000000',
      textSecondary: '#666666',
      border: '#e0e0e0',
      shadow: 'rgba(0, 0, 0, 0.1)'
    },
    fonts: {
      family: 'Roboto, sans-serif',
      size: {
        xs: '0.75rem',
        sm: '0.875rem',
        md: '1rem',
        lg: '1.125rem',
        xl: '1.25rem',
        h1: '2.5rem',
        h2: '2rem',
        h3: '1.75rem',
        h4: '1.5rem',
        h5: '1.25rem',
        h6: '1rem'
      },
      weight: {
        light: 300,
        normal: 400,
        medium: 500,
        bold: 700
      }
    },
    spacing: {
      xs: '0.25rem',
      sm: '0.5rem',
      md: '1rem',
      lg: '1.5rem',
      xl: '2rem',
      xxl: '3rem'
    },
    borderRadius: {
      sm: '4px',
      md: '8px',
      lg: '12px',
      xl: '16px'
    },
    shadows: {
      sm: '0 1px 3px rgba(0,0,0,0.12)',
      md: '0 4px 6px rgba(0,0,0,0.1)',
      lg: '0 10px 15px rgba(0,0,0,0.1)',
      xl: '0 20px 25px rgba(0,0,0,0.1)'
    },
    breakpoints: {
      xs: 0,
      sm: 600,
      md: 1024,
      lg: 1440,
      xl: 1920
    }
  })
  
  // Инициализируем настройки
  const settingsManager = getGlobalSettingsManager()
  settingsManager.addSetting({
    key: 'language',
    value: 'ru',
    type: 'string',
    label: 'Язык интерфейса',
    category: 'general',
    defaultValue: 'ru'
  })
  
  settingsManager.addSetting({
    key: 'theme',
    value: 'light',
    type: 'string',
    label: 'Тема',
    category: 'display',
    defaultValue: 'light'
  })
  
  settingsManager.addSetting({
    key: 'notifications',
    value: true,
    type: 'boolean',
    label: 'Уведомления',
    category: 'general',
    defaultValue: true
  })
  
  return {
    apiClientManager,
    cacheManager,
    eventManager,
    i18nManager,
    themeManager,
    settingsManager
  }
}

// Create app
const app = createApp({
  name: 'VuegeApp'
})

// Use plugins
app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Loading
  },
  config: {
    brand: {
      primary: '#1976D2',
      secondary: '#26A69A',
      accent: '#9C27B0',
      dark: '#1D1D1D',
      darkPage: '#121212',
      positive: '#21BA45',
      negative: '#C10015',
      info: '#31CCEC',
      warning: '#F2C037'
    }
  }
})

// Инициализируем менеджеры после создания приложения
const managers = initializeManagers()

// Инициализируем менеджеры, которые требуют Quasar
const initializeQuasarManagers = () => {
  // Инициализируем уведомления
  const notificationManager = getGlobalNotificationManager()
  notificationManager.init(app.config.globalProperties.$q)
  
  // Инициализируем загрузку
  const loadingManager = getGlobalLoadingManager()
  loadingManager.init(app.config.globalProperties.$q)
  
  // Инициализируем модальные окна
  const modalManager = getGlobalModalManager()
  modalManager.init(app.config.globalProperties.$q)
}

// Вызываем инициализацию после монтирования
app.config.globalProperties.$managers = managers

// Use router
app.use(router)

// Provide Apollo client
app.provide(DefaultApolloClient, apolloClient)

// Инициализируем Quasar менеджеры
initializeQuasarManagers()

// Глобальные обработчики ошибок
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error)
  const notificationManager = getGlobalNotificationManager()
  notificationManager.error('Произошла ошибка в приложении')
})

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason)
  const notificationManager = getGlobalNotificationManager()
  notificationManager.error('Необработанная ошибка промиса')
})

// Mount app
app.mount('#app')
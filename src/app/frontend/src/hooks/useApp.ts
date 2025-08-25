import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import {
  useNotificationManager,
  useLoadingManager,
  useModalManager,
  useCacheManager,
  useEventManager,
  useI18nManager,
  useThemeManager,
  useSettingsManager,
  useApiClient,
  useTableManager,
  useFormManager
} from '@/utils'
import { APP_NAME, APP_VERSION, DEFAULT_LANGUAGE, DEFAULT_THEME } from '@/constants'

/**
 * Основной хук приложения, предоставляющий доступ ко всем менеджерам
 */
export function useApp() {
  const $q = useQuasar()
  const router = useRouter()

  // Состояние приложения
  const isInitialized = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const currentRoute = ref(router.currentRoute.value)

  // Менеджеры
  const notificationManager = useNotificationManager()
  const loadingManager = useLoadingManager()
  const modalManager = useModalManager()
  const cacheManager = useCacheManager()
  const eventManager = useEventManager()
  const i18nManager = useI18nManager()
  const themeManager = useThemeManager()
  const settingsManager = useSettingsManager()
  const apiClient = useApiClient()

  // Вычисляемые свойства
  const appInfo = computed(() => ({
    name: APP_NAME,
    version: APP_VERSION,
    language: i18nManager.currentLanguage,
    theme: themeManager.currentTheme,
    isDark: themeManager.isDark,
    isMobile: $q.platform.is.mobile,
    isDesktop: $q.platform.is.desktop,
    isOnline: navigator.onLine
  }))

  const userPreferences = computed(() => ({
    language: settingsManager.getSetting('language') || DEFAULT_LANGUAGE,
    theme: settingsManager.getSetting('theme') || DEFAULT_THEME,
    notifications: settingsManager.getSetting('notifications') || true,
    autoSave: settingsManager.getSetting('autoSave') || false,
    compactMode: settingsManager.getSetting('compactMode') || false
  }))

  // Методы инициализации
  const initializeApp = async () => {
    if (isInitialized.value) return

    isLoading.value = true
    error.value = null

    try {
      // Инициализируем менеджеры
      await Promise.all([
        initializeSettings(),
        initializeTheme(),
        initializeLanguage(),
        initializeCache(),
        initializeEventListeners()
      ])

      isInitialized.value = true
      notificationManager.success('Приложение инициализировано')
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка инициализации приложения'
      notificationManager.error(error.value)
    } finally {
      isLoading.value = false
    }
  }

  const initializeSettings = async () => {
    // Загружаем настройки из localStorage
    const savedSettings = settingsManager.loadSettings()
    
    // Применяем настройки по умолчанию
    if (!savedSettings.language) {
      settingsManager.setSetting('language', DEFAULT_LANGUAGE)
    }
    if (!savedSettings.theme) {
      settingsManager.setSetting('theme', DEFAULT_THEME)
    }
  }

  const initializeTheme = () => {
    const theme = settingsManager.getSetting('theme') || DEFAULT_THEME
    themeManager.setTheme(theme)
  }

  const initializeLanguage = () => {
    const language = settingsManager.getSetting('language') || DEFAULT_LANGUAGE
    i18nManager.setLanguage(language)
  }

  const initializeCache = () => {
    cacheManager.initialize()
  }

  const initializeEventListeners = () => {
    // Слушаем изменения сети
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    // Слушаем изменения размера окна
    window.addEventListener('resize', handleResize)

    // Слушаем изменения видимости страницы
    document.addEventListener('visibilitychange', handleVisibilityChange)

    // Слушаем ошибки
    window.addEventListener('error', handleGlobalError)
    window.addEventListener('unhandledrejection', handleUnhandledRejection)
  }

  // Обработчики событий
  const handleOnline = () => {
    notificationManager.info('Соединение восстановлено')
    eventManager.emit('app:online')
  }

  const handleOffline = () => {
    notificationManager.warning('Соединение потеряно')
    eventManager.emit('app:offline')
  }

  const handleResize = () => {
    eventManager.emit('app:resize', {
      width: window.innerWidth,
      height: window.innerHeight
    })
  }

  const handleVisibilityChange = () => {
    const isVisible = !document.hidden
    eventManager.emit('app:visibility', { isVisible })
  }

  const handleGlobalError = (event: ErrorEvent) => {
    console.error('Global error:', event.error)
    notificationManager.error('Произошла ошибка в приложении')
    eventManager.emit('app:error', event.error)
  }

  const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
    console.error('Unhandled promise rejection:', event.reason)
    notificationManager.error('Необработанная ошибка промиса')
    eventManager.emit('app:unhandledRejection', event.reason)
  }

  // Методы управления приложением
  const showLoading = (message?: string) => {
    loadingManager.show({ message })
  }

  const hideLoading = () => {
    loadingManager.hide()
  }

  const showNotification = (type: 'success' | 'error' | 'warning' | 'info', message: string) => {
    notificationManager[type](message)
  }

  const showModal = (config: any) => {
    return modalManager.show(config)
  }

  const showConfirm = (config: any) => {
    return modalManager.confirm(config)
  }

  const navigateTo = (route: string) => {
    router.push(route)
  }

  const goBack = () => {
    router.back()
  }

  const refreshPage = () => {
    window.location.reload()
  }

  const clearCache = () => {
    cacheManager.clear()
    notificationManager.success('Кэш очищен')
  }

  const exportSettings = () => {
    const settings = settingsManager.exportSettings()
    const blob = new Blob([JSON.stringify(settings, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'vuege-settings.json'
    link.click()
    URL.revokeObjectURL(url)
  }

  const importSettings = async (file: File) => {
    try {
      const text = await file.text()
      const settings = JSON.parse(text)
      settingsManager.importSettings(settings)
      notificationManager.success('Настройки импортированы')
    } catch (error) {
      notificationManager.error('Ошибка импорта настроек')
    }
  }

  const resetSettings = () => {
    settingsManager.resetSettings()
    notificationManager.success('Настройки сброшены')
  }

  const toggleTheme = () => {
    const newTheme = themeManager.currentTheme === 'light' ? 'dark' : 'light'
    themeManager.setTheme(newTheme)
    settingsManager.setSetting('theme', newTheme)
  }

  const changeLanguage = (language: string) => {
    i18nManager.setLanguage(language)
    settingsManager.setSetting('language', language)
  }

  // Методы для работы с данными
  const fetchData = async (query: string, variables?: any) => {
    try {
      showLoading('Загрузка данных...')
      const result = await apiClient.query(query, variables)
      return result
    } catch (error) {
      notificationManager.error('Ошибка загрузки данных')
      throw error
    } finally {
      hideLoading()
    }
  }

  const mutateData = async (mutation: string, variables?: any) => {
    try {
      showLoading('Сохранение данных...')
      const result = await apiClient.mutate(mutation, variables)
      notificationManager.success('Данные сохранены')
      return result
    } catch (error) {
      notificationManager.error('Ошибка сохранения данных')
      throw error
    } finally {
      hideLoading()
    }
  }

  // Методы для работы с таблицами
  const createTableManager = (data: any[], columns: any[], rowKey = 'id') => {
    return useTableManager(data, columns, rowKey)
  }

  // Методы для работы с формами
  const createFormManager = (initialValues: any, validationRules?: any) => {
    return useFormManager(initialValues, validationRules)
  }

  // Очистка при размонтировании
  const cleanup = () => {
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
    window.removeEventListener('resize', handleResize)
    document.removeEventListener('visibilitychange', handleVisibilityChange)
    window.removeEventListener('error', handleGlobalError)
    window.removeEventListener('unhandledrejection', handleUnhandledRejection)
  }

  // Инициализация при монтировании
  onMounted(() => {
    initializeApp()
  })

  // Очистка при размонтировании
  onUnmounted(() => {
    cleanup()
  })

  return {
    // Состояние
    isInitialized: readonly(isInitialized),
    isLoading: readonly(isLoading),
    error: readonly(error),
    currentRoute: readonly(currentRoute),

    // Менеджеры
    notificationManager,
    loadingManager,
    modalManager,
    cacheManager,
    eventManager,
    i18nManager,
    themeManager,
    settingsManager,
    apiClient,

    // Вычисляемые свойства
    appInfo,
    userPreferences,

    // Методы
    initializeApp,
    showLoading,
    hideLoading,
    showNotification,
    showModal,
    showConfirm,
    navigateTo,
    goBack,
    refreshPage,
    clearCache,
    exportSettings,
    importSettings,
    resetSettings,
    toggleTheme,
    changeLanguage,
    fetchData,
    mutateData,
    createTableManager,
    createFormManager
  }
}
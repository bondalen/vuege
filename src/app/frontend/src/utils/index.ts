// Индексный файл для экспорта всех утилит

// Основные утилиты
export * from './formatters'
export * from './validators'
export * from './storage'
export * from './errors'
export * from './api'
export * from './dates'
export * from './helpers'
export * from './colors'
export * from './files'
export * from './browser'
export * from './network'
export * from './crypto'
export * from './validation'
export * from './forms'
export * from './notifications'
export * from './dialogs'
export * from './loading'
export * from './cache'
export * from './events'
export * from './i18n'
export * from './themes'
export * from './settings'

// Специализированные утилиты
export * from './router'
export * from './state'
export * from './api-client'
export * from './components'
export * from './tables'
export * from './modals'

// Константы
export * from '../constants'

// Типы
export * from '../types/graphql'
export * from '../types/inputs'

// GraphQL
export * from '../graphql/queries'
export * from '../graphql/mutations'

// Apollo Client
export * from '../utils/apollo'

// Создаем удобные алиасы для часто используемых утилит
export { formatters as fmt } from './formatters'
export { validators as val } from './validators'
export { storage as store } from './storage'
export { errors as err } from './errors'
export { api } from './api'
export { dates } from './dates'
export { helpers as help } from './helpers'
export { colors as col } from './colors'
export { files } from './files'
export { browser as brw } from './browser'
export { network as net } from './network'
export { crypto } from './crypto'
export { validation as valid } from './validation'
export { forms } from './forms'
export { notifications as notif } from './notifications'
export { dialogs } from './dialogs'
export { loading } from './loading'
export { cache } from './cache'
export { events } from './events'
export { i18nManager as i18n } from './i18n'
export { themeManager as theme } from './themes'
export { settingsManager as settings } from './settings'
export { router } from './router'
export { state } from './state'
export { apiClient } from './api-client'
export { componentManager as components } from './components'
export { useTableManager as tables } from './tables'
export { modalManager as modals } from './modals'

// Экспортируем все хуки
export {
  useFormatters,
  useValidators,
  useStorage,
  useErrors,
  useApi,
  useDates,
  useHelpers,
  useColors,
  useFiles,
  useBrowser,
  useNetwork,
  useCrypto,
  useValidation,
  useForms,
  useNotifications,
  useDialogs,
  useLoading,
  useCache,
  useEvents,
  useI18nManager,
  useThemeManager,
  useSettingsManager,
  useRouterUtils,
  useAppState,
  useApiClient,
  useComponentManager,
  useTableManager,
  useModalManager
} from './index-hooks'

// Экспортируем все менеджеры
export {
  i18nManager,
  themeManager,
  settingsManager,
  modalManager,
  componentManager
} from './index-managers'

// Экспортируем функции форматирования
export { formatDate, formatYear, formatCoordinates, formatFullName, formatNameWithType, formatFileSize, formatPhoneNumber, formatInn, formatOgrn } from './formatters'
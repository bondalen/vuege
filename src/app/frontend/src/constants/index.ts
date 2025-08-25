// Константы приложения Vuege

export const APP_NAME = 'Vuege'
export const APP_VERSION = '0.1.0'
export const APP_DESCRIPTION = 'Система учета организационных единиц с исторической перспективой'

// API константы
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080'
export const GRAPHQL_ENDPOINT = '/graphql'

// Пагинация
export const DEFAULT_PAGE_SIZE = 10
export const MAX_PAGE_SIZE = 100

// Локальное хранилище
export const STORAGE_KEYS = {
  SETTINGS: 'vuege-settings',
  AUTH_TOKEN: 'vuege-auth-token',
  USER_PREFERENCES: 'vuege-user-preferences',
  THEME: 'vuege-theme',
  LANGUAGE: 'vuege-language',
  CACHE: 'vuege-cache',
  LOCALE: 'vuege-locale'
} as const

// Сессии
export const SESSION_KEYS = {
  CURRENT_USER: 'vuege-current-user',
  TEMP_DATA: 'vuege-temp-data',
  FORM_DATA: 'vuege-form-data'
} as const

// Кэш
export const CACHE_CONFIG = {
  DEFAULT_TTL: 5 * 60 * 1000, // 5 минут
  MAX_SIZE: 1000,
  CLEANUP_INTERVAL: 60 * 1000 // 1 минута
} as const

// Уведомления
export const NOTIFICATION_CONFIG = {
  DEFAULT_TIMEOUT: 5000,
  MAX_NOTIFICATIONS: 5,
  POSITIONS: ['top', 'bottom', 'left', 'right', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
} as const

// Валидация
export const VALIDATION_RULES = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  URL: /^https?:\/\/.+/,
  PHONE: /^\+?[\d\s\-\(\)]+$/,
  PASSWORD_MIN_LENGTH: 8,
  USERNAME_MIN_LENGTH: 3,
  USERNAME_MAX_LENGTH: 50
} as const

// Файлы
export const FILE_CONFIG = {
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/csv', 'application/json'],
  ALLOWED_EXTENSIONS: ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.csv', '.json']
} as const

// Безопасность
export const SECURITY_CONFIG = {
  SESSION_TIMEOUT: 30 * 60 * 1000, // 30 минут
  PASSWORD_EXPIRY_DAYS: 90,
  MAX_LOGIN_ATTEMPTS: 5,
  LOCKOUT_DURATION: 15 * 60 * 1000 // 15 минут
} as const

// Аналитика
export const ANALYTICS_CONFIG = {
  ENABLED: import.meta.env.PROD,
  TRACKING_ID: import.meta.env.VITE_GA_TRACKING_ID,
  EVENTS: {
    PAGE_VIEW: 'page_view',
    BUTTON_CLICK: 'button_click',
    FORM_SUBMIT: 'form_submit',
    FILE_DOWNLOAD: 'file_download',
    SEARCH: 'search',
    REPORT_GENERATE: 'report_generate',
    DATA_EXPORT: 'data_export',
    DATA_IMPORT: 'data_import'
  }
} as const

// Типы организаций
export const ORGANIZATION_TYPES = {
  GOVERNMENT: 'GOVERNMENT',
  COMMERCIAL: 'COMMERCIAL',
  NON_PROFIT: 'NON_PROFIT',
  EDUCATIONAL: 'EDUCATIONAL',
  MILITARY: 'MILITARY',
  RELIGIOUS: 'RELIGIOUS',
  OTHER: 'OTHER'
} as const

// Типы государств
export const STATE_TYPES = {
  EMPIRE: 'EMPIRE',
  KINGDOM: 'KINGDOM',
  REPUBLIC: 'REPUBLIC',
  FEDERATION: 'FEDERATION',
  CONFEDERATION: 'CONFEDERATION',
  OTHER: 'OTHER'
} as const

// Типы мест
export const LOCATION_TYPES = {
  COUNTRY: 'COUNTRY',
  REGION: 'REGION',
  CITY: 'CITY',
  DISTRICT: 'DISTRICT',
  ADDRESS: 'ADDRESS',
  COORDINATES: 'COORDINATES'
} as const

// Цвета для разных типов
export const TYPE_COLORS = {
  [ORGANIZATION_TYPES.GOVERNMENT]: 'primary',
  [ORGANIZATION_TYPES.COMMERCIAL]: 'secondary',
  [ORGANIZATION_TYPES.NON_PROFIT]: 'accent',
  [ORGANIZATION_TYPES.EDUCATIONAL]: 'info',
  [ORGANIZATION_TYPES.MILITARY]: 'warning',
  [ORGANIZATION_TYPES.RELIGIOUS]: 'purple',
  [ORGANIZATION_TYPES.OTHER]: 'grey',
  
  [STATE_TYPES.EMPIRE]: 'deep-purple',
  [STATE_TYPES.KINGDOM]: 'amber',
  [STATE_TYPES.REPUBLIC]: 'blue',
  [STATE_TYPES.FEDERATION]: 'green',
  [STATE_TYPES.CONFEDERATION]: 'orange',
  [STATE_TYPES.OTHER]: 'grey',
  
  [LOCATION_TYPES.COUNTRY]: 'deep-orange',
  [LOCATION_TYPES.REGION]: 'light-blue',
  [LOCATION_TYPES.CITY]: 'teal',
  [LOCATION_TYPES.DISTRICT]: 'lime',
  [LOCATION_TYPES.ADDRESS]: 'brown',
  [LOCATION_TYPES.COORDINATES]: 'grey'
} as const

// Иконки для разных типов
export const TYPE_ICONS = {
  [ORGANIZATION_TYPES.GOVERNMENT]: 'account_balance',
  [ORGANIZATION_TYPES.COMMERCIAL]: 'business',
  [ORGANIZATION_TYPES.NON_PROFIT]: 'volunteer_activism',
  [ORGANIZATION_TYPES.EDUCATIONAL]: 'school',
  [ORGANIZATION_TYPES.MILITARY]: 'security',
  [ORGANIZATION_TYPES.RELIGIOUS]: 'church',
  [ORGANIZATION_TYPES.OTHER]: 'business_center',
  
  [STATE_TYPES.EMPIRE]: 'crown',
  [STATE_TYPES.KINGDOM]: 'castle',
  [STATE_TYPES.REPUBLIC]: 'flag',
  [STATE_TYPES.FEDERATION]: 'public',
  [STATE_TYPES.CONFEDERATION]: 'hub',
  [STATE_TYPES.OTHER]: 'public',
  
  [LOCATION_TYPES.COUNTRY]: 'public',
  [LOCATION_TYPES.REGION]: 'terrain',
  [LOCATION_TYPES.CITY]: 'location_city',
  [LOCATION_TYPES.DISTRICT]: 'map',
  [LOCATION_TYPES.ADDRESS]: 'place',
  [LOCATION_TYPES.COORDINATES]: 'gps_fixed'
} as const

// Форматы дат
export const DATE_FORMATS = {
  DISPLAY: 'DD.MM.YYYY',
  API: 'YYYY-MM-DD',
  DATETIME: 'DD.MM.YYYY HH:mm',
  TIME: 'HH:mm'
} as const

// Сообщения об ошибках
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Ошибка сети. Проверьте подключение к интернету.',
  UNAUTHORIZED: 'Необходима авторизация.',
  FORBIDDEN: 'Доступ запрещен.',
  NOT_FOUND: 'Ресурс не найден.',
  VALIDATION_ERROR: 'Ошибка валидации данных.',
  SERVER_ERROR: 'Ошибка сервера. Попробуйте позже.',
  UNKNOWN_ERROR: 'Неизвестная ошибка.'
} as const

// Сообщения об успехе
export const SUCCESS_MESSAGES = {
  CREATED: 'Запись успешно создана.',
  UPDATED: 'Запись успешно обновлена.',
  DELETED: 'Запись успешно удалена.',
  SAVED: 'Данные успешно сохранены.',
  EXPORTED: 'Данные успешно экспортированы.',
  CACHE_CLEARED: 'Кэш успешно очищен.',
  SETTINGS_SAVED: 'Настройки успешно сохранены.',
  THEME_CHANGED: 'Тема успешно изменена.',
  LANGUAGE_CHANGED: 'Язык успешно изменен.',
  REPORT_GENERATED: 'Отчет успешно сгенерирован.'
} as const

// Предупреждения
export const WARNING_MESSAGES = {
  UNSAVED_CHANGES: 'У вас есть несохраненные изменения.',
  DELETE_CONFIRMATION: 'Вы уверены, что хотите удалить этот элемент?',
  LEAVE_PAGE: 'Вы уверены, что хотите покинуть страницу?',
  LARGE_FILE: 'Файл имеет большой размер. Загрузка может занять время.',
  CACHE_EXPIRED: 'Кэш устарел. Данные будут обновлены.',
  SESSION_EXPIRING: 'Сессия скоро истечет. Сохраните работу.',
  DATA_LOSS: 'Несохраненные данные будут потеряны.',
  SLOW_CONNECTION: 'Медленное соединение. Операция может занять время.'
} as const

// Информационные сообщения
export const INFO_MESSAGES = {
  LOADING: 'Загрузка данных...',
  PROCESSING: 'Обработка данных...',
  SAVING: 'Сохранение данных...',
  UPLOADING: 'Загрузка файла...',
  DOWNLOADING: 'Скачивание файла...',
  EXPORTING: 'Экспорт данных...',
  IMPORTING: 'Импорт данных...',
  CACHING: 'Кэширование данных...',
  GENERATING_REPORT: 'Генерация отчета...',
  VALIDATING: 'Валидация данных...',
  SYNCHRONIZING: 'Синхронизация данных...',
  BACKING_UP: 'Создание резервной копии...',
  RESTORING: 'Восстановление данных...'
} as const

// Статусы
export const STATUS_TYPES = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  PROCESSING: 'processing',
  CANCELLED: 'cancelled',
  EXPIRED: 'expired'
} as const

// Форматы отчетов
export const REPORT_FORMATS = {
  PDF: 'pdf',
  EXCEL: 'excel',
  JSON: 'json',
  CSV: 'csv',
  XML: 'xml'
} as const

// Размеры файлов
export const FILE_SIZES = {
  BYTE: 1,
  KB: 1024,
  MB: 1024 * 1024,
  GB: 1024 * 1024 * 1024,
  TB: 1024 * 1024 * 1024 * 1024
} as const

// Цвета
export const COLORS = {
  PRIMARY: '#1976D2',
  SECONDARY: '#26A69A',
  ACCENT: '#9C27B0',
  POSITIVE: '#21BA45',
  NEGATIVE: '#C10015',
  WARNING: '#F2C037',
  INFO: '#31CCEC',
  DARK: '#1D1D1D',
  LIGHT: '#FFFFFF',
  GREY: '#9E9E9E'
} as const

// Анимации
export const ANIMATIONS = {
  DURATION: {
    FAST: 150,
    NORMAL: 300,
    SLOW: 500
  },
  EASING: {
    EASE_IN: 'ease-in',
    EASE_OUT: 'ease-out',
    EASE_IN_OUT: 'ease-in-out',
    LINEAR: 'linear'
  }
} as const

// Размеры экранов
export const BREAKPOINTS = {
  XS: 0,
  SM: 600,
  MD: 1024,
  LG: 1440,
  XL: 1920
} as const

// Z-индексы
export const Z_INDEX = {
  DROPDOWN: 1000,
  STICKY: 1020,
  FIXED: 1030,
  MODAL_BACKDROP: 1040,
  MODAL: 1050,
  POPOVER: 1060,
  TOOLTIP: 1070,
  TOAST: 1080
} as const
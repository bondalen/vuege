// Основные типы приложения

// Экспорт всех типов
export * from './graphql'
export * from './inputs'

// Глобальные типы
export interface AppConfig {
  name: string
  version: string
  description: string
  author: string
  apiUrl: string
  graphqlEndpoint: string
  defaultLanguage: string
  defaultTheme: string
  features: {
    auth: boolean
    notifications: boolean
    analytics: boolean
    caching: boolean
  }
}

export interface User {
  id: string
  username: string
  email: string
  firstName?: string
  lastName?: string
  avatar?: string
  roles: string[]
  permissions: string[]
  preferences: Record<string, any>
  lastLogin?: Date
  createdAt: Date
  updatedAt: Date
}

export interface ApiResponse<T = any> {
  data: T
  success: boolean
  message?: string
  errors?: string[]
  meta?: {
    total?: number
    page?: number
    pageSize?: number
    totalPages?: number
  }
}

export interface PaginationParams {
  page: number
  pageSize: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface FilterParams {
  [key: string]: any
}

export interface SearchParams {
  query: string
  fields?: string[]
  filters?: FilterParams
}

export interface ExportParams {
  format: 'pdf' | 'excel' | 'json' | 'csv' | 'xml'
  filters?: FilterParams
  columns?: string[]
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface ImportParams {
  file: File
  format: 'json' | 'csv' | 'excel'
  options?: {
    skipHeader?: boolean
    delimiter?: string
    encoding?: string
  }
}

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: Date
  read: boolean
  actions?: Array<{
    label: string
    action: string
    data?: any
  }>
}

export interface AuditLog {
  id: string
  userId: string
  action: string
  resource: string
  resourceId: string
  details: Record<string, any>
  ipAddress: string
  userAgent: string
  timestamp: Date
}

export interface SystemStats {
  users: {
    total: number
    active: number
    inactive: number
  }
  organizations: {
    total: number
    active: number
    dissolved: number
  }
  states: {
    total: number
    active: number
    historical: number
  }
  people: {
    total: number
    active: number
    deceased: number
  }
  locations: {
    total: number
    cities: number
    countries: number
  }
  storage: {
    used: number
    total: number
    percentage: number
  }
  performance: {
    avgResponseTime: number
    requestsPerMinute: number
    errorRate: number
  }
}

export interface Theme {
  name: string
  label: string
  colors: {
    primary: string
    secondary: string
    accent: string
    dark: string
    darkPage: string
    positive: string
    negative: string
    info: string
    warning: string
    background: string
    surface: string
    text: string
    textSecondary: string
    border: string
    shadow: string
  }
  fonts: {
    family: string
    size: Record<string, string>
    weight: Record<string, number>
  }
  spacing: Record<string, string>
  borderRadius: Record<string, string>
  shadows: Record<string, string>
  breakpoints: Record<string, number>
}

export interface Language {
  code: string
  name: string
  nativeName: string
  flag?: string
  rtl: boolean
}

export interface Settings {
  general: {
    language: string
    timezone: string
    dateFormat: string
    timeFormat: string
    notifications: boolean
    autoSave: boolean
  }
  display: {
    theme: string
    compactMode: boolean
    showBreadcrumbs: boolean
    itemsPerPage: number
    defaultSort: string
    showFilters: boolean
    autoRefresh: boolean
  }
  api: {
    baseUrl: string
    graphqlEndpoint: string
    timeout: number
    retryAttempts: number
    enableCaching: boolean
    cacheTimeout: number
  }
  security: {
    requireAuth: boolean
    sessionTimeout: number
    auditLog: boolean
    dataEncryption: boolean
    twoFactorAuth: boolean
  }
  advanced: {
    debugMode: boolean
    analytics: boolean
    telemetry: boolean
    experimentalFeatures: boolean
  }
}

// Утилитарные типы
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

export type Required<T, K extends keyof T> = T & Required<Pick<T, K>>

export type Nullable<T> = T | null

export type Undefinable<T> = T | undefined

export type AsyncReturnType<T extends (...args: any) => Promise<any>> = 
  T extends (...args: any) => Promise<infer R> ? R : any

export type ComponentProps<T> = T extends React.ComponentType<infer P> ? P : never

export type EventHandler<T = Event> = (event: T) => void

export type Callback<T = any> = (data: T) => void

export type Predicate<T = any> = (item: T) => boolean

export type Comparator<T = any> = (a: T, b: T) => number

export type Mapper<T = any, R = any> = (item: T) => R

export type Reducer<T = any, R = any> = (acc: R, item: T) => R

// Типы для форм
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'checkbox' | 'radio' | 'date' | 'file' | 'custom'
  value?: any
  required?: boolean
  validation?: ValidationRule[]
  options?: Array<{ label: string; value: any; disabled?: boolean }>
  placeholder?: string
  help?: string
  disabled?: boolean
  readonly?: boolean
  hidden?: boolean
  dependencies?: string[]
  customComponent?: any
  customProps?: Record<string, any>
}

export interface ValidationRule {
  type: 'required' | 'min' | 'max' | 'minLength' | 'maxLength' | 'pattern' | 'email' | 'url' | 'custom'
  message: string
  value?: any
  validator?: (value: any) => boolean | string
}

export interface FormState {
  values: Record<string, any>
  errors: Record<string, string>
  touched: Record<string, boolean>
  dirty: Record<string, boolean>
  loading: boolean
  submitted: boolean
  valid: boolean
}

// Типы для таблиц
export interface TableColumn {
  name: string
  label: string
  field: string
  sortable?: boolean
  filterable?: boolean
  align?: 'left' | 'center' | 'right'
  format?: (value: any) => string
  render?: (value: any, row: any) => any
  style?: Record<string, any>
  classes?: string
  width?: string | number
  minWidth?: number
  maxWidth?: number
  fixed?: 'left' | 'right'
  resizable?: boolean
  hidden?: boolean
}

export interface TableState {
  data: any[]
  columns: TableColumn[]
  sort: { key: string; direction: 'asc' | 'desc' } | null
  filters: Record<string, any>
  pagination: {
    page: number
    pageSize: number
    total: number
  }
  selection: {
    selectedKeys: Set<string | number>
    selectAll: boolean
    indeterminate: boolean
  }
  loading: boolean
  error: any
  search: string
  expandedRows: Set<string | number>
}

// Типы для модальных окон
export interface ModalConfig {
  title?: string
  subtitle?: string
  persistent?: boolean
  maximized?: boolean
  fullHeight?: boolean
  fullWidth?: boolean
  position?: string
  transitionShow?: string
  transitionHide?: string
  showClose?: boolean
  showCancel?: boolean
  showConfirm?: boolean
  cancelLabel?: string
  confirmLabel?: string
  cancelColor?: string
  confirmColor?: string
  cancelIcon?: string
  confirmIcon?: string
  loading?: boolean
  size?: string
  cardStyle?: Record<string, any>
  cardClass?: string
}

// Типы для уведомлений
export interface NotificationConfig {
  message: string
  caption?: string
  icon?: string
  color?: string
  textColor?: string
  bgColor?: string
  position?: string
  timeout?: number
  multiLine?: boolean
  html?: boolean
  actions?: NotificationAction[]
  progress?: boolean
  spinner?: boolean
  spinnerColor?: string
  spinnerSize?: string
  classes?: string
  style?: string
  attrs?: Record<string, any>
  onDismiss?: () => void
  onAction?: (action: NotificationAction) => void
  onTimeout?: () => void
  onShow?: () => void
  onHide?: () => void
}

export interface NotificationAction {
  label: string
  color?: string
  textColor?: string
  icon?: string
  flat?: boolean
  outline?: boolean
  round?: boolean
  size?: string
  dense?: boolean
  noCaps?: boolean
  noWrap?: boolean
  align?: string
  stretch?: boolean
  loading?: boolean
  disable?: boolean
  tabindex?: number
  type?: string
  href?: string
  target?: string
  rel?: string
  download?: boolean
  onClick?: () => void
}

// Типы для кэша
export interface CacheItem<T = any> {
  value: T
  timestamp: number
  ttl: number
  accessCount: number
  lastAccess: number
}

export interface CacheConfig {
  maxSize: number
  defaultTtl: number
  cleanupInterval: number
  enableStats: boolean
}

// Типы для событий
export interface EventHandler {
  id: string
  handler: Function
  once: boolean
  priority: number
}

export interface EventConfig {
  priority?: number
  once?: boolean
  async?: boolean
  timeout?: number
}

// Типы для i18n
export interface Translation {
  [key: string]: string | Translation
}

export interface I18nConfig {
  locale: string
  fallbackLocale: string
  messages: Record<string, Translation>
  dateTimeFormats?: Record<string, any>
  numberFormats?: Record<string, any>
  pluralizationRules?: Record<string, Function>
}

// Типы для настроек
export interface Setting<T = any> {
  key: string
  value: T
  type: 'string' | 'number' | 'boolean' | 'object' | 'array'
  label: string
  description?: string
  category: string
  required?: boolean
  readonly?: boolean
  hidden?: boolean
  validation?: (value: T) => boolean | string
  options?: Array<{ value: T; label: string }>
  min?: number
  max?: number
  step?: number
  placeholder?: string
  defaultValue: T
}

export interface SettingsConfig {
  storageKey: string
  autoSave: boolean
  validateOnChange: boolean
  categories: string[]
}
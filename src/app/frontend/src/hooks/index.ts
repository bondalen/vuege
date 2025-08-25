// Экспорт всех хуков

export { useApp } from './useApp'

// Типы для хуков
export interface AppState {
  isInitialized: boolean
  isLoading: boolean
  error: string | null
  currentRoute: any
}

export interface AppInfo {
  name: string
  version: string
  language: string
  theme: string
  isDark: boolean
  isMobile: boolean
  isDesktop: boolean
  isOnline: boolean
}

export interface UserPreferences {
  language: string
  theme: string
  notifications: boolean
  autoSave: boolean
  compactMode: boolean
}

export interface AppMethods {
  initializeApp: () => Promise<void>
  showLoading: (message?: string) => void
  hideLoading: () => void
  showNotification: (type: 'success' | 'error' | 'warning' | 'info', message: string) => void
  showModal: (config: any) => Promise<any>
  showConfirm: (config: any) => Promise<boolean>
  navigateTo: (route: string) => void
  goBack: () => void
  refreshPage: () => void
  clearCache: () => void
  exportSettings: () => void
  importSettings: (file: File) => Promise<void>
  resetSettings: () => void
  toggleTheme: () => void
  changeLanguage: (language: string) => void
  fetchData: (query: string, variables?: any) => Promise<any>
  mutateData: (mutation: string, variables?: any) => Promise<any>
  createTableManager: (data: any[], columns: any[], rowKey?: string) => any
  createFormManager: (initialValues: any, validationRules?: any) => any
}
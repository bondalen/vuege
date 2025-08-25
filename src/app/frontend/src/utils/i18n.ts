// Утилиты для работы с интернационализацией

/**
 * Интерфейс для перевода
 */
export interface Translation {
  [key: string]: string | Translation
}

/**
 * Интерфейс для конфигурации i18n
 */
export interface I18nConfig {
  locale: string
  fallbackLocale: string
  messages: Record<string, Translation>
  dateTimeFormats?: Record<string, any>
  numberFormats?: Record<string, any>
  pluralizationRules?: Record<string, Function>
}

/**
 * Класс для управления интернационализацией
 */
export class I18nManager {
  private config: I18nConfig
  private currentLocale: string
  private fallbackLocale: string
  private messages: Record<string, Translation>
  private dateTimeFormats: Record<string, any>
  private numberFormats: Record<string, any>
  private pluralizationRules: Record<string, Function>

  constructor(config?: Partial<I18nConfig>) {
    this.config = {
      locale: 'ru',
      fallbackLocale: 'en',
      messages: {},
      dateTimeFormats: {},
      numberFormats: {},
      pluralizationRules: {},
      ...config
    }

    this.currentLocale = this.config.locale
    this.fallbackLocale = this.config.fallbackLocale
    this.messages = { ...this.config.messages }
    this.dateTimeFormats = { ...this.config.dateTimeFormats }
    this.numberFormats = { ...this.config.numberFormats }
    this.pluralizationRules = { ...this.config.pluralizationRules }
  }

  /**
   * Устанавливает локаль
   */
  setLocale(locale: string): void {
    this.currentLocale = locale
    localStorage.setItem('vuege_locale', locale)
  }

  /**
   * Получает текущую локаль
   */
  getLocale(): string {
    return this.currentLocale
  }

  /**
   * Устанавливает локаль по умолчанию
   */
  setFallbackLocale(locale: string): void {
    this.fallbackLocale = locale
  }

  /**
   * Получает локаль по умолчанию
   */
  getFallbackLocale(): string {
    return this.fallbackLocale
  }

  /**
   * Добавляет переводы
   */
  addMessages(locale: string, messages: Translation): void {
    if (!this.messages[locale]) {
      this.messages[locale] = {}
    }
    
    this.messages[locale] = { ...this.messages[locale], ...messages }
  }

  /**
   * Получает переводы для локали
   */
  getMessages(locale?: string): Translation {
    const targetLocale = locale || this.currentLocale
    return this.messages[targetLocale] || this.messages[this.fallbackLocale] || {}
  }

  /**
   * Переводит ключ
   */
  t(key: string, params?: Record<string, any>): string {
    const messages = this.getMessages()
    let message = this.getNestedValue(messages, key)

    if (!message) {
      // Пробуем fallback
      const fallbackMessages = this.messages[this.fallbackLocale]
      message = this.getNestedValue(fallbackMessages, key)
    }

    if (!message) {
      console.warn(`Translation key not found: ${key}`)
      return key
    }

    // Заменяем параметры
    if (params) {
      message = this.interpolate(message, params)
    }

    return message
  }

  /**
   * Переводит ключ с плюрализацией
   */
  tc(key: string, count: number, params?: Record<string, any>): string {
    const messages = this.getMessages()
    let message = this.getNestedValue(messages, key)

    if (!message) {
      const fallbackMessages = this.messages[this.fallbackLocale]
      message = this.getNestedValue(fallbackMessages, key)
    }

    if (!message) {
      console.warn(`Translation key not found: ${key}`)
      return key
    }

    // Применяем плюрализацию
    const pluralRule = this.pluralizationRules[this.currentLocale]
    if (pluralRule && typeof message === 'object') {
      const pluralIndex = pluralRule(count)
      message = message[pluralIndex] || message[0] || key
    }

    // Заменяем параметры
    if (params) {
      message = this.interpolate(message, { ...params, count })
    }

    return message
  }

  /**
   * Форматирует дату
   */
  formatDate(date: Date | string | number, format?: string): string {
    const targetDate = new Date(date)
    const dateFormat = format || this.dateTimeFormats[this.currentLocale]?.date || 'short'
    
    return new Intl.DateTimeFormat(this.currentLocale, {
      dateStyle: dateFormat
    }).format(targetDate)
  }

  /**
   * Форматирует время
   */
  formatTime(date: Date | string | number, format?: string): string {
    const targetDate = new Date(date)
    const timeFormat = format || this.dateTimeFormats[this.currentLocale]?.time || 'short'
    
    return new Intl.DateTimeFormat(this.currentLocale, {
      timeStyle: timeFormat
    }).format(targetDate)
  }

  /**
   * Форматирует дату и время
   */
  formatDateTime(date: Date | string | number, format?: string): string {
    const targetDate = new Date(date)
    const dateTimeFormat = format || this.dateTimeFormats[this.currentLocale]?.datetime || 'short'
    
    return new Intl.DateTimeFormat(this.currentLocale, {
      dateStyle: dateTimeFormat,
      timeStyle: dateTimeFormat
    }).format(targetDate)
  }

  /**
   * Форматирует число
   */
  formatNumber(number: number, format?: string): string {
    const numberFormat = format || this.numberFormats[this.currentLocale]?.number || 'decimal'
    
    return new Intl.NumberFormat(this.currentLocale, {
      style: numberFormat
    }).format(number)
  }

  /**
   * Форматирует валюту
   */
  formatCurrency(amount: number, currency: string = 'RUB', format?: string): string {
    const currencyFormat = format || this.numberFormats[this.currentLocale]?.currency || 'currency'
    
    return new Intl.NumberFormat(this.currentLocale, {
      style: 'currency',
      currency
    }).format(amount)
  }

  /**
   * Форматирует проценты
   */
  formatPercent(value: number, format?: string): string {
    const percentFormat = format || this.numberFormats[this.currentLocale]?.percent || 'percent'
    
    return new Intl.NumberFormat(this.currentLocale, {
      style: 'percent'
    }).format(value / 100)
  }

  /**
   * Получает доступные локали
   */
  getAvailableLocales(): string[] {
    return Object.keys(this.messages)
  }

  /**
   * Проверяет, поддерживается ли локаль
   */
  isLocaleSupported(locale: string): boolean {
    return this.getAvailableLocales().includes(locale)
  }

  /**
   * Загружает переводы из файла
   */
  async loadLocale(locale: string, url: string): Promise<void> {
    try {
      const response = await fetch(url)
      const messages = await response.json()
      this.addMessages(locale, messages)
    } catch (error) {
      console.error(`Failed to load locale ${locale}:`, error)
    }
  }

  /**
   * Загружает переводы из нескольких файлов
   */
  async loadLocales(locales: Record<string, string>): Promise<void> {
    const promises = Object.entries(locales).map(([locale, url]) => 
      this.loadLocale(locale, url)
    )
    
    await Promise.all(promises)
  }

  /**
   * Экспортирует переводы
   */
  exportMessages(locale?: string): Translation {
    return this.getMessages(locale)
  }

  /**
   * Импортирует переводы
   */
  importMessages(locale: string, messages: Translation): void {
    this.addMessages(locale, messages)
  }

  /**
   * Получает статистику переводов
   */
  getStats(): Record<string, any> {
    const locales = this.getAvailableLocales()
    const stats: Record<string, any> = {}

    locales.forEach(locale => {
      const messages = this.messages[locale]
      stats[locale] = {
        keys: this.countKeys(messages),
        size: JSON.stringify(messages).length
      }
    })

    return {
      currentLocale: this.currentLocale,
      fallbackLocale: this.fallbackLocale,
      availableLocales: locales,
      stats
    }
  }

  /**
   * Приватные методы
   */
  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => {
      return current && current[key] !== undefined ? current[key] : null
    }, obj)
  }

  private interpolate(message: string, params: Record<string, any>): string {
    return message.replace(/\{(\w+)\}/g, (match, key) => {
      return params[key] !== undefined ? String(params[key]) : match
    })
  }

  private countKeys(obj: any): number {
    let count = 0
    
    const countRecursive = (obj: any) => {
      if (typeof obj === 'object' && obj !== null) {
        Object.keys(obj).forEach(key => {
          count++
          countRecursive(obj[key])
        })
      }
    }
    
    countRecursive(obj)
    return count
  }
}

/**
 * Глобальный менеджер i18n
 */
let globalI18nManager: I18nManager | null = null

/**
 * Получает глобальный менеджер i18n
 */
export function getGlobalI18nManager(): I18nManager {
  if (!globalI18nManager) {
    globalI18nManager = new I18nManager()
  }
  return globalI18nManager
}

/**
 * Устанавливает глобальный менеджер i18n
 */
export function setGlobalI18nManager(manager: I18nManager): void {
  globalI18nManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const i18nManager = {
  setLocale: (locale: string) => getGlobalI18nManager().setLocale(locale),
  getLocale: () => getGlobalI18nManager().getLocale(),
  setFallbackLocale: (locale: string) => getGlobalI18nManager().setFallbackLocale(locale),
  getFallbackLocale: () => getGlobalI18nManager().getFallbackLocale(),
  addMessages: (locale: string, messages: Translation) => getGlobalI18nManager().addMessages(locale, messages),
  getMessages: (locale?: string) => getGlobalI18nManager().getMessages(locale),
  t: (key: string, params?: Record<string, any>) => getGlobalI18nManager().t(key, params),
  tc: (key: string, count: number, params?: Record<string, any>) => getGlobalI18nManager().tc(key, count, params),
  formatDate: (date: Date | string | number, format?: string) => getGlobalI18nManager().formatDate(date, format),
  formatTime: (date: Date | string | number, format?: string) => getGlobalI18nManager().formatTime(date, format),
  formatDateTime: (date: Date | string | number, format?: string) => getGlobalI18nManager().formatDateTime(date, format),
  formatNumber: (number: number, format?: string) => getGlobalI18nManager().formatNumber(number, format),
  formatCurrency: (amount: number, currency?: string, format?: string) => getGlobalI18nManager().formatCurrency(amount, currency, format),
  formatPercent: (value: number, format?: string) => getGlobalI18nManager().formatPercent(value, format),
  getAvailableLocales: () => getGlobalI18nManager().getAvailableLocales(),
  isLocaleSupported: (locale: string) => getGlobalI18nManager().isLocaleSupported(locale),
  loadLocale: (locale: string, url: string) => getGlobalI18nManager().loadLocale(locale, url),
  loadLocales: (locales: Record<string, string>) => getGlobalI18nManager().loadLocales(locales),
  exportMessages: (locale?: string) => getGlobalI18nManager().exportMessages(locale),
  importMessages: (locale: string, messages: Translation) => getGlobalI18nManager().importMessages(locale, messages),
  getStats: () => getGlobalI18nManager().getStats()
}

/**
 * Хук для использования менеджера i18n в Vue компонентах
 */
export function useI18nManager() {
  const manager = getGlobalI18nManager()
  
  return {
    setLocale: manager.setLocale.bind(manager),
    getLocale: manager.getLocale.bind(manager),
    setFallbackLocale: manager.setFallbackLocale.bind(manager),
    getFallbackLocale: manager.getFallbackLocale.bind(manager),
    addMessages: manager.addMessages.bind(manager),
    getMessages: manager.getMessages.bind(manager),
    t: manager.t.bind(manager),
    tc: manager.tc.bind(manager),
    formatDate: manager.formatDate.bind(manager),
    formatTime: manager.formatTime.bind(manager),
    formatDateTime: manager.formatDateTime.bind(manager),
    formatNumber: manager.formatNumber.bind(manager),
    formatCurrency: manager.formatCurrency.bind(manager),
    formatPercent: manager.formatPercent.bind(manager),
    getAvailableLocales: manager.getAvailableLocales.bind(manager),
    isLocaleSupported: manager.isLocaleSupported.bind(manager),
    loadLocale: manager.loadLocale.bind(manager),
    loadLocales: manager.loadLocales.bind(manager),
    exportMessages: manager.exportMessages.bind(manager),
    importMessages: manager.importMessages.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}
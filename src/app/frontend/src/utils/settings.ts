// Утилиты для работы с настройками

/**
 * Интерфейс для настройки
 */
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

/**
 * Интерфейс для конфигурации настроек
 */
export interface SettingsConfig {
  storageKey: string
  autoSave: boolean
  validateOnChange: boolean
  categories: string[]
}

/**
 * Класс для управления настройками
 */
export class SettingsManager {
  private settings: Map<string, Setting>
  private config: SettingsConfig
  private watchers: Map<string, Set<Function>>

  constructor(config?: Partial<SettingsConfig>) {
    this.config = {
      storageKey: 'vuege_settings',
      autoSave: true,
      validateOnChange: true,
      categories: ['general', 'display', 'api', 'security', 'advanced'],
      ...config
    }

    this.settings = new Map()
    this.watchers = new Map()

    this.loadSettings()
  }

  /**
   * Добавляет настройку
   */
  addSetting<T>(setting: Setting<T>): void {
    this.settings.set(setting.key, setting)
    
    // Устанавливаем значение по умолчанию, если не существует
    if (!this.hasValue(setting.key)) {
      this.setValue(setting.key, setting.defaultValue)
    }
  }

  /**
   * Получает настройку
   */
  getSetting<T>(key: string): Setting<T> | null {
    return this.settings.get(key) as Setting<T> | null
  }

  /**
   * Удаляет настройку
   */
  removeSetting(key: string): boolean {
    return this.settings.delete(key)
  }

  /**
   * Получает значение настройки
   */
  getValue<T>(key: string): T | null {
    const setting = this.settings.get(key)
    if (!setting) {
      return null
    }

    const storedValue = localStorage.getItem(`${this.config.storageKey}_${key}`)
    
    if (storedValue !== null) {
      try {
        return JSON.parse(storedValue)
      } catch {
        return setting.defaultValue
      }
    }

    return setting.defaultValue
  }

  /**
   * Устанавливает значение настройки
   */
  setValue<T>(key: string, value: T): boolean {
    const setting = this.settings.get(key)
    if (!setting) {
      return false
    }

    // Валидация
    if (this.config.validateOnChange && setting.validation) {
      const validationResult = setting.validation(value)
      if (validationResult !== true) {
        console.error(`Validation failed for setting ${key}:`, validationResult)
        return false
      }
    }

    // Сохраняем в localStorage
    localStorage.setItem(`${this.config.storageKey}_${key}`, JSON.stringify(value))
    
    // Обновляем значение в настройке
    setting.value = value

    // Уведомляем наблюдателей
    this.notifyWatchers(key, value)

    return true
  }

  /**
   * Проверяет, существует ли значение настройки
   */
  hasValue(key: string): boolean {
    return localStorage.getItem(`${this.config.storageKey}_${key}`) !== null
  }

  /**
   * Сбрасывает настройку к значению по умолчанию
   */
  resetSetting(key: string): boolean {
    const setting = this.settings.get(key)
    if (!setting) {
      return false
    }

    return this.setValue(key, setting.defaultValue)
  }

  /**
   * Сбрасывает все настройки к значениям по умолчанию
   */
  resetAllSettings(): void {
    this.settings.forEach((setting, key) => {
      this.setValue(key, setting.defaultValue)
    })
  }

  /**
   * Получает настройки по категории
   */
  getSettingsByCategory(category: string): Setting[] {
    return Array.from(this.settings.values()).filter(setting => setting.category === category)
  }

  /**
   * Получает все категории
   */
  getCategories(): string[] {
    const categories = new Set(this.settings.values().map(setting => setting.category))
    return Array.from(categories).sort()
  }

  /**
   * Получает все настройки
   */
  getAllSettings(): Setting[] {
    return Array.from(this.settings.values())
  }

  /**
   * Получает видимые настройки
   */
  getVisibleSettings(): Setting[] {
    return Array.from(this.settings.values()).filter(setting => !setting.hidden)
  }

  /**
   * Подписывается на изменения настройки
   */
  watch(key: string, callback: Function): () => void {
    if (!this.watchers.has(key)) {
      this.watchers.set(key, new Set())
    }

    this.watchers.get(key)!.add(callback)

    return () => {
      const watchers = this.watchers.get(key)
      if (watchers) {
        watchers.delete(callback)
        if (watchers.size === 0) {
          this.watchers.delete(key)
        }
      }
    }
  }

  /**
   * Уведомляет наблюдателей об изменениях
   */
  private notifyWatchers(key: string, value: any): void {
    const watchers = this.watchers.get(key)
    if (watchers) {
      watchers.forEach(callback => {
        try {
          callback(value)
        } catch (error) {
          console.error(`Error in settings watcher for ${key}:`, error)
        }
      })
    }
  }

  /**
   * Загружает настройки из localStorage
   */
  private loadSettings(): void {
    // Настройки загружаются по требованию в getValue
  }

  /**
   * Сохраняет настройки в localStorage
   */
  saveSettings(): void {
    this.settings.forEach((setting, key) => {
      const value = this.getValue(key)
      if (value !== null) {
        localStorage.setItem(`${this.config.storageKey}_${key}`, JSON.stringify(value))
      }
    })
  }

  /**
   * Экспортирует настройки
   */
  exportSettings(): Record<string, any> {
    const exported: Record<string, any> = {}
    
    this.settings.forEach((setting, key) => {
      const value = this.getValue(key)
      if (value !== null) {
        exported[key] = {
          value,
          type: setting.type,
          category: setting.category,
          label: setting.label,
          description: setting.description
        }
      }
    })

    return exported
  }

  /**
   * Импортирует настройки
   */
  importSettings(data: Record<string, any>): void {
    Object.entries(data).forEach(([key, item]) => {
      if (this.settings.has(key)) {
        this.setValue(key, item.value)
      }
    })
  }

  /**
   * Получает статистику настроек
   */
  getStats(): Record<string, any> {
    const categories = this.getCategories()
    const stats: Record<string, any> = {}

    categories.forEach(category => {
      const settings = this.getSettingsByCategory(category)
      stats[category] = {
        total: settings.length,
        visible: settings.filter(s => !s.hidden).length,
        required: settings.filter(s => s.required).length,
        readonly: settings.filter(s => s.readonly).length
      }
    })

    return {
      totalSettings: this.settings.size,
      categories: categories.length,
      watchers: Array.from(this.watchers.values()).reduce((sum, watchers) => sum + watchers.size, 0),
      stats
    }
  }

  /**
   * Обновляет конфигурацию
   */
  updateConfig(newConfig: Partial<SettingsConfig>): void {
    this.config = { ...this.config, ...newConfig }
  }

  /**
   * Получает конфигурацию
   */
  getConfig(): SettingsConfig {
    return { ...this.config }
  }
}

/**
 * Глобальный менеджер настроек
 */
let globalSettingsManager: SettingsManager | null = null

/**
 * Получает глобальный менеджер настроек
 */
export function getGlobalSettingsManager(): SettingsManager {
  if (!globalSettingsManager) {
    globalSettingsManager = new SettingsManager()
  }
  return globalSettingsManager
}

/**
 * Устанавливает глобальный менеджер настроек
 */
export function setGlobalSettingsManager(manager: SettingsManager): void {
  globalSettingsManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const settingsManager = {
  addSetting: <T>(setting: Setting<T>) => getGlobalSettingsManager().addSetting(setting),
  getSetting: <T>(key: string) => getGlobalSettingsManager().getSetting<T>(key),
  removeSetting: (key: string) => getGlobalSettingsManager().removeSetting(key),
  getValue: <T>(key: string) => getGlobalSettingsManager().getValue<T>(key),
  setValue: <T>(key: string, value: T) => getGlobalSettingsManager().setValue(key, value),
  hasValue: (key: string) => getGlobalSettingsManager().hasValue(key),
  resetSetting: (key: string) => getGlobalSettingsManager().resetSetting(key),
  resetAllSettings: () => getGlobalSettingsManager().resetAllSettings(),
  getSettingsByCategory: (category: string) => getGlobalSettingsManager().getSettingsByCategory(category),
  getCategories: () => getGlobalSettingsManager().getCategories(),
  getAllSettings: () => getGlobalSettingsManager().getAllSettings(),
  getVisibleSettings: () => getGlobalSettingsManager().getVisibleSettings(),
  watch: (key: string, callback: Function) => getGlobalSettingsManager().watch(key, callback),
  saveSettings: () => getGlobalSettingsManager().saveSettings(),
  exportSettings: () => getGlobalSettingsManager().exportSettings(),
  importSettings: (data: Record<string, any>) => getGlobalSettingsManager().importSettings(data),
  getStats: () => getGlobalSettingsManager().getStats(),
  updateConfig: (newConfig: Partial<SettingsConfig>) => getGlobalSettingsManager().updateConfig(newConfig),
  getConfig: () => getGlobalSettingsManager().getConfig()
}

/**
 * Хук для использования менеджера настроек в Vue компонентах
 */
export function useSettingsManager() {
  const manager = getGlobalSettingsManager()
  
  return {
    addSetting: manager.addSetting.bind(manager),
    getSetting: manager.getSetting.bind(manager),
    removeSetting: manager.removeSetting.bind(manager),
    getValue: manager.getValue.bind(manager),
    setValue: manager.setValue.bind(manager),
    hasValue: manager.hasValue.bind(manager),
    resetSetting: manager.resetSetting.bind(manager),
    resetAllSettings: manager.resetAllSettings.bind(manager),
    getSettingsByCategory: manager.getSettingsByCategory.bind(manager),
    getCategories: manager.getCategories.bind(manager),
    getAllSettings: manager.getAllSettings.bind(manager),
    getVisibleSettings: manager.getVisibleSettings.bind(manager),
    watch: manager.watch.bind(manager),
    saveSettings: manager.saveSettings.bind(manager),
    exportSettings: manager.exportSettings.bind(manager),
    importSettings: manager.importSettings.bind(manager),
    getStats: manager.getStats.bind(manager),
    updateConfig: manager.updateConfig.bind(manager),
    getConfig: manager.getConfig.bind(manager)
  }
}
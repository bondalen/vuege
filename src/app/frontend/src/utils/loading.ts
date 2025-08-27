// Утилиты для работы с загрузкой

import { useQuasar } from 'quasar'

/**
 * Интерфейс для конфигурации загрузки
 */
export interface LoadingConfig {
  message?: string
  spinner?: string
  spinnerColor?: string
  spinnerSize?: string
  backgroundColor?: string
  customClass?: string
  delay?: number
  onShow?: () => void
  onHide?: () => void
}

/**
 * Класс для управления загрузкой
 */
export class LoadingManager {
  private $q: any
  private activeLoadings: Map<string, any>
  private counter: number

  constructor() {
    this.activeLoadings = new Map()
    this.counter = 0
  }

  /**
   * Инициализирует менеджер с Quasar
   */
  init($q: any): void {
    this.$q = $q
  }

  /**
   * Показывает индикатор загрузки
   */
  show(config?: LoadingConfig): string {
    const id = `loading_${++this.counter}`
    
    const loading = this.$q.loading.show({
      message: config?.message || 'Загрузка...',
      spinner: config?.spinner || 'QSpinnerGears',
      spinnerColor: config?.spinnerColor || 'primary',
      spinnerSize: config?.spinnerSize || '50px',
      backgroundColor: config?.backgroundColor || 'white',
      customClass: config?.customClass,
      delay: config?.delay || 0,
      onShow: () => {
        if (config?.onShow) {
          config.onShow()
        }
      },
      onHide: () => {
        this.activeLoadings.delete(id)
        if (config?.onHide) {
          config.onHide()
        }
      }
    })

    this.activeLoadings.set(id, loading)
    return id
  }

  /**
   * Скрывает индикатор загрузки
   */
  hide(id?: string): void {
    if (id) {
      const loading = this.activeLoadings.get(id)
      if (loading) {
        loading()
        this.activeLoadings.delete(id)
      }
    } else {
      this.$q.loading.hide()
      this.activeLoadings.clear()
    }
  }

  /**
   * Проверяет, активно ли загрузка
   */
  isActive(id?: string): boolean {
    if (id) {
      return this.activeLoadings.has(id)
    }
    return this.activeLoadings.size > 0
  }

  /**
   * Получает все активные загрузки
   */
  getActive(): string[] {
    return Array.from(this.activeLoadings.keys())
  }

  /**
   * Обновляет сообщение загрузки
   */
  updateMessage(id: string, message: string): void {
    const loading = this.activeLoadings.get(id)
    if (loading) {
      // Закрываем старое и создаем новое
      loading()
      this.activeLoadings.delete(id)
      
      const newId = this.show({ message })
      this.activeLoadings.set(id, this.activeLoadings.get(newId))
      this.activeLoadings.delete(newId)
    }
  }

  /**
   * Показывает загрузку с автоматическим скрытием
   */
  async withLoading<T>(
    promise: Promise<T>,
    config?: LoadingConfig
  ): Promise<T> {
    const id = this.show(config)
    
    try {
      const result = await promise
      return result
    } finally {
      this.hide(id)
    }
  }

  /**
   * Показывает загрузку с прогрессом
   */
  showWithProgress(
    message: string,
    progress: number,
    config?: LoadingConfig
  ): string {
    const progressMessage = `${message} (${Math.round(progress)}%)`
    return this.show({ ...config, message: progressMessage })
  }

  /**
   * Получает статистику загрузки
   */
  getStats(): Record<string, any> {
    return {
      activeLoadings: this.activeLoadings.size,
      loadingIds: Array.from(this.activeLoadings.keys()),
      counter: this.counter
    }
  }
}

/**
 * Глобальный менеджер загрузки
 */
let globalLoadingManager: LoadingManager | null = null

/**
 * Получает глобальный менеджер загрузки
 */
export function getGlobalLoadingManager(): LoadingManager {
  if (!globalLoadingManager) {
    globalLoadingManager = new LoadingManager()
  }
  return globalLoadingManager
}

/**
 * Устанавливает глобальный менеджер загрузки
 */
export function setGlobalLoadingManager(manager: LoadingManager): void {
  globalLoadingManager = manager
}

/**
 * Объект со всеми функциями для работы с загрузкой
 */
export const loading = {
  init: ($q: any) => getGlobalLoadingManager().init($q),
  show: (config?: LoadingConfig) => getGlobalLoadingManager().show(config),
  hide: (id?: string) => getGlobalLoadingManager().hide(id),
  isActive: (id?: string) => getGlobalLoadingManager().isActive(id),
  getActive: () => getGlobalLoadingManager().getActive(),
  updateMessage: (id: string, message: string) => getGlobalLoadingManager().updateMessage(id, message),
  withLoading: <T>(promise: Promise<T>, config?: LoadingConfig) => getGlobalLoadingManager().withLoading(promise, config),
  showWithProgress: (message: string, progress: number, config?: LoadingConfig) => getGlobalLoadingManager().showWithProgress(message, progress, config),
  getStats: () => getGlobalLoadingManager().getStats()
}

/**
 * Алиас для useLoadingManager
 */
export const useLoading = useLoadingManager

/**
 * Хук для использования менеджера загрузки в Vue компонентах
 */
export function useLoadingManager() {
  const $q = useQuasar()
  const manager = getGlobalLoadingManager()
  
  // Инициализируем с Quasar
  manager.init($q)
  
  return {
    show: manager.show.bind(manager),
    hide: manager.hide.bind(manager),
    isActive: manager.isActive.bind(manager),
    getActive: manager.getActive.bind(manager),
    updateMessage: manager.updateMessage.bind(manager),
    withLoading: manager.withLoading.bind(manager),
    showWithProgress: manager.showWithProgress.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

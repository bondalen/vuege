// Утилиты для работы с уведомлениями

import { useQuasar } from 'quasar'

/**
 * Интерфейс для конфигурации уведомления
 */
export interface NotificationConfig {
  message: string
  caption?: string
  icon?: string
  color?: string
  textColor?: string
  bgColor?: string
  position?: 'top' | 'bottom' | 'left' | 'right' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center'
  timeout?: number
  multiLine?: boolean
  html?: boolean
  actions?: NotificationAction[]
  progress?: boolean
  spinner?: boolean
  spinnerColor?: string
  spinnerSize?: string
  persistent?: boolean
  classes?: string
  style?: string
  attrs?: Record<string, any>
  onDismiss?: () => void
  onAction?: (action: NotificationAction) => void
  onTimeout?: () => void
  onShow?: () => void
  onHide?: () => void
}

/**
 * Интерфейс для действия уведомления
 */
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

/**
 * Класс для управления уведомлениями
 */
export class NotificationManager {
  private $q: any
  private notifications: Map<string, any>
  private counter: number

  constructor() {
    this.notifications = new Map()
    this.counter = 0
  }

  /**
   * Инициализирует менеджер с Quasar
   */
  init($q: any): void {
    this.$q = $q
  }

  /**
   * Показывает уведомление
   */
  show(config: NotificationConfig): string {
    const id = `notification_${++this.counter}`
    
    const notification = this.$q.notify({
      message: config.message,
      caption: config.caption,
      icon: config.icon,
      color: config.color || 'primary',
      textColor: config.textColor,
      bgColor: config.bgColor,
      position: config.position || 'top',
      timeout: config.timeout || 5000,
      multiLine: config.multiLine || false,
      html: config.html || false,
      actions: config.actions || [],
      progress: config.progress || false,
      spinner: config.spinner || false,
      spinnerColor: config.spinnerColor,
      spinnerSize: config.spinnerSize,
      classes: config.classes,
      style: config.style,
      attrs: config.attrs,
      onDismiss: () => {
        this.notifications.delete(id)
        if (config.onDismiss) {
          config.onDismiss()
        }
      },
      onAction: (action: NotificationAction) => {
        if (config.onAction) {
          config.onAction(action)
        }
        if (action.onClick) {
          action.onClick()
        }
      },
      onTimeout: () => {
        this.notifications.delete(id)
        if (config.onTimeout) {
          config.onTimeout()
        }
      },
      onShow: () => {
        if (config.onShow) {
          config.onShow()
        }
      },
      onHide: () => {
        this.notifications.delete(id)
        if (config.onHide) {
          config.onHide()
        }
      }
    })

    this.notifications.set(id, notification)
    return id
  }

  /**
   * Показывает уведомление об успехе
   */
  success(message: string, config?: Partial<NotificationConfig>): string {
    return this.show({
      message,
      icon: 'check_circle',
      color: 'positive',
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает уведомление об ошибке
   */
  error(message: string, config?: Partial<NotificationConfig>): string {
    return this.show({
      message,
      icon: 'error',
      color: 'negative',
      timeout: 8000,
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает уведомление с предупреждением
   */
  warning(message: string, config?: Partial<NotificationConfig>): string {
    return this.show({
      message,
      icon: 'warning',
      color: 'warning',
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает информационное уведомление
   */
  info(message: string, config?: Partial<NotificationConfig>): string {
    return this.show({
      message,
      icon: 'info',
      color: 'info',
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает уведомление с загрузкой
   */
  loading(message: string, config?: Partial<NotificationConfig>): string {
    return this.show({
      message,
      icon: 'hourglass_empty',
      color: 'primary',
      spinner: true,
      timeout: 0,
      persistent: true,
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает уведомление с прогрессом
   */
  progress(message: string, _progress: number, config?: Partial<NotificationConfig>): string {
    return this.show({
      message,
      icon: 'trending_up',
      color: 'primary',
      progress: true,
      timeout: 0,
      persistent: true,
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает уведомление с кнопками действий
   */
  action(
    message: string,
    actions: NotificationAction[],
    config?: Partial<NotificationConfig>
  ): string {
    return this.show({
      message,
      actions,
      timeout: 0,
      persistent: true,
      ...config
    } as NotificationConfig)
  }

  /**
   * Показывает уведомление с подтверждением
   */
  confirm(
    message: string,
    onConfirm?: () => void,
    onCancel?: () => void,
    config?: Partial<NotificationConfig>
  ): string {
    const actions: NotificationAction[] = [
      {
        label: 'Отмена',
        color: 'grey',
        flat: true,
        onClick: () => {
          this.dismiss(id)
          if (onCancel) onCancel()
        }
      },
      {
        label: 'Подтвердить',
        color: 'primary',
        flat: true,
        onClick: () => {
          this.dismiss(id)
          if (onConfirm) onConfirm()
        }
      }
    ]

    const id = this.action(message, actions, config)
    return id
  }

  /**
   * Показывает уведомление с вводом
   */
  prompt(
    message: string,
    _placeholder: string = 'Введите значение',
    onConfirm?: (value: string) => void,
    onCancel?: () => void,
    config?: Partial<NotificationConfig>
  ): string {
    let inputValue = ''

    const actions: NotificationAction[] = [
      {
        label: 'Отмена',
        color: 'grey',
        flat: true,
        onClick: () => {
          this.dismiss(id)
          if (onCancel) onCancel()
        }
      },
      {
        label: 'OK',
        color: 'primary',
        flat: true,
        onClick: () => {
          this.dismiss(id)
          if (onConfirm) onConfirm(inputValue)
        }
      }
    ]

    const id = this.show({
      message,
      html: true,
      actions,
      timeout: 0,
      persistent: true,
      ...config
    })

    // Добавляем поле ввода
    const notification = this.notifications.get(id)
    if (notification) {
      // Здесь нужно добавить поле ввода в уведомление
      // Это требует дополнительной реализации
    }

    return id
  }

  /**
   * Закрывает уведомление
   */
  dismiss(id: string): void {
    const notification = this.notifications.get(id)
    if (notification) {
      notification()
      this.notifications.delete(id)
    }
  }

  /**
   * Закрывает все уведомления
   */
  dismissAll(): void {
    this.notifications.forEach(notification => {
      notification()
    })
    this.notifications.clear()
  }

  /**
   * Получает уведомление по ID
   */
  get(id: string): any {
    return this.notifications.get(id)
  }

  /**
   * Проверяет, активно ли уведомление
   */
  isActive(id: string): boolean {
    return this.notifications.has(id)
  }

  /**
   * Получает все активные уведомления
   */
  getAll(): string[] {
    return Array.from(this.notifications.keys())
  }

  /**
   * Обновляет уведомление
   */
  update(id: string, updates: Partial<NotificationConfig>): void {
    const notification = this.notifications.get(id)
    if (notification) {
      // Закрываем старое уведомление
      notification()
      this.notifications.delete(id)

      // Создаем новое с обновленной конфигурацией
      const newId = this.show(updates as NotificationConfig)
      this.notifications.set(id, this.notifications.get(newId))
      this.notifications.delete(newId)
    }
  }

  /**
   * Показывает уведомление о копировании
   */
  copySuccess(text: string): string {
    return this.success(`Скопировано: ${text}`, {
      timeout: 2000,
      position: 'bottom'
    })
  }

  /**
   * Показывает уведомление о сохранении
   */
  saveSuccess(item: string): string {
    return this.success(`${item} успешно сохранен`, {
      timeout: 3000
    })
  }

  /**
   * Показывает уведомление об удалении
   */
  deleteSuccess(item: string): string {
    return this.success(`${item} успешно удален`, {
      timeout: 3000
    })
  }

  /**
   * Показывает уведомление о создании
   */
  createSuccess(item: string): string {
    return this.success(`${item} успешно создан`, {
      timeout: 3000
    })
  }

  /**
   * Показывает уведомление об обновлении
   */
  updateSuccess(item: string): string {
    return this.success(`${item} успешно обновлен`, {
      timeout: 3000
    })
  }

  /**
   * Показывает уведомление о загрузке
   */
  uploadSuccess(filename: string): string {
    return this.success(`Файл "${filename}" успешно загружен`, {
      timeout: 3000
    })
  }

  /**
   * Показывает уведомление о скачивании
   */
  downloadSuccess(filename: string): string {
    return this.success(`Файл "${filename}" успешно скачан`, {
      timeout: 3000
    })
  }

  /**
   * Показывает уведомление о подключении
   */
  connectionSuccess(): string {
    return this.success('Соединение восстановлено', {
      timeout: 2000
    })
  }

  /**
   * Показывает уведомление о потере соединения
   */
  connectionError(): string {
    return this.error('Соединение потеряно', {
      timeout: 0,
      persistent: true
    })
  }

  /**
   * Показывает уведомление о синхронизации
   */
  syncSuccess(): string {
    return this.success('Данные синхронизированы', {
      timeout: 2000
    })
  }

  /**
   * Показывает уведомление об ошибке синхронизации
   */
  syncError(): string {
    return this.error('Ошибка синхронизации', {
      timeout: 5000
    })
  }

  /**
   * Показывает уведомление о валидации
   */
  validationError(field: string): string {
    return this.error(`Ошибка валидации: ${field}`, {
      timeout: 5000
    })
  }

  /**
   * Показывает уведомление о разрешениях
   */
  permissionError(action: string): string {
    return this.error(`Недостаточно прав для: ${action}`, {
      timeout: 5000
    })
  }

  /**
   * Показывает уведомление о блокировке
   */
  lockSuccess(item: string): string {
    return this.success(`${item} заблокирован`, {
      timeout: 2000
    })
  }

  /**
   * Показывает уведомление о разблокировке
   */
  unlockSuccess(item: string): string {
    return this.success(`${item} разблокирован`, {
      timeout: 2000
    })
  }

  /**
   * Получает статистику уведомлений
   */
  getStats(): Record<string, any> {
    return {
      totalNotifications: this.notifications.size,
      activeNotifications: Array.from(this.notifications.keys()),
      counter: this.counter
    }
  }
}

/**
 * Глобальный менеджер уведомлений
 */
let globalNotificationManager: NotificationManager | null = null

/**
 * Получает глобальный менеджер уведомлений
 */
export function getGlobalNotificationManager(): NotificationManager {
  if (!globalNotificationManager) {
    globalNotificationManager = new NotificationManager()
  }
  return globalNotificationManager
}

/**
 * Устанавливает глобальный менеджер уведомлений
 */
export function setGlobalNotificationManager(manager: NotificationManager): void {
  globalNotificationManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const notificationManager = {
  init: ($q: any) => getGlobalNotificationManager().init($q),
  show: (config: NotificationConfig) => getGlobalNotificationManager().show(config),
  success: (message: string, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().success(message, config),
  error: (message: string, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().error(message, config),
  warning: (message: string, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().warning(message, config),
  info: (message: string, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().info(message, config),
  loading: (message: string, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().loading(message, config),
  progress: (message: string, progress: number, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().progress(message, progress, config),
  action: (message: string, actions: NotificationAction[], config?: Partial<NotificationConfig>) => getGlobalNotificationManager().action(message, actions, config),
  confirm: (message: string, onConfirm?: () => void, onCancel?: () => void, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().confirm(message, onConfirm, onCancel, config),
  prompt: (message: string, placeholder?: string, onConfirm?: (value: string) => void, onCancel?: () => void, config?: Partial<NotificationConfig>) => getGlobalNotificationManager().prompt(message, placeholder, onConfirm, onCancel, config),
  dismiss: (id: string) => getGlobalNotificationManager().dismiss(id),
  dismissAll: () => getGlobalNotificationManager().dismissAll(),
  get: (id: string) => getGlobalNotificationManager().get(id),
  isActive: (id: string) => getGlobalNotificationManager().isActive(id),
  getAll: () => getGlobalNotificationManager().getAll(),
  update: (id: string, updates: Partial<NotificationConfig>) => getGlobalNotificationManager().update(id, updates),
  copySuccess: (text: string) => getGlobalNotificationManager().copySuccess(text),
  saveSuccess: (item: string) => getGlobalNotificationManager().saveSuccess(item),
  deleteSuccess: (item: string) => getGlobalNotificationManager().deleteSuccess(item),
  createSuccess: (item: string) => getGlobalNotificationManager().createSuccess(item),
  updateSuccess: (item: string) => getGlobalNotificationManager().updateSuccess(item),
  uploadSuccess: (filename: string) => getGlobalNotificationManager().uploadSuccess(filename),
  downloadSuccess: (filename: string) => getGlobalNotificationManager().downloadSuccess(filename),
  connectionSuccess: () => getGlobalNotificationManager().connectionSuccess(),
  connectionError: () => getGlobalNotificationManager().connectionError(),
  syncSuccess: () => getGlobalNotificationManager().syncSuccess(),
  syncError: () => getGlobalNotificationManager().syncError(),
  validationError: (field: string) => getGlobalNotificationManager().validationError(field),
  permissionError: (action: string) => getGlobalNotificationManager().permissionError(action),
  lockSuccess: (item: string) => getGlobalNotificationManager().lockSuccess(item),
  unlockSuccess: (item: string) => getGlobalNotificationManager().unlockSuccess(item),
  getStats: () => getGlobalNotificationManager().getStats()
}

/**
 * Хук для использования менеджера уведомлений в Vue компонентах
 */
export function useNotificationManager() {
  const $q = useQuasar()
  const manager = getGlobalNotificationManager()
  
  // Инициализируем с Quasar
  manager.init($q)
  
  return {
    show: manager.show.bind(manager),
    success: manager.success.bind(manager),
    error: manager.error.bind(manager),
    warning: manager.warning.bind(manager),
    info: manager.info.bind(manager),
    loading: manager.loading.bind(manager),
    progress: manager.progress.bind(manager),
    action: manager.action.bind(manager),
    confirm: manager.confirm.bind(manager),
    prompt: manager.prompt.bind(manager),
    dismiss: manager.dismiss.bind(manager),
    dismissAll: manager.dismissAll.bind(manager),
    get: manager.get.bind(manager),
    isActive: manager.isActive.bind(manager),
    getAll: manager.getAll.bind(manager),
    update: manager.update.bind(manager),
    copySuccess: manager.copySuccess.bind(manager),
    saveSuccess: manager.saveSuccess.bind(manager),
    deleteSuccess: manager.deleteSuccess.bind(manager),
    createSuccess: manager.createSuccess.bind(manager),
    updateSuccess: manager.updateSuccess.bind(manager),
    uploadSuccess: manager.uploadSuccess.bind(manager),
    downloadSuccess: manager.downloadSuccess.bind(manager),
    connectionSuccess: manager.connectionSuccess.bind(manager),
    connectionError: manager.connectionError.bind(manager),
    syncSuccess: manager.syncSuccess.bind(manager),
    syncError: manager.syncError.bind(manager),
    validationError: manager.validationError.bind(manager),
    permissionError: manager.permissionError.bind(manager),
    lockSuccess: manager.lockSuccess.bind(manager),
    unlockSuccess: manager.unlockSuccess.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

export const notifications = { 
  NotificationManager,
  getGlobalNotificationManager,
  setGlobalNotificationManager,
  notificationManager,
  useNotificationManager
}

/**
 * Алиас для useNotificationManager
 */
export const useNotifications = useNotificationManager

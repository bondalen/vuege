// Утилиты для работы с диалогами

import { useQuasar } from 'quasar'

/**
 * Опции диалога подтверждения
 */
export interface ConfirmDialogOptions {
  title?: string
  message: string
  okLabel?: string
  cancelLabel?: string
  persistent?: boolean
  color?: string
  icon?: string
  html?: boolean
  style?: string
  class?: string
}

/**
 * Опции диалога ввода
 */
export interface PromptDialogOptions {
  title?: string
  message?: string
  defaultValue?: string
  placeholder?: string
  type?: 'text' | 'password' | 'email' | 'number' | 'tel' | 'url'
  pattern?: string
  required?: boolean
  minLength?: number
  maxLength?: number
  okLabel?: string
  cancelLabel?: string
  persistent?: boolean
  color?: string
  icon?: string
  style?: string
  class?: string
}

/**
 * Опции диалога выбора
 */
export interface SelectDialogOptions {
  title?: string
  message?: string
  options: Array<{
    label: string
    value: any
    icon?: string
    color?: string
  }>
  selectedValue?: any
  multiple?: boolean
  okLabel?: string
  cancelLabel?: string
  persistent?: boolean
  color?: string
  icon?: string
  style?: string
  class?: string
}

/**
 * Класс для управления диалогами
 */
export class DialogManager {
  private $q: any

  constructor() {
    this.$q = useQuasar()
  }

  /**
   * Показывает диалог подтверждения
   */
  async confirm(options: ConfirmDialogOptions): Promise<boolean> {
    return new Promise((resolve) => {
      this.$q.dialog({
        title: options.title || 'Подтверждение',
        message: options.message,
        ok: {
          label: options.okLabel || 'Подтвердить',
          color: options.color || 'primary'
        },
        cancel: {
          label: options.cancelLabel || 'Отмена',
          color: 'grey'
        },
        persistent: options.persistent !== false,
        html: options.html,
        style: options.style,
        class: options.class
      }).onOk(() => {
        resolve(true)
      }).onCancel(() => {
        resolve(false)
      }).onDismiss(() => {
        resolve(false)
      })
    })
  }

  /**
   * Показывает диалог ввода
   */
  async prompt(options: PromptDialogOptions): Promise<string | null> {
    return new Promise((resolve) => {
      this.$q.dialog({
        title: options.title || 'Ввод',
        message: options.message,
        prompt: {
          model: options.defaultValue || '',
          type: options.type || 'text',
          placeholder: options.placeholder,
          pattern: options.pattern,
          required: options.required,
          minLength: options.minLength,
          maxLength: options.maxLength
        },
        ok: {
          label: options.okLabel || 'OK',
          color: options.color || 'primary'
        },
        cancel: {
          label: options.cancelLabel || 'Отмена',
          color: 'grey'
        },
        persistent: options.persistent !== false,
        style: options.style,
        class: options.class
      }).onOk((data: string) => {
        resolve(data)
      }).onCancel(() => {
        resolve(null)
      }).onDismiss(() => {
        resolve(null)
      })
    })
  }

  /**
   * Показывает диалог выбора
   */
  async select(options: SelectDialogOptions): Promise<any | null> {
    return new Promise((resolve) => {
      this.$q.dialog({
        title: options.title || 'Выбор',
        message: options.message,
        options: {
          type: options.multiple ? 'checkbox' : 'radio',
          model: options.selectedValue,
          items: options.options.map(option => ({
            label: option.label,
            value: option.value,
            icon: option.icon,
            color: option.color
          }))
        },
        ok: {
          label: options.okLabel || 'OK',
          color: options.color || 'primary'
        },
        cancel: {
          label: options.cancelLabel || 'Отмена',
          color: 'grey'
        },
        persistent: options.persistent !== false,
        style: options.style,
        class: options.class
      }).onOk((data: any) => {
        resolve(data)
      }).onCancel(() => {
        resolve(null)
      }).onDismiss(() => {
        resolve(null)
      })
    })
  }

  /**
   * Показывает диалог удаления
   */
  async confirmDelete(resourceName: string, options?: Partial<ConfirmDialogOptions>): Promise<boolean> {
    return this.confirm({
      title: 'Подтверждение удаления',
      message: `Вы уверены, что хотите удалить "${resourceName}"?`,
      okLabel: 'Удалить',
      color: 'negative',
      icon: 'delete',
      persistent: true,
      ...options
    })
  }

  /**
   * Показывает диалог сохранения
   */
  async confirmSave(options?: Partial<ConfirmDialogOptions>): Promise<boolean> {
    return this.confirm({
      title: 'Подтверждение сохранения',
      message: 'Сохранить изменения?',
      okLabel: 'Сохранить',
      color: 'positive',
      icon: 'save',
      ...options
    })
  }

  /**
   * Показывает диалог отмены
   */
  async confirmCancel(options?: Partial<ConfirmDialogOptions>): Promise<boolean> {
    return this.confirm({
      title: 'Подтверждение отмены',
      message: 'Отменить изменения? Все несохраненные данные будут потеряны.',
      okLabel: 'Отменить',
      color: 'warning',
      icon: 'cancel',
      ...options
    })
  }

  /**
   * Показывает диалог выхода
   */
  async confirmExit(options?: Partial<ConfirmDialogOptions>): Promise<boolean> {
    return this.confirm({
      title: 'Подтверждение выхода',
      message: 'Вы уверены, что хотите выйти? Все несохраненные данные будут потеряны.',
      okLabel: 'Выйти',
      color: 'negative',
      icon: 'exit_to_app',
      persistent: true,
      ...options
    })
  }

  /**
   * Показывает диалог с информацией
   */
  async info(title: string, message: string, options?: Partial<ConfirmDialogOptions>): Promise<void> {
    return new Promise((resolve) => {
      this.$q.dialog({
        title,
        message,
        ok: {
          label: 'OK',
          color: 'primary'
        },
        persistent: false,
        ...options
      }).onOk(() => {
        resolve()
      }).onCancel(() => {
        resolve()
      }).onDismiss(() => {
        resolve()
      })
    })
  }

  /**
   * Показывает диалог с предупреждением
   */
  async warning(title: string, message: string, options?: Partial<ConfirmDialogOptions>): Promise<void> {
    return this.info(title, message, {
      color: 'warning',
      icon: 'warning',
      ...options
    })
  }

  /**
   * Показывает диалог с ошибкой
   */
  async error(title: string, message: string, options?: Partial<ConfirmDialogOptions>): Promise<void> {
    return this.info(title, message, {
      color: 'negative',
      icon: 'error',
      ...options
    })
  }

  /**
   * Показывает диалог с успехом
   */
  async success(title: string, message: string, options?: Partial<ConfirmDialogOptions>): Promise<void> {
    return this.info(title, message, {
      color: 'positive',
      icon: 'check_circle',
      ...options
    })
  }

  /**
   * Показывает диалог загрузки
   */
  async loading(message: string = 'Загрузка...'): Promise<void> {
    return new Promise((resolve) => {
      this.$q.dialog({
        component: 'div',
        message,
        persistent: true,
        noEscDismiss: true,
        noBackdropDismiss: true,
        style: 'min-width: 200px'
      }).onOk(() => {
        resolve()
      }).onCancel(() => {
        resolve()
      }).onDismiss(() => {
        resolve()
      })
    })
  }

  /**
   * Скрывает диалог загрузки
   */
  hideLoading(): void {
    this.$q.dialog().hide()
  }

  /**
   * Показывает диалог с кастомным компонентом
   */
  async custom(component: any, props?: Record<string, any>): Promise<any> {
    return new Promise((resolve) => {
      this.$q.dialog({
        component,
        componentProps: props
      }).onOk((data: any) => {
        resolve(data)
      }).onCancel(() => {
        resolve(null)
      }).onDismiss(() => {
        resolve(null)
      })
    })
  }
}

/**
 * Создает менеджер диалогов
 */
export function createDialogManager(): DialogManager {
  return new DialogManager()
}

/**
 * Хук для использования диалогов в Vue компонентах
 */
export function useDialogs() {
  const manager = createDialogManager()
  
  return {
    confirm: manager.confirm.bind(manager),
    prompt: manager.prompt.bind(manager),
    select: manager.select.bind(manager),
    confirmDelete: manager.confirmDelete.bind(manager),
    confirmSave: manager.confirmSave.bind(manager),
    confirmCancel: manager.confirmCancel.bind(manager),
    confirmExit: manager.confirmExit.bind(manager),
    info: manager.info.bind(manager),
    warning: manager.warning.bind(manager),
    error: manager.error.bind(manager),
    success: manager.success.bind(manager),
    loading: manager.loading.bind(manager),
    hideLoading: manager.hideLoading.bind(manager),
    custom: manager.custom.bind(manager)
  }
}

/**
 * Глобальный менеджер диалогов
 */
let globalDialogManager: DialogManager | null = null

/**
 * Получает глобальный менеджер диалогов
 */
export function getGlobalDialogManager(): DialogManager {
  if (!globalDialogManager) {
    globalDialogManager = createDialogManager()
  }
  return globalDialogManager
}

/**
 * Устанавливает глобальный менеджер диалогов
 */
export function setGlobalDialogManager(manager: DialogManager): void {
  globalDialogManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const dialog = {
  confirm: (options: ConfirmDialogOptions) => getGlobalDialogManager().confirm(options),
  prompt: (options: PromptDialogOptions) => getGlobalDialogManager().prompt(options),
  select: (options: SelectDialogOptions) => getGlobalDialogManager().select(options),
  confirmDelete: (resourceName: string, options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().confirmDelete(resourceName, options),
  confirmSave: (options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().confirmSave(options),
  confirmCancel: (options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().confirmCancel(options),
  confirmExit: (options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().confirmExit(options),
  info: (title: string, message: string, options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().info(title, message, options),
  warning: (title: string, message: string, options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().warning(title, message, options),
  error: (title: string, message: string, options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().error(title, message, options),
  success: (title: string, message: string, options?: Partial<ConfirmDialogOptions>) => getGlobalDialogManager().success(title, message, options),
  loading: (message?: string) => getGlobalDialogManager().loading(message),
  hideLoading: () => getGlobalDialogManager().hideLoading(),
  custom: (component: any, props?: Record<string, any>) => getGlobalDialogManager().custom(component, props)
}
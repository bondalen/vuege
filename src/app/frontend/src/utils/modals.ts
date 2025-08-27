// Утилиты для работы с модальными окнами



/**
 * Интерфейс для конфигурации модального окна
 */
export interface ModalConfig {
  id: string
  title?: string
  message?: string
  component?: any
  props?: Record<string, any>
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full'
  persistent?: boolean
  maximized?: boolean
  fullHeight?: boolean
  fullWidth?: boolean
  position?: 'top' | 'right' | 'bottom' | 'left' | 'standard'
  transitionShow?: string
  transitionHide?: string
  noEscDismiss?: boolean
  noBackdropDismiss?: boolean
  noRouteDismiss?: boolean
  autoClose?: boolean
  autoCloseDelay?: number
  onShow?: () => void
  onHide?: () => void
  onOk?: () => void | Promise<void>
  onCancel?: () => void
  onConfirm?: () => void | Promise<void>
  onDismiss?: () => void
  okLabel?: string
  cancelLabel?: string
  confirmLabel?: string
  dismissLabel?: string
  showOk?: boolean
  showCancel?: boolean
  showConfirm?: boolean
  showDismiss?: boolean
  okColor?: string
  cancelColor?: string
  confirmColor?: string
  dismissColor?: string
  okIcon?: string
  cancelIcon?: string
  confirmIcon?: string
  dismissIcon?: string
  loading?: boolean
  loadingText?: string
  closable?: boolean
  draggable?: boolean
  resizable?: boolean
  minWidth?: number
  maxWidth?: number
  minHeight?: number
  maxHeight?: number
  zIndex?: number
  backdrop?: boolean
  backdropColor?: string
  backdropOpacity?: number
  scrollable?: boolean
  noFocus?: boolean
  noRefocus?: boolean
  noShake?: boolean
  noClickOutside?: boolean
  noKeydown?: boolean
  noKeyup?: boolean
  noKeypress?: boolean
  noMousewheel?: boolean
  noTouchstart?: boolean
  noTouchmove?: boolean
  noTouchend?: boolean
  noPointerdown?: boolean
  noPointermove?: boolean
  noPointerup?: boolean
  noPointerenter?: boolean
  noPointerleave?: boolean
  noPointerover?: boolean
  noPointerout?: boolean
  noPointercancel?: boolean
  noGotpointercapture?: boolean
  noLostpointercapture?: boolean
  noContextmenu?: boolean
  noAuxclick?: boolean
  noCompositionstart?: boolean
  noCompositionupdate?: boolean
  noCompositionend?: boolean
  noBeforeinput?: boolean
  noInput?: boolean
  noChange?: boolean
  noSelect?: boolean
  noSelectstart?: boolean
  noSelectionchange?: boolean
  noCut?: boolean
  noCopy?: boolean
  noPaste?: boolean
  noDrag?: boolean
  noDragstart?: boolean
  noDragend?: boolean
  noDragenter?: boolean
  noDragover?: boolean
  noDragleave?: boolean
  noDrop?: boolean
  noDragexit?: boolean
}

/**
 * Интерфейс для состояния модального окна
 */
export interface ModalState {
  id: string
  visible: boolean
  loading: boolean
  data: any
  config: ModalConfig
}

/**
 * Класс для управления модальными окнами
 */
export class ModalManager {
  private modals: Map<string, ModalState>
  private zIndexCounter: number

  constructor() {
    this.modals = new Map()
    this.zIndexCounter = 1000
  }

  /**
   * Инициализирует менеджер с Quasar
   */
  init(_$q: any): void {
    // Инициализация с Quasar (пока не используется)
  }

  /**
   * Открывает модальное окно
   */
  open(config: ModalConfig): Promise<any> {
    return new Promise((resolve, _reject) => {
      const modalState: ModalState = {
        id: config.id,
        visible: true,
        loading: false,
        data: null,
        config: {
          size: 'md',
          persistent: false,
          maximized: false,
          fullHeight: false,
          fullWidth: false,
          position: 'standard',
          transitionShow: 'fade',
          transitionHide: 'fade',
          noEscDismiss: false,
          noBackdropDismiss: false,
          noRouteDismiss: false,
          autoClose: false,
          autoCloseDelay: 0,
          okLabel: 'OK',
          cancelLabel: 'Cancel',
          confirmLabel: 'Confirm',
          dismissLabel: 'Dismiss',
          showOk: false,
          showCancel: false,
          showConfirm: false,
          showDismiss: false,
          okColor: 'primary',
          cancelColor: 'grey',
          confirmColor: 'positive',
          dismissColor: 'grey',
          okIcon: 'check',
          cancelIcon: 'close',
          confirmIcon: 'check',
          dismissIcon: 'close',
          loading: false,
          loadingText: 'Loading...',
          closable: true,
          draggable: false,
          resizable: false,
          minWidth: 300,
          maxWidth: 800,
          minHeight: 200,
          maxHeight: 600,
          zIndex: this.zIndexCounter++,
          backdrop: true,
          backdropColor: 'black',
          backdropOpacity: 0.5,
          scrollable: true,
          noFocus: false,
          noRefocus: false,
          noShake: false,
          noClickOutside: false,
          ...config
        }
      }

      this.modals.set(config.id, modalState)

      // Вызываем onShow если есть
      if (config.onShow) {
        config.onShow()
      }

      // Автоматическое закрытие
      if (config.autoClose && config.autoCloseDelay) {
        setTimeout(() => {
          this.close(config.id)
        }, config.autoCloseDelay)
      }

      resolve(modalState)
    })
  }

  /**
   * Закрывает модальное окно
   */
  close(id: string, data?: any): void {
    const modal = this.modals.get(id)
    if (modal) {
      modal.visible = false
      modal.data = data

      // Вызываем onHide если есть
      if (modal.config.onHide) {
        modal.config.onHide()
      }

      // Удаляем из списка
      setTimeout(() => {
        this.modals.delete(id)
      }, 300) // Время анимации
    }
  }

  /**
   * Получает модальное окно по ID
   */
  get(id: string): ModalState | undefined {
    return this.modals.get(id)
  }

  /**
   * Проверяет, открыто ли модальное окно
   */
  isOpen(id: string): boolean {
    const modal = this.modals.get(id)
    return modal ? modal.visible : false
  }

  /**
   * Получает все открытые модальные окна
   */
  getAll(): ModalState[] {
    return Array.from(this.modals.values())
  }

  /**
   * Закрывает все модальные окна
   */
  closeAll(): void {
    this.modals.forEach((_modal, id) => {
      this.close(id)
    })
  }

  /**
   * Устанавливает данные модального окна
   */
  setData(id: string, data: any): void {
    const modal = this.modals.get(id)
    if (modal) {
      modal.data = data
    }
  }

  /**
   * Получает данные модального окна
   */
  getData(id: string): any {
    const modal = this.modals.get(id)
    return modal ? modal.data : null
  }

  /**
   * Устанавливает состояние загрузки
   */
  setLoading(id: string, loading: boolean): void {
    const modal = this.modals.get(id)
    if (modal) {
      modal.loading = loading
    }
  }

  /**
   * Обновляет конфигурацию модального окна
   */
  updateConfig(id: string, updates: Partial<ModalConfig>): void {
    const modal = this.modals.get(id)
    if (modal) {
      Object.assign(modal.config, updates)
    }
  }

  /**
   * Показывает диалог подтверждения
   */
  confirm(config: Partial<ModalConfig>): Promise<boolean> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `confirm_${Date.now()}`,
        title: 'Подтверждение',
        message: 'Вы уверены?',
        showConfirm: true,
        showCancel: true,
        persistent: true,
        ...config,
        onConfirm: async () => {
          if (config.onConfirm) {
            await config.onConfirm()
          }
          this.close(modalConfig.id, true)
          resolve(true)
        },
        onCancel: () => {
          if (config.onCancel) {
            config.onCancel()
          }
          this.close(modalConfig.id, false)
          resolve(false)
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с предупреждением
   */
  alert(config: Partial<ModalConfig>): Promise<void> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `alert_${Date.now()}`,
        title: 'Внимание',
        message: 'Сообщение',
        showOk: true,
        persistent: true,
        ...config,
        onOk: async () => {
          if (config.onOk) {
            await config.onOk()
          }
          this.close(modalConfig.id)
          resolve()
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с вводом
   */
  prompt(config: Partial<ModalConfig>): Promise<string | null> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `prompt_${Date.now()}`,
        title: 'Ввод',
        message: 'Введите значение:',
        showConfirm: true,
        showCancel: true,
        persistent: true,
        ...config,
        onConfirm: async () => {
          if (config.onConfirm) {
            await config.onConfirm()
          }
          const data = this.getData(modalConfig.id)
          this.close(modalConfig.id, data)
          resolve(data)
        },
        onCancel: () => {
          if (config.onCancel) {
            config.onCancel()
          }
          this.close(modalConfig.id, null)
          resolve(null)
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с выбором
   */
  select<T = any>(config: Partial<ModalConfig>): Promise<T | null> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `select_${Date.now()}`,
        title: 'Выбор',
        message: 'Выберите значение:',
        showConfirm: true,
        showCancel: true,
        persistent: true,
        ...config,
        onConfirm: async () => {
          if (config.onConfirm) {
            await config.onConfirm()
          }
          const data = this.getData(modalConfig.id)
          this.close(modalConfig.id, data)
          resolve(data)
        },
        onCancel: () => {
          if (config.onCancel) {
            config.onCancel()
          }
          this.close(modalConfig.id, null)
          resolve(null)
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с формой
   */
  form<T = any>(config: Partial<ModalConfig>): Promise<T | null> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `form_${Date.now()}`,
        title: 'Форма',
        showConfirm: true,
        showCancel: true,
        persistent: true,
        size: 'lg',
        ...config,
        onConfirm: async () => {
          if (config.onConfirm) {
            await config.onConfirm()
          }
          const data = this.getData(modalConfig.id)
          this.close(modalConfig.id, data)
          resolve(data)
        },
        onCancel: () => {
          if (config.onCancel) {
            config.onCancel()
          }
          this.close(modalConfig.id, null)
          resolve(null)
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с изображением
   */
  image(config: Partial<ModalConfig>): Promise<void> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `image_${Date.now()}`,
        title: 'Изображение',
        showOk: true,
        size: 'lg',
        ...config,
        onOk: async () => {
          if (config.onOk) {
            await config.onOk()
          }
          this.close(modalConfig.id)
          resolve()
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с видео
   */
  video(config: Partial<ModalConfig>): Promise<void> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `video_${Date.now()}`,
        title: 'Видео',
        showOk: true,
        size: 'lg',
        ...config,
        onOk: async () => {
          if (config.onOk) {
            await config.onOk()
          }
          this.close(modalConfig.id)
          resolve()
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с PDF
   */
  pdf(config: Partial<ModalConfig>): Promise<void> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `pdf_${Date.now()}`,
        title: 'PDF документ',
        showOk: true,
        size: 'xl',
        fullHeight: true,
        ...config,
        onOk: async () => {
          if (config.onOk) {
            await config.onOk()
          }
          this.close(modalConfig.id)
          resolve()
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Показывает диалог с картой
   */
  map(config: Partial<ModalConfig>): Promise<void> {
    return new Promise((resolve) => {
      const modalConfig: ModalConfig = {
        id: `map_${Date.now()}`,
        title: 'Карта',
        showOk: true,
        size: 'xl',
        fullHeight: true,
        ...config,
        onOk: async () => {
          if (config.onOk) {
            await config.onOk()
          }
          this.close(modalConfig.id)
          resolve()
        }
      }

      this.open(modalConfig)
    })
  }

  /**
   * Получает статистику модальных окон
   */
  getStats(): Record<string, any> {
    const totalModals = this.modals.size
    const openModals = Array.from(this.modals.values()).filter(m => m.visible).length
    const loadingModals = Array.from(this.modals.values()).filter(m => m.loading).length

    return {
      totalModals,
      openModals,
      loadingModals,
      closedModals: totalModals - openModals,
      modalIds: Array.from(this.modals.keys())
    }
  }
}

/**
 * Глобальный менеджер модальных окон
 */
let globalModalManager: ModalManager | null = null

/**
 * Получает глобальный менеджер модальных окон
 */
export function getGlobalModalManager(): ModalManager {
  if (!globalModalManager) {
    globalModalManager = new ModalManager()
  }
  return globalModalManager
}

/**
 * Устанавливает глобальный менеджер модальных окон
 */
export function setGlobalModalManager(manager: ModalManager): void {
  globalModalManager = manager
}

/**
 * Хук для использования менеджера модальных окон в Vue компонентах
 */
export function useModalManager() {
  // const $q = useQuasar() // Пока не используется
  const manager = getGlobalModalManager()
  
  // Инициализируем с Quasar (пока не используется)
  // manager.init($q)
  
  return {
    open: manager.open.bind(manager),
    close: manager.close.bind(manager),
    get: manager.get.bind(manager),
    isOpen: manager.isOpen.bind(manager),
    getAll: manager.getAll.bind(manager),
    closeAll: manager.closeAll.bind(manager),
    setData: manager.setData.bind(manager),
    getData: manager.getData.bind(manager),
    setLoading: manager.setLoading.bind(manager),
    updateConfig: manager.updateConfig.bind(manager),
    confirm: manager.confirm.bind(manager),
    alert: manager.alert.bind(manager),
    prompt: manager.prompt.bind(manager),
    select: manager.select.bind(manager),
    form: manager.form.bind(manager),
    image: manager.image.bind(manager),
    video: manager.video.bind(manager),
    pdf: manager.pdf.bind(manager),
    map: manager.map.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

/**
 * Объект со всеми функциями модальных окон для совместимости
 */
export const modalManager = {
  ModalManager,
  getGlobalModalManager,
  setGlobalModalManager,
  useModalManager
}


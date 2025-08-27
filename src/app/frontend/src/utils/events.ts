// Утилиты для работы с событиями

/**
 * Интерфейс для обработчика события
 */
export interface EventHandler {
  id: string
  handler: Function
  once: boolean
  priority: number
}

/**
 * Интерфейс для конфигурации события
 */
export interface EventConfig {
  priority?: number
  once?: boolean
  async?: boolean
  timeout?: number
}

/**
 * Класс для управления событиями
 */
export class EventManager {
  private events: Map<string, EventHandler[]>
  private globalEvents: Map<string, EventHandler[]>
  private counter: number

  constructor() {
    this.events = new Map()
    this.globalEvents = new Map()
    this.counter = 0
  }

  /**
   * Подписывается на событие
   */
  on(event: string, handler: Function, config?: EventConfig): string {
    const id = `event_${++this.counter}`
    const eventHandler: EventHandler = {
      id,
      handler,
      once: config?.once || false,
      priority: config?.priority || 0
    }

    if (!this.events.has(event)) {
      this.events.set(event, [])
    }

    this.events.get(event)!.push(eventHandler)
    
    // Сортируем по приоритету
    this.events.get(event)!.sort((a, b) => b.priority - a.priority)

    return id
  }

  /**
   * Подписывается на событие один раз
   */
  once(event: string, handler: Function, config?: EventConfig): string {
    return this.on(event, handler, { ...config, once: true })
  }

  /**
   * Отписывается от события
   */
  off(event: string, handlerOrId: Function | string): boolean {
    const handlers = this.events.get(event)
    if (!handlers) {
      return false
    }

    const index = typeof handlerOrId === 'function'
      ? handlers.findIndex(h => h.handler === handlerOrId)
      : handlers.findIndex(h => h.id === handlerOrId)

    if (index !== -1) {
      handlers.splice(index, 1)
      if (handlers.length === 0) {
        this.events.delete(event)
      }
      return true
    }

    return false
  }

  /**
   * Эмитит событие
   */
  emit(event: string, ...args: any[]): void {
    const handlers = this.events.get(event)
    if (!handlers || handlers.length === 0) {
      return
    }

    const handlersToRemove: string[] = []

    handlers.forEach(handler => {
      try {
        handler.handler(...args)
        
        if (handler.once) {
          handlersToRemove.push(handler.id)
        }
      } catch (error) {
        console.error(`Error in event handler for ${event}:`, error)
      }
    })

    // Удаляем обработчики once
    handlersToRemove.forEach(id => {
      this.off(event, id)
    })
  }

  /**
   * Эмитит событие асинхронно
   */
  async emitAsync(event: string, ...args: any[]): Promise<void> {
    const handlers = this.events.get(event)
    if (!handlers || handlers.length === 0) {
      return
    }

    const handlersToRemove: string[] = []
    const promises: Promise<void>[] = []

    handlers.forEach(handler => {
      const promise = (async () => {
        try {
          await handler.handler(...args)
          
          if (handler.once) {
            handlersToRemove.push(handler.id)
          }
        } catch (error) {
          console.error(`Error in async event handler for ${event}:`, error)
        }
      })()
      
      promises.push(promise)
    })

    await Promise.all(promises)

    // Удаляем обработчики once
    handlersToRemove.forEach(id => {
      this.off(event, id)
    })
  }

  /**
   * Эмитит событие с таймаутом
   */
  emitWithTimeout(event: string, timeout: number, ...args: any[]): Promise<void> {
    return Promise.race([
      this.emitAsync(event, ...args),
      new Promise<void>((_, reject) => {
        setTimeout(() => {
          reject(new Error(`Event ${event} timed out after ${timeout}ms`))
        }, timeout)
      })
    ])
  }

  /**
   * Подписывается на глобальное событие
   */
  onGlobal(event: string, handler: Function, config?: EventConfig): string {
    const id = `global_event_${++this.counter}`
    const eventHandler: EventHandler = {
      id,
      handler,
      once: config?.once || false,
      priority: config?.priority || 0
    }

    if (!this.globalEvents.has(event)) {
      this.globalEvents.set(event, [])
    }

    this.globalEvents.get(event)!.push(eventHandler)
    
    // Сортируем по приоритету
    this.globalEvents.get(event)!.sort((a, b) => b.priority - a.priority)

    return id
  }

  /**
   * Подписывается на глобальное событие один раз
   */
  onceGlobal(event: string, handler: Function, config?: EventConfig): string {
    return this.onGlobal(event, handler, { ...config, once: true })
  }

  /**
   * Отписывается от глобального события
   */
  offGlobal(event: string, handlerOrId: Function | string): boolean {
    const handlers = this.globalEvents.get(event)
    if (!handlers) {
      return false
    }

    const index = typeof handlerOrId === 'function'
      ? handlers.findIndex(h => h.handler === handlerOrId)
      : handlers.findIndex(h => h.id === handlerOrId)

    if (index !== -1) {
      handlers.splice(index, 1)
      if (handlers.length === 0) {
        this.globalEvents.delete(event)
      }
      return true
    }

    return false
  }

  /**
   * Эмитит глобальное событие
   */
  emitGlobal(event: string, ...args: any[]): void {
    const handlers = this.globalEvents.get(event)
    if (!handlers || handlers.length === 0) {
      return
    }

    const handlersToRemove: string[] = []

    handlers.forEach(handler => {
      try {
        handler.handler(...args)
        
        if (handler.once) {
          handlersToRemove.push(handler.id)
        }
      } catch (error) {
        console.error(`Error in global event handler for ${event}:`, error)
      }
    })

    // Удаляем обработчики once
    handlersToRemove.forEach(id => {
      this.offGlobal(event, id)
    })
  }

  /**
   * Эмитит глобальное событие асинхронно
   */
  async emitGlobalAsync(event: string, ...args: any[]): Promise<void> {
    const handlers = this.globalEvents.get(event)
    if (!handlers || handlers.length === 0) {
      return
    }

    const handlersToRemove: string[] = []
    const promises: Promise<void>[] = []

    handlers.forEach(handler => {
      const promise = (async () => {
        try {
          await handler.handler(...args)
          
          if (handler.once) {
            handlersToRemove.push(handler.id)
          }
        } catch (error) {
          console.error(`Error in async global event handler for ${event}:`, error)
        }
      })()
      
      promises.push(promise)
    })

    await Promise.all(promises)

    // Удаляем обработчики once
    handlersToRemove.forEach(id => {
      this.offGlobal(event, id)
    })
  }

  /**
   * Удаляет все обработчики события
   */
  removeAllListeners(event?: string): void {
    if (event) {
      this.events.delete(event)
      this.globalEvents.delete(event)
    } else {
      this.events.clear()
      this.globalEvents.clear()
    }
  }

  /**
   * Получает количество обработчиков события
   */
  listenerCount(event: string): number {
    const localCount = this.events.get(event)?.length || 0
    const globalCount = this.globalEvents.get(event)?.length || 0
    return localCount + globalCount
  }

  /**
   * Получает все события
   */
  eventNames(): string[] {
    const localEvents = Array.from(this.events.keys())
    const globalEvents = Array.from(this.globalEvents.keys())
    return [...new Set([...localEvents, ...globalEvents])]
  }

  /**
   * Получает обработчики события
   */
  listeners(event: string): EventHandler[] {
    const localHandlers = this.events.get(event) || []
    const globalHandlers = this.globalEvents.get(event) || []
    return [...localHandlers, ...globalHandlers]
  }

  /**
   * Создает эмиттер событий
   */
  createEmitter(): EventEmitter {
    return new EventEmitter()
  }

  /**
   * Получает статистику событий
   */
  getStats(): Record<string, any> {
    const localEvents = Array.from(this.events.keys())
    const globalEvents = Array.from(this.globalEvents.keys())
    
    const localHandlers = Array.from(this.events.values()).reduce((sum, handlers) => sum + handlers.length, 0)
    const globalHandlers = Array.from(this.globalEvents.values()).reduce((sum, handlers) => sum + handlers.length, 0)

    return {
      totalEvents: localEvents.length + globalEvents.length,
      localEvents: localEvents.length,
      globalEvents: globalEvents.length,
      totalHandlers: localHandlers + globalHandlers,
      localHandlers,
      globalHandlers,
      counter: this.counter
    }
  }
}

/**
 * Класс эмиттера событий
 */
export class EventEmitter {
  private manager: EventManager

  constructor() {
    this.manager = new EventManager()
  }

  on(event: string, handler: Function, config?: EventConfig): string {
    return this.manager.on(event, handler, config)
  }

  once(event: string, handler: Function, config?: EventConfig): string {
    return this.manager.once(event, handler, config)
  }

  off(event: string, handlerOrId: Function | string): boolean {
    return this.manager.off(event, handlerOrId)
  }

  emit(event: string, ...args: any[]): void {
    return this.manager.emit(event, ...args)
  }

  emitAsync(event: string, ...args: any[]): Promise<void> {
    return this.manager.emitAsync(event, ...args)
  }

  removeAllListeners(event?: string): void {
    return this.manager.removeAllListeners(event)
  }

  listenerCount(event: string): number {
    return this.manager.listenerCount(event)
  }

  eventNames(): string[] {
    return this.manager.eventNames()
  }

  listeners(event: string): EventHandler[] {
    return this.manager.listeners(event)
  }

  getStats(): Record<string, any> {
    return this.manager.getStats()
  }
}

/**
 * Глобальный менеджер событий
 */
let globalEventManager: EventManager | null = null

/**
 * Получает глобальный менеджер событий
 */
export function getGlobalEventManager(): EventManager {
  if (!globalEventManager) {
    globalEventManager = new EventManager()
  }
  return globalEventManager
}

/**
 * Устанавливает глобальный менеджер событий
 */
export function setGlobalEventManager(manager: EventManager): void {
  globalEventManager = manager
}

/**
 * Объект со всеми функциями для работы с событиями
 */
export const events = {
  on: (event: string, handler: Function, config?: EventConfig) => getGlobalEventManager().on(event, handler, config),
  once: (event: string, handler: Function, config?: EventConfig) => getGlobalEventManager().once(event, handler, config),
  off: (event: string, handlerOrId: Function | string) => getGlobalEventManager().off(event, handlerOrId),
  emit: (event: string, ...args: any[]) => getGlobalEventManager().emit(event, ...args),
  emitAsync: (event: string, ...args: any[]) => getGlobalEventManager().emitAsync(event, ...args),
  emitWithTimeout: (event: string, timeout: number, ...args: any[]) => getGlobalEventManager().emitWithTimeout(event, timeout, ...args),
  onGlobal: (event: string, handler: Function, config?: EventConfig) => getGlobalEventManager().onGlobal(event, handler, config),
  onceGlobal: (event: string, handler: Function, config?: EventConfig) => getGlobalEventManager().onceGlobal(event, handler, config),
  offGlobal: (event: string, handlerOrId: Function | string) => getGlobalEventManager().offGlobal(event, handlerOrId),
  emitGlobal: (event: string, ...args: any[]) => getGlobalEventManager().emitGlobal(event, ...args),
  emitGlobalAsync: (event: string, ...args: any[]) => getGlobalEventManager().emitGlobalAsync(event, ...args),
  removeAllListeners: (event?: string) => getGlobalEventManager().removeAllListeners(event),
  listenerCount: (event: string) => getGlobalEventManager().listenerCount(event),
  eventNames: () => getGlobalEventManager().eventNames(),
  listeners: (event: string) => getGlobalEventManager().listeners(event),
  createEmitter: () => getGlobalEventManager().createEmitter(),
  getStats: () => getGlobalEventManager().getStats()
}

/**
 * Алиас для useEventManager
 */
export const useEvents = useEventManager

/**
 * Хук для использования менеджера событий в Vue компонентах
 */
export function useEventManager() {
  const manager = getGlobalEventManager()
  
  return {
    on: manager.on.bind(manager),
    once: manager.once.bind(manager),
    off: manager.off.bind(manager),
    emit: manager.emit.bind(manager),
    emitAsync: manager.emitAsync.bind(manager),
    emitWithTimeout: manager.emitWithTimeout.bind(manager),
    onGlobal: manager.onGlobal.bind(manager),
    onceGlobal: manager.onceGlobal.bind(manager),
    offGlobal: manager.offGlobal.bind(manager),
    emitGlobal: manager.emitGlobal.bind(manager),
    emitGlobalAsync: manager.emitGlobalAsync.bind(manager),
    removeAllListeners: manager.removeAllListeners.bind(manager),
    listenerCount: manager.listenerCount.bind(manager),
    eventNames: manager.eventNames.bind(manager),
    listeners: manager.listeners.bind(manager),
    createEmitter: manager.createEmitter.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

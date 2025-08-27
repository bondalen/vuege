// Утилиты для управления состоянием приложения

import { ref, reactive, computed, watch, watchEffect, readonly } from 'vue'
import type { Ref, ComputedRef, WatchSource, WatchCallback } from 'vue'

/**
 * Интерфейс для состояния приложения
 */
export interface AppState {
  user: UserState
  ui: UIState
  data: DataState
  settings: SettingsState
  [key: string]: any
}

/**
 * Состояние пользователя
 */
export interface UserState {
  isAuthenticated: boolean
  user: any | null
  roles: string[]
  permissions: string[]
  preferences: Record<string, any>
}

/**
 * Состояние UI
 */
export interface UIState {
  theme: string
  language: string
  sidebar: {
    isOpen: boolean
    isCollapsed: boolean
  }
  notifications: {
    isEnabled: boolean
    position: string
  }
  loading: {
    isGlobalLoading: boolean
    loadingStates: Record<string, boolean>
  }
  modals: {
    activeModals: string[]
    modalData: Record<string, any>
  }
}

/**
 * Состояние данных
 */
export interface DataState {
  cache: Record<string, any>
  filters: Record<string, any>
  pagination: Record<string, any>
  selections: Record<string, any[]>
}

/**
 * Состояние настроек
 */
export interface SettingsState {
  general: Record<string, any>
  display: Record<string, any>
  api: Record<string, any>
  security: Record<string, any>
}

/**
 * Класс для управления состоянием приложения
 */
export class StateManager {
  private state: Ref<AppState>
  private subscribers: Map<string, Set<Function>>
  private history: AppState[]
  private maxHistorySize: number

  constructor(initialState?: Partial<AppState>) {
    this.state = ref<AppState>({
      user: {
        isAuthenticated: false,
        user: null,
        roles: [],
        permissions: [],
        preferences: {}
      },
      ui: {
        theme: 'light',
        language: 'ru',
        sidebar: {
          isOpen: true,
          isCollapsed: false
        },
        notifications: {
          isEnabled: true,
          position: 'top-right'
        },
        loading: {
          isGlobalLoading: false,
          loadingStates: {}
        },
        modals: {
          activeModals: [],
          modalData: {}
        }
      },
      data: {
        cache: {},
        filters: {},
        pagination: {},
        selections: {}
      },
      settings: {
        general: {},
        display: {},
        api: {},
        security: {}
      },
      ...initialState
    })

    this.subscribers = new Map()
    this.history = []
    this.maxHistorySize = 50
  }

  /**
   * Получает текущее состояние
   */
  getState(): AppState {
    return this.state.value
  }

  /**
   * Получает реактивное состояние
   */
  getReactiveState(): Ref<AppState> {
    return readonly(this.state)
  }

  /**
   * Устанавливает состояние
   */
  setState(newState: Partial<AppState>): void {
    this.saveToHistory()
    this.state.value = { ...this.state.value, ...newState }
    this.notifySubscribers('state', newState)
  }

  /**
   * Обновляет часть состояния
   */
  updateState(path: string, value: any): void {
    this.saveToHistory()
    const keys = path.split('.')
    let current: any = this.state.value

    for (let i = 0; i < keys.length - 1; i++) {
      if (!(keys[i] in current)) {
        current[keys[i]] = {}
      }
      current = current[keys[i]]
    }

    current[keys[keys.length - 1]] = value
    this.notifySubscribers(path, value)
  }

  /**
   * Получает значение по пути
   */
  getValue(path: string): any {
    const keys = path.split('.')
    let current: any = this.state.value

    for (const key of keys) {
      if (current && typeof current === 'object' && key in current) {
        current = current[key]
      } else {
        return undefined
      }
    }

    return current
  }

  /**
   * Создает вычисляемое свойство для части состояния
   */
  createComputed<T>(path: string): ComputedRef<T> {
    return computed(() => this.getValue(path) as T)
  }

  /**
   * Подписывается на изменения состояния
   */
  subscribe(path: string, callback: Function): () => void {
    if (!this.subscribers.has(path)) {
      this.subscribers.set(path, new Set())
    }

    this.subscribers.get(path)!.add(callback)

    return () => {
      const pathSubscribers = this.subscribers.get(path)
      if (pathSubscribers) {
        pathSubscribers.delete(callback)
        if (pathSubscribers.size === 0) {
          this.subscribers.delete(path)
        }
      }
    }
  }

  /**
   * Уведомляет подписчиков об изменениях
   */
  private notifySubscribers(path: string, value: any): void {
    const pathSubscribers = this.subscribers.get(path)
    if (pathSubscribers) {
      pathSubscribers.forEach(callback => {
        try {
          callback(value)
        } catch (error) {
          console.error('Error in state subscriber:', error)
        }
      })
    }
  }

  /**
   * Сохраняет состояние в историю
   */
  private saveToHistory(): void {
    this.history.push(JSON.parse(JSON.stringify(this.state.value)))
    
    if (this.history.length > this.maxHistorySize) {
      this.history.shift()
    }
  }

  /**
   * Отменяет последнее изменение
   */
  undo(): boolean {
    if (this.history.length > 0) {
      const previousState = this.history.pop()
      if (previousState) {
        this.state.value = previousState
        this.notifySubscribers('state', previousState)
        return true
      }
    }
    return false
  }

  /**
   * Получает историю состояний
   */
  getHistory(): AppState[] {
    return [...this.history]
  }

  /**
   * Очищает историю состояний
   */
  clearHistory(): void {
    this.history = []
  }

  /**
   * Устанавливает максимальный размер истории
   */
  setMaxHistorySize(size: number): void {
    this.maxHistorySize = size
    while (this.history.length > this.maxHistorySize) {
      this.history.shift()
    }
  }

  /**
   * Сбрасывает состояние к начальному
   */
  reset(): void {
    this.saveToHistory()
    this.state.value = {
      user: {
        isAuthenticated: false,
        user: null,
        roles: [],
        permissions: [],
        preferences: {}
      },
      ui: {
        theme: 'light',
        language: 'ru',
        sidebar: {
          isOpen: true,
          isCollapsed: false
        },
        notifications: {
          isEnabled: true,
          position: 'top-right'
        },
        loading: {
          isGlobalLoading: false,
          loadingStates: {}
        },
        modals: {
          activeModals: [],
          modalData: {}
        }
      },
      data: {
        cache: {},
        filters: {},
        pagination: {},
        selections: {}
      },
      settings: {
        general: {},
        display: {},
        api: {},
        security: {}
      }
    }
    this.notifySubscribers('state', this.state.value)
  }

  /**
   * Экспортирует состояние
   */
  export(): string {
    return JSON.stringify(this.state.value, null, 2)
  }

  /**
   * Импортирует состояние
   */
  import(stateJson: string): boolean {
    try {
      const newState = JSON.parse(stateJson)
      this.setState(newState)
      return true
    } catch (error) {
      console.error('Error importing state:', error)
      return false
    }
  }

  /**
   * Создает снапшот состояния
   */
  createSnapshot(): AppState {
    return JSON.parse(JSON.stringify(this.state.value))
  }

  /**
   * Восстанавливает состояние из снапшота
   */
  restoreFromSnapshot(snapshot: AppState): void {
    this.setState(snapshot)
  }

  /**
   * Сравнивает текущее состояние с другим
   */
  compare(otherState: AppState): Record<string, any> {
    const differences: Record<string, any> = {}
    
    const compareObjects = (obj1: any, obj2: any, path: string = ''): void => {
      const keys = new Set([...Object.keys(obj1), ...Object.keys(obj2)])
      
      for (const key of keys) {
        const currentPath = path ? `${path}.${key}` : key
        const val1 = obj1[key]
        const val2 = obj2[key]
        
        if (val1 !== val2) {
          if (typeof val1 === 'object' && typeof val2 === 'object' && val1 !== null && val2 !== null) {
            compareObjects(val1, val2, currentPath)
          } else {
            differences[currentPath] = {
              from: val1,
              to: val2
            }
          }
        }
      }
    }
    
    compareObjects(this.state.value, otherState)
    return differences
  }

  /**
   * Получает размер состояния в байтах
   */
  getSize(): number {
    return new Blob([JSON.stringify(this.state.value)]).size
  }

  /**
   * Проверяет, изменилось ли состояние
   */
  hasChanged(originalState: AppState): boolean {
    return JSON.stringify(this.state.value) !== JSON.stringify(originalState)
  }

  /**
   * Получает статистику состояния
   */
  getStats(): Record<string, any> {
    const state = this.state.value
    const stats = {
      totalKeys: 0,
      nestedLevels: 0,
      size: this.getSize(),
      historySize: this.history.length,
      subscribers: 0
    }

    const countKeys = (obj: any, level: number = 0): void => {
      stats.totalKeys += Object.keys(obj).length
      stats.nestedLevels = Math.max(stats.nestedLevels, level)
      
      for (const value of Object.values(obj)) {
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
          countKeys(value, level + 1)
        }
      }
    }

    countKeys(state)
    
    for (const subscribers of this.subscribers.values()) {
      stats.subscribers += subscribers.size
    }

    return stats
  }
}

/**
 * Глобальный менеджер состояния
 */
let globalStateManager: StateManager | null = null

/**
 * Получает глобальный менеджер состояния
 */
export function getGlobalStateManager(): StateManager {
  if (!globalStateManager) {
    globalStateManager = new StateManager()
  }
  return globalStateManager
}

/**
 * Устанавливает глобальный менеджер состояния
 */
export function setGlobalStateManager(manager: StateManager): void {
  globalStateManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const state = {
  get: () => getGlobalStateManager().getState(),
  getReactive: () => getGlobalStateManager().getReactiveState(),
  set: (newState: Partial<AppState>) => getGlobalStateManager().setState(newState),
  update: (path: string, value: any) => getGlobalStateManager().updateState(path, value),
  getValue: (path: string) => getGlobalStateManager().getValue(path),
  createComputed: <T>(path: string) => getGlobalStateManager().createComputed<T>(path),
  subscribe: (path: string, callback: Function) => getGlobalStateManager().subscribe(path, callback),
  undo: () => getGlobalStateManager().undo(),
  getHistory: () => getGlobalStateManager().getHistory(),
  clearHistory: () => getGlobalStateManager().clearHistory(),
  setMaxHistorySize: (size: number) => getGlobalStateManager().setMaxHistorySize(size),
  reset: () => getGlobalStateManager().reset(),
  export: () => getGlobalStateManager().export(),
  import: (stateJson: string) => getGlobalStateManager().import(stateJson),
  createSnapshot: () => getGlobalStateManager().createSnapshot(),
  restoreFromSnapshot: (snapshot: AppState) => getGlobalStateManager().restoreFromSnapshot(snapshot),
  compare: (otherState: AppState) => getGlobalStateManager().compare(otherState),
  getSize: () => getGlobalStateManager().getSize(),
  hasChanged: (originalState: AppState) => getGlobalStateManager().hasChanged(originalState),
  getStats: () => getGlobalStateManager().getStats()
}

/**
 * Хук для использования состояния в Vue компонентах
 */
export function useAppState() {
  const manager = getGlobalStateManager()
  
  return {
    state: manager.getReactiveState(),
    getState: manager.getState.bind(manager),
    setState: manager.setState.bind(manager),
    updateState: manager.updateState.bind(manager),
    getValue: manager.getValue.bind(manager),
    createComputed: manager.createComputed.bind(manager),
    subscribe: manager.subscribe.bind(manager),
    undo: manager.undo.bind(manager),
    getHistory: manager.getHistory.bind(manager),
    clearHistory: manager.clearHistory.bind(manager),
    setMaxHistorySize: manager.setMaxHistorySize.bind(manager),
    reset: manager.reset.bind(manager),
    export: manager.export.bind(manager),
    import: manager.import.bind(manager),
    createSnapshot: manager.createSnapshot.bind(manager),
    restoreFromSnapshot: manager.restoreFromSnapshot.bind(manager),
    compare: manager.compare.bind(manager),
    getSize: manager.getSize.bind(manager),
    hasChanged: manager.hasChanged.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

/**
 * Создает локальное состояние для компонента
 */
export function createLocalState<T>(initialValue: T) {
  const state = ref<T>(initialValue)
  
  return {
    state: readonly(state),
    setState: (value: T) => { state.value = value },
    updateState: (updater: (current: T) => T) => { state.value = updater(state.value) }
  }
}

/**
 * Создает реактивное состояние с валидацией
 */
export function createValidatedState<T>(
  initialValue: T,
  validator: (value: T) => boolean | string
) {
  const state = ref<T>(initialValue)
  const error = ref<string | null>(null)
  
  const setState = (value: T) => {
    const validation = validator(value)
    if (validation === true) {
      state.value = value
      error.value = null
    } else {
      error.value = validation as string
    }
  }
  
  return {
    state: readonly(state),
    error: readonly(error),
    setState,
    updateState: (updater: (current: T) => T) => setState(updater(state.value)),
    isValid: computed(() => error.value === null)
  }
}


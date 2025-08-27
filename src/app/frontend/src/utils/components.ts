// Утилиты для работы с компонентами

import { h, VNode, Component } from 'vue'

/**
 * Интерфейс для пропсов компонента
 */
export interface ComponentProps {
  [key: string]: any
}

/**
 * Интерфейс для событий компонента
 */
export interface ComponentEvents {
  [key: string]: (...args: any[]) => void
}

/**
 * Интерфейс для слотов компонента
 */
export interface ComponentSlots {
  [key: string]: () => VNode[]
}

/**
 * Интерфейс для конфигурации компонента
 */
export interface ComponentConfig {
  name: string
  props?: ComponentProps
  events?: ComponentEvents
  slots?: ComponentSlots
  attrs?: Record<string, any>
  class?: string | string[]
  style?: Record<string, any>
}

/**
 * Класс для управления компонентами
 */
export class ComponentManager {
  private components: Map<string, Component>
  private configs: Map<string, ComponentConfig>

  constructor() {
    this.components = new Map()
    this.configs = new Map()
  }

  /**
   * Регистрирует компонент
   */
  register(name: string, component: Component): void {
    this.components.set(name, component)
  }

  /**
   * Получает компонент по имени
   */
  get(name: string): Component | undefined {
    return this.components.get(name)
  }

  /**
   * Проверяет, зарегистрирован ли компонент
   */
  has(name: string): boolean {
    return this.components.has(name)
  }

  /**
   * Удаляет компонент
   */
  unregister(name: string): boolean {
    return this.components.delete(name)
  }

  /**
   * Получает все зарегистрированные компоненты
   */
  getAll(): Map<string, Component> {
    return new Map(this.components)
  }

  /**
   * Создает компонент с конфигурацией
   */
  create(config: ComponentConfig): VNode {
    const component = this.get(config.name)
    if (!component) {
      throw new Error(`Component "${config.name}" not found`)
    }

    return h(component, {
      ...config.props,
      ...config.attrs,
      class: config.class,
      style: config.style,
      on: config.events
    }, config.slots)
  }

  /**
   * Создает динамический компонент
   */
  createDynamic(
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    return h(component, {
      ...props,
      on: events
    }, slots)
  }

  /**
   * Создает компонент с условным рендерингом
   */
  createConditional(
    condition: boolean,
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode | null {
    if (!condition) return null
    return this.createDynamic(component, props, events, slots)
  }

  /**
   * Создает список компонентов
   */
  createList<T>(
    items: T[],
    component: Component | string,
    getProps: (item: T, index: number) => ComponentProps,
    getKey?: (item: T, index: number) => string | number
  ): VNode[] {
    return items.map((item, index) => {
      const props = getProps(item, index)
      const key = getKey ? getKey(item, index) : index
      return h(component, { ...props, key })
    })
  }

  /**
   * Создает компонент с загрузкой
   */
  createWithLoading(
    loading: boolean,
    component: Component | string,
    loadingComponent: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    if (loading) {
      return this.createDynamic(loadingComponent, props, events, slots)
    }
    return this.createDynamic(component, props, events, slots)
  }

  /**
   * Создает компонент с ошибкой
   */
  createWithError(
    error: any,
    component: Component | string,
    errorComponent: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    if (error) {
      return this.createDynamic(errorComponent, { error, ...props }, events, slots)
    }
    return this.createDynamic(component, props, events, slots)
  }

  /**
   * Создает компонент с пустым состоянием
   */
  createWithEmpty(
    isEmpty: boolean,
    component: Component | string,
    emptyComponent: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    if (isEmpty) {
      return this.createDynamic(emptyComponent, props, events, slots)
    }
    return this.createDynamic(component, props, events, slots)
  }

  /**
   * Создает компонент с пагинацией
   */
  createWithPagination<T>(
    items: T[],
    page: number,
    pageSize: number,
    component: Component | string,
    getProps: (item: T, index: number) => ComponentProps,
    paginationComponent?: Component | string
  ): VNode[] {
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const pageItems = items.slice(start, end)

    const nodes = this.createList(pageItems, component, getProps)

    if (paginationComponent) {
      nodes.push(
        h(paginationComponent, {
          currentPage: page,
          totalPages: Math.ceil(items.length / pageSize),
          totalItems: items.length,
          pageSize
        })
      )
    }

    return nodes
  }

  /**
   * Создает компонент с фильтрацией
   */
  createWithFilter<T>(
    items: T[],
    filter: (item: T) => boolean,
    component: Component | string,
    getProps: (item: T, index: number) => ComponentProps
  ): VNode[] {
    const filteredItems = items.filter(filter)
    return this.createList(filteredItems, component, getProps)
  }

  /**
   * Создает компонент с сортировкой
   */
  createWithSort<T>(
    items: T[],
    sortFn: (a: T, b: T) => number,
    component: Component | string,
    getProps: (item: T, index: number) => ComponentProps
  ): VNode[] {
    const sortedItems = [...items].sort(sortFn)
    return this.createList(sortedItems, component, getProps)
  }

  /**
   * Создает компонент с группировкой
   */
  createWithGroup<T>(
    items: T[],
    groupBy: (item: T) => string,
    component: Component | string,
    getProps: (item: T, index: number) => ComponentProps,
    groupComponent?: Component | string
  ): VNode[] {
    const groups = new Map<string, T[]>()
    
    items.forEach(item => {
      const key = groupBy(item)
      if (!groups.has(key)) {
        groups.set(key, [])
      }
      groups.get(key)!.push(item)
    })

    const nodes: VNode[] = []
    
    groups.forEach((groupItems, groupKey) => {
      if (groupComponent) {
        nodes.push(
          h(groupComponent, { title: groupKey }, () =>
            groupItems.map((item, index) =>
              h(component, { ...getProps(item, index), key: index })
            )
          )
        )
      } else {
        nodes.push(...this.createList(groupItems, component, getProps))
      }
    })

    return nodes
  }

  /**
   * Создает компонент с виртуализацией
   */
  createVirtualized<T>(
    items: T[],
    component: Component | string,
    getProps: (item: T, index: number) => ComponentProps,
    itemHeight: number,
    containerHeight: number,
    startIndex: number = 0,
    endIndex?: number
  ): VNode[] {
    const visibleEndIndex = endIndex || Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight),
      items.length
    )
    
    const visibleItems = items.slice(startIndex, visibleEndIndex)
    
    return visibleItems.map((item, index) => {
      const actualIndex = startIndex + index
      const props = getProps(item, actualIndex)
      return h(component, {
        ...props,
        key: actualIndex,
        style: {
          position: 'absolute',
          top: `${actualIndex * itemHeight}px`,
          height: `${itemHeight}px`
        }
      })
    })
  }

  /**
   * Создает компонент с анимацией
   */
  createWithAnimation(
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots,
    animation?: string
  ): VNode {
    return h('transition', {
      name: animation || 'fade',
      appear: true
    }, () => [this.createDynamic(component, props, events, slots)])
  }

  /**
   * Создает компонент с задержкой
   */
  createWithDelay(
    delay: number,
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): Promise<VNode> {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(this.createDynamic(component, props, events, slots))
      }, delay)
    })
  }

  /**
   * Создает компонент с повторением
   */
  createRepeated(
    count: number,
    component: Component | string,
    getProps: (index: number) => ComponentProps
  ): VNode[] {
    return Array.from({ length: count }, (_, index) =>
      h(component, { ...getProps(index), key: index })
    )
  }

  /**
   * Создает компонент с интервалом
   */
  createWithInterval(
    interval: number,
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    return h('div', {
      onMounted: () => {
        setInterval(() => {
          // Обновление компонента
        }, interval)
      }
    }, () => [this.createDynamic(component, props, events, slots)])
  }

  /**
   * Создает компонент с дебаунсом
   */
  createWithDebounce(
    delay: number,
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    let timeoutId: ReturnType<typeof setTimeout> | null = null

    return h('div', {
      onUpdate: () => {
        if (timeoutId) {
          clearTimeout(timeoutId)
        }
        timeoutId = setTimeout(() => {
          // Обновление компонента
        }, delay)
      }
    }, () => [this.createDynamic(component, props, events, slots)])
  }

  /**
   * Создает компонент с троттлингом
   */
  createWithThrottle(
    delay: number,
    component: Component | string,
    props?: ComponentProps,
    events?: ComponentEvents,
    slots?: ComponentSlots
  ): VNode {
    let lastCall = 0

    return h('div', {
      onUpdate: () => {
        const now = Date.now()
        if (now - lastCall >= delay) {
          lastCall = now
          // Обновление компонента
        }
      }
    }, () => [this.createDynamic(component, props, events, slots)])
  }

  /**
   * Получает статистику компонентов
   */
  getStats(): Record<string, any> {
    return {
      totalComponents: this.components.size,
      componentNames: Array.from(this.components.keys()),
      totalConfigs: this.configs.size,
      configNames: Array.from(this.configs.keys())
    }
  }
}

/**
 * Глобальный менеджер компонентов
 */
let globalComponentManager: ComponentManager | null = null

/**
 * Получает глобальный менеджер компонентов
 */
export function getGlobalComponentManager(): ComponentManager {
  if (!globalComponentManager) {
    globalComponentManager = new ComponentManager()
  }
  return globalComponentManager
}

/**
 * Устанавливает глобальный менеджер компонентов
 */
export function setGlobalComponentManager(manager: ComponentManager): void {
  globalComponentManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const componentManager = {
  register: (name: string, component: Component) => getGlobalComponentManager().register(name, component),
  get: (name: string) => getGlobalComponentManager().get(name),
  has: (name: string) => getGlobalComponentManager().has(name),
  unregister: (name: string) => getGlobalComponentManager().unregister(name),
  getAll: () => getGlobalComponentManager().getAll(),
  create: (config: ComponentConfig) => getGlobalComponentManager().create(config),
  createDynamic: (component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createDynamic(component, props, events, slots),
  createConditional: (condition: boolean, component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createConditional(condition, component, props, events, slots),
  createList: <T>(items: T[], component: Component | string, getProps: (item: T, index: number) => ComponentProps, getKey?: (item: T, index: number) => string | number) => 
    getGlobalComponentManager().createList(items, component, getProps, getKey),
  createWithLoading: (loading: boolean, component: Component | string, loadingComponent: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithLoading(loading, component, loadingComponent, props, events, slots),
  createWithError: (error: any, component: Component | string, errorComponent: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithError(error, component, errorComponent, props, events, slots),
  createWithEmpty: (isEmpty: boolean, component: Component | string, emptyComponent: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithEmpty(isEmpty, component, emptyComponent, props, events, slots),
  createWithPagination: <T>(items: T[], page: number, pageSize: number, component: Component | string, getProps: (item: T, index: number) => ComponentProps, paginationComponent?: Component | string) => 
    getGlobalComponentManager().createWithPagination(items, page, pageSize, component, getProps, paginationComponent),
  createWithFilter: <T>(items: T[], filter: (item: T) => boolean, component: Component | string, getProps: (item: T, index: number) => ComponentProps) => 
    getGlobalComponentManager().createWithFilter(items, filter, component, getProps),
  createWithSort: <T>(items: T[], sortFn: (a: T, b: T) => number, component: Component | string, getProps: (item: T, index: number) => ComponentProps) => 
    getGlobalComponentManager().createWithSort(items, sortFn, component, getProps),
  createWithGroup: <T>(items: T[], groupBy: (item: T) => string, component: Component | string, getProps: (item: T, index: number) => ComponentProps, groupComponent?: Component | string) => 
    getGlobalComponentManager().createWithGroup(items, groupBy, component, getProps, groupComponent),
  createVirtualized: <T>(items: T[], component: Component | string, getProps: (item: T, index: number) => ComponentProps, itemHeight: number, containerHeight: number, startIndex?: number, endIndex?: number) => 
    getGlobalComponentManager().createVirtualized(items, component, getProps, itemHeight, containerHeight, startIndex, endIndex),
  createWithAnimation: (component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots, animation?: string) => 
    getGlobalComponentManager().createWithAnimation(component, props, events, slots, animation),
  createWithDelay: (delay: number, component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithDelay(delay, component, props, events, slots),
  createRepeated: (count: number, component: Component | string, getProps: (index: number) => ComponentProps) => 
    getGlobalComponentManager().createRepeated(count, component, getProps),
  createWithInterval: (interval: number, component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithInterval(interval, component, props, events, slots),
  createWithDebounce: (delay: number, component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithDebounce(delay, component, props, events, slots),
  createWithThrottle: (delay: number, component: Component | string, props?: ComponentProps, events?: ComponentEvents, slots?: ComponentSlots) => 
    getGlobalComponentManager().createWithThrottle(delay, component, props, events, slots),
  getStats: () => getGlobalComponentManager().getStats()
}

/**
 * Хук для использования менеджера компонентов в Vue компонентах
 */
export function useComponentManager() {
  const manager = getGlobalComponentManager()
  
  return {
    register: manager.register.bind(manager),
    get: manager.get.bind(manager),
    has: manager.has.bind(manager),
    unregister: manager.unregister.bind(manager),
    getAll: manager.getAll.bind(manager),
    create: manager.create.bind(manager),
    createDynamic: manager.createDynamic.bind(manager),
    createConditional: manager.createConditional.bind(manager),
    createList: manager.createList.bind(manager),
    createWithLoading: manager.createWithLoading.bind(manager),
    createWithError: manager.createWithError.bind(manager),
    createWithEmpty: manager.createWithEmpty.bind(manager),
    createWithPagination: manager.createWithPagination.bind(manager),
    createWithFilter: manager.createWithFilter.bind(manager),
    createWithSort: manager.createWithSort.bind(manager),
    createWithGroup: manager.createWithGroup.bind(manager),
    createVirtualized: manager.createVirtualized.bind(manager),
    createWithAnimation: manager.createWithAnimation.bind(manager),
    createWithDelay: manager.createWithDelay.bind(manager),
    createRepeated: manager.createRepeated.bind(manager),
    createWithInterval: manager.createWithInterval.bind(manager),
    createWithDebounce: manager.createWithDebounce.bind(manager),
    createWithThrottle: manager.createWithThrottle.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

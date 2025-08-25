// Утилиты для работы с роутингом

import { useRouter, useRoute } from 'vue-router'
import type { RouteLocationRaw, NavigationGuardNext, RouteLocationNormalized } from 'vue-router'

/**
 * Интерфейс для метаданных маршрута
 */
export interface RouteMeta {
  title?: string
  description?: string
  requiresAuth?: boolean
  roles?: string[]
  permissions?: string[]
  layout?: string
  breadcrumb?: string
  icon?: string
  order?: number
  hidden?: boolean
  cache?: boolean
  [key: string]: any
}

/**
 * Интерфейс для хлебных крошек
 */
export interface Breadcrumb {
  name: string
  path: string
  icon?: string
  disabled?: boolean
}

/**
 * Класс для управления роутингом
 */
export class RouterManager {
  private router: any
  private route: any

  constructor() {
    this.router = useRouter()
    this.route = useRoute()
  }

  /**
   * Переходит к маршруту
   */
  push(to: RouteLocationRaw): Promise<void> {
    return this.router.push(to)
  }

  /**
   * Заменяет текущий маршрут
   */
  replace(to: RouteLocationRaw): Promise<void> {
    return this.router.replace(to)
  }

  /**
   * Переходит назад
   */
  back(): void {
    this.router.back()
  }

  /**
   * Переходит вперед
   */
  forward(): void {
    this.router.forward()
  }

  /**
   * Переходит к указанному шагу в истории
   */
  go(delta: number): void {
    this.router.go(delta)
  }

  /**
   * Получает текущий маршрут
   */
  getCurrentRoute(): RouteLocationNormalized {
    return this.route
  }

  /**
   * Получает текущий путь
   */
  getCurrentPath(): string {
    return this.route.path
  }

  /**
   * Получает текущее имя маршрута
   */
  getCurrentName(): string | null {
    return this.route.name as string | null
  }

  /**
   * Получает параметры маршрута
   */
  getParams(): Record<string, string> {
    return this.route.params
  }

  /**
   * Получает параметр маршрута
   */
  getParam(name: string): string | undefined {
    return this.route.params[name] as string | undefined
  }

  /**
   * Получает query параметры
   */
  getQuery(): Record<string, string> {
    return this.route.query
  }

  /**
   * Получает query параметр
   */
  getQueryParam(name: string): string | undefined {
    return this.route.query[name] as string | undefined
  }

  /**
   * Устанавливает query параметр
   */
  setQueryParam(name: string, value: string): void {
    const query = { ...this.route.query, [name]: value }
    this.router.push({ query })
  }

  /**
   * Удаляет query параметр
   */
  removeQueryParam(name: string): void {
    const query = { ...this.route.query }
    delete query[name]
    this.router.push({ query })
  }

  /**
   * Получает метаданные маршрута
   */
  getMeta(): RouteMeta {
    return this.route.meta as RouteMeta
  }

  /**
   * Получает значение метаданного
   */
  getMetaValue(key: string): any {
    return this.route.meta?.[key]
  }

  /**
   * Проверяет, является ли текущий маршрут активным
   */
  isActive(routeName: string): boolean {
    return this.route.name === routeName
  }

  /**
   * Проверяет, соответствует ли текущий маршрут паттерну
   */
  isRouteMatching(pattern: string): boolean {
    return this.route.path.startsWith(pattern)
  }

  /**
   * Получает хлебные крошки для текущего маршрута
   */
  getBreadcrumbs(): Breadcrumb[] {
    const breadcrumbs: Breadcrumb[] = []
    const matched = this.route.matched

    for (const route of matched) {
      if (route.meta?.breadcrumb) {
        breadcrumbs.push({
          name: route.meta.breadcrumb,
          path: route.path,
          icon: route.meta.icon
        })
      }
    }

    return breadcrumbs
  }

  /**
   * Получает заголовок страницы
   */
  getPageTitle(): string {
    const meta = this.getMeta()
    return meta.title || 'Vuege'
  }

  /**
   * Получает описание страницы
   */
  getPageDescription(): string {
    const meta = this.getMeta()
    return meta.description || ''
  }

  /**
   * Проверяет, требуется ли аутентификация
   */
  requiresAuthentication(): boolean {
    const meta = this.getMeta()
    return meta.requiresAuth === true
  }

  /**
   * Проверяет, есть ли у пользователя необходимые роли
   */
  hasRequiredRoles(userRoles: string[]): boolean {
    const meta = this.getMeta()
    const requiredRoles = meta.roles || []
    
    if (requiredRoles.length === 0) {
      return true
    }

    return requiredRoles.some(role => userRoles.includes(role))
  }

  /**
   * Проверяет, есть ли у пользователя необходимые разрешения
   */
  hasRequiredPermissions(userPermissions: string[]): boolean {
    const meta = this.getMeta()
    const requiredPermissions = meta.permissions || []
    
    if (requiredPermissions.length === 0) {
      return true
    }

    return requiredPermissions.every(permission => userPermissions.includes(permission))
  }

  /**
   * Получает layout для текущего маршрута
   */
  getLayout(): string {
    const meta = this.getMeta()
    return meta.layout || 'default'
  }

  /**
   * Проверяет, должен ли маршрут кэшироваться
   */
  shouldCache(): boolean {
    const meta = this.getMeta()
    return meta.cache === true
  }

  /**
   * Проверяет, скрыт ли маршрут
   */
  isHidden(): boolean {
    const meta = this.getMeta()
    return meta.hidden === true
  }

  /**
   * Получает порядок маршрута
   */
  getOrder(): number {
    const meta = this.getMeta()
    return meta.order || 0
  }

  /**
   * Создает URL для маршрута
   */
  createUrl(name: string, params?: Record<string, any>, query?: Record<string, any>): string {
    try {
      const route = this.router.resolve({ name, params, query })
      return route.href
    } catch {
      return '/'
    }
  }

  /**
   * Проверяет, существует ли маршрут
   */
  hasRoute(name: string): boolean {
    return this.router.hasRoute(name)
  }

  /**
   * Получает все маршруты
   */
  getRoutes(): any[] {
    return this.router.getRoutes()
  }

  /**
   * Получает видимые маршруты (не скрытые)
   */
  getVisibleRoutes(): any[] {
    return this.router.getRoutes().filter(route => !route.meta?.hidden)
  }

  /**
   * Сортирует маршруты по порядку
   */
  getSortedRoutes(): any[] {
    return this.getVisibleRoutes().sort((a, b) => {
      const orderA = a.meta?.order || 0
      const orderB = b.meta?.order || 0
      return orderA - orderB
    })
  }

  /**
   * Получает дочерние маршруты
   */
  getChildRoutes(parentName: string): any[] {
    const parentRoute = this.router.getRoutes().find(route => route.name === parentName)
    return parentRoute?.children || []
  }

  /**
   * Проверяет, является ли маршрут дочерним
   */
  isChildRoute(parentName: string): boolean {
    return this.route.matched.some(route => route.name === parentName)
  }

  /**
   * Получает родительский маршрут
   */
  getParentRoute(): any | null {
    const matched = this.route.matched
    return matched.length > 1 ? matched[matched.length - 2] : null
  }

  /**
   * Получает корневой маршрут
   */
  getRootRoute(): any | null {
    const matched = this.route.matched
    return matched.length > 0 ? matched[0] : null
  }

  /**
   * Проверяет, является ли маршрут корневым
   */
  isRootRoute(): boolean {
    return this.route.matched.length === 1
  }

  /**
   * Получает глубину вложенности маршрута
   */
  getRouteDepth(): number {
    return this.route.matched.length
  }

  /**
   * Проверяет, можно ли вернуться назад
   */
  canGoBack(): boolean {
    return window.history.length > 1
  }

  /**
   * Проверяет, можно ли перейти вперед
   */
  canGoForward(): boolean {
    // Это сложно определить без дополнительной логики
    return false
  }

  /**
   * Получает историю навигации
   */
  getHistory(): string[] {
    // Это требует дополнительной реализации
    return []
  }

  /**
   * Очищает историю навигации
   */
  clearHistory(): void {
    // Это требует дополнительной реализации
  }

  /**
   * Добавляет guard для навигации
   */
  addGuard(guard: (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => void): void {
    this.router.beforeEach(guard)
  }

  /**
   * Удаляет guard для навигации
   */
  removeGuard(): void {
    // Это требует дополнительной реализации
  }
}

/**
 * Создает менеджер роутинга
 */
export function createRouterManager(): RouterManager {
  return new RouterManager()
}

/**
 * Глобальный менеджер роутинга
 */
let globalRouterManager: RouterManager | null = null

/**
 * Получает глобальный менеджер роутинга
 */
export function getGlobalRouterManager(): RouterManager {
  if (!globalRouterManager) {
    globalRouterManager = createRouterManager()
  }
  return globalRouterManager
}

/**
 * Устанавливает глобальный менеджер роутинга
 */
export function setGlobalRouterManager(manager: RouterManager): void {
  globalRouterManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const router = {
  push: (to: RouteLocationRaw) => getGlobalRouterManager().push(to),
  replace: (to: RouteLocationRaw) => getGlobalRouterManager().replace(to),
  back: () => getGlobalRouterManager().back(),
  forward: () => getGlobalRouterManager().forward(),
  go: (delta: number) => getGlobalRouterManager().go(delta),
  getCurrentRoute: () => getGlobalRouterManager().getCurrentRoute(),
  getCurrentPath: () => getGlobalRouterManager().getCurrentPath(),
  getCurrentName: () => getGlobalRouterManager().getCurrentName(),
  getParams: () => getGlobalRouterManager().getParams(),
  getParam: (name: string) => getGlobalRouterManager().getParam(name),
  getQuery: () => getGlobalRouterManager().getQuery(),
  getQueryParam: (name: string) => getGlobalRouterManager().getQueryParam(name),
  setQueryParam: (name: string, value: string) => getGlobalRouterManager().setQueryParam(name, value),
  removeQueryParam: (name: string) => getGlobalRouterManager().removeQueryParam(name),
  getMeta: () => getGlobalRouterManager().getMeta(),
  getMetaValue: (key: string) => getGlobalRouterManager().getMetaValue(key),
  isActive: (routeName: string) => getGlobalRouterManager().isActive(routeName),
  isRouteMatching: (pattern: string) => getGlobalRouterManager().isRouteMatching(pattern),
  getBreadcrumbs: () => getGlobalRouterManager().getBreadcrumbs(),
  getPageTitle: () => getGlobalRouterManager().getPageTitle(),
  getPageDescription: () => getGlobalRouterManager().getPageDescription(),
  requiresAuthentication: () => getGlobalRouterManager().requiresAuthentication(),
  hasRequiredRoles: (userRoles: string[]) => getGlobalRouterManager().hasRequiredRoles(userRoles),
  hasRequiredPermissions: (userPermissions: string[]) => getGlobalRouterManager().hasRequiredPermissions(userPermissions),
  getLayout: () => getGlobalRouterManager().getLayout(),
  shouldCache: () => getGlobalRouterManager().shouldCache(),
  isHidden: () => getGlobalRouterManager().isHidden(),
  getOrder: () => getGlobalRouterManager().getOrder(),
  createUrl: (name: string, params?: Record<string, any>, query?: Record<string, any>) => getGlobalRouterManager().createUrl(name, params, query),
  hasRoute: (name: string) => getGlobalRouterManager().hasRoute(name),
  getRoutes: () => getGlobalRouterManager().getRoutes(),
  getVisibleRoutes: () => getGlobalRouterManager().getVisibleRoutes(),
  getSortedRoutes: () => getGlobalRouterManager().getSortedRoutes(),
  getChildRoutes: (parentName: string) => getGlobalRouterManager().getChildRoutes(parentName),
  isChildRoute: (parentName: string) => getGlobalRouterManager().isChildRoute(parentName),
  getParentRoute: () => getGlobalRouterManager().getParentRoute(),
  getRootRoute: () => getGlobalRouterManager().getRootRoute(),
  isRootRoute: () => getGlobalRouterManager().isRootRoute(),
  getRouteDepth: () => getGlobalRouterManager().getRouteDepth(),
  canGoBack: () => getGlobalRouterManager().canGoBack(),
  canGoForward: () => getGlobalRouterManager().canGoForward(),
  getHistory: () => getGlobalRouterManager().getHistory(),
  clearHistory: () => getGlobalRouterManager().clearHistory(),
  addGuard: (guard: (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => void) => getGlobalRouterManager().addGuard(guard),
  removeGuard: () => getGlobalRouterManager().removeGuard()
}

/**
 * Хук для использования роутинга в Vue компонентах
 */
export function useRouterUtils() {
  const manager = createRouterManager()
  
  return {
    push: manager.push.bind(manager),
    replace: manager.replace.bind(manager),
    back: manager.back.bind(manager),
    forward: manager.forward.bind(manager),
    go: manager.go.bind(manager),
    getCurrentRoute: manager.getCurrentRoute.bind(manager),
    getCurrentPath: manager.getCurrentPath.bind(manager),
    getCurrentName: manager.getCurrentName.bind(manager),
    getParams: manager.getParams.bind(manager),
    getParam: manager.getParam.bind(manager),
    getQuery: manager.getQuery.bind(manager),
    getQueryParam: manager.getQueryParam.bind(manager),
    setQueryParam: manager.setQueryParam.bind(manager),
    removeQueryParam: manager.removeQueryParam.bind(manager),
    getMeta: manager.getMeta.bind(manager),
    getMetaValue: manager.getMetaValue.bind(manager),
    isActive: manager.isActive.bind(manager),
    isRouteMatching: manager.isRouteMatching.bind(manager),
    getBreadcrumbs: manager.getBreadcrumbs.bind(manager),
    getPageTitle: manager.getPageTitle.bind(manager),
    getPageDescription: manager.getPageDescription.bind(manager),
    requiresAuthentication: manager.requiresAuthentication.bind(manager),
    hasRequiredRoles: manager.hasRequiredRoles.bind(manager),
    hasRequiredPermissions: manager.hasRequiredPermissions.bind(manager),
    getLayout: manager.getLayout.bind(manager),
    shouldCache: manager.shouldCache.bind(manager),
    isHidden: manager.isHidden.bind(manager),
    getOrder: manager.getOrder.bind(manager),
    createUrl: manager.createUrl.bind(manager),
    hasRoute: manager.hasRoute.bind(manager),
    getRoutes: manager.getRoutes.bind(manager),
    getVisibleRoutes: manager.getVisibleRoutes.bind(manager),
    getSortedRoutes: manager.getSortedRoutes.bind(manager),
    getChildRoutes: manager.getChildRoutes.bind(manager),
    isChildRoute: manager.isChildRoute.bind(manager),
    getParentRoute: manager.getParentRoute.bind(manager),
    getRootRoute: manager.getRootRoute.bind(manager),
    isRootRoute: manager.isRootRoute.bind(manager),
    getRouteDepth: manager.getRouteDepth.bind(manager),
    canGoBack: manager.canGoBack.bind(manager),
    canGoForward: manager.canGoForward.bind(manager),
    getHistory: manager.getHistory.bind(manager),
    clearHistory: manager.clearHistory.bind(manager),
    addGuard: manager.addGuard.bind(manager),
    removeGuard: manager.removeGuard.bind(manager)
  }
}
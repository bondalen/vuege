// Утилиты для работы с кэшем

/**
 * Интерфейс для элемента кэша
 */
export interface CacheItem<T = any> {
  value: T
  timestamp: number
  ttl: number
  accessCount: number
  lastAccess: number
}

/**
 * Интерфейс для конфигурации кэша
 */
export interface CacheConfig {
  maxSize: number
  defaultTtl: number
  cleanupInterval: number
  enableStats: boolean
}

/**
 * Класс для управления кэшем
 */
export class CacheManager {
  private cache: Map<string, CacheItem>
  private config: CacheConfig
  private stats: {
    hits: number
    misses: number
    sets: number
    deletes: number
    evictions: number
  }
  private cleanupTimer: number | null

  constructor(config?: Partial<CacheConfig>) {
    this.config = {
      maxSize: 1000,
      defaultTtl: 5 * 60 * 1000, // 5 минут
      cleanupInterval: 60 * 1000, // 1 минута
      enableStats: true,
      ...config
    }

    this.cache = new Map()
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      evictions: 0
    }
    this.cleanupTimer = null

    this.startCleanup()
  }

  /**
   * Устанавливает значение в кэш
   */
  set<T>(key: string, value: T, ttl?: number): void {
    const now = Date.now()
    const itemTtl = ttl || this.config.defaultTtl

    // Проверяем размер кэша
    if (this.cache.size >= this.config.maxSize) {
      this.evictOldest()
    }

    this.cache.set(key, {
      value,
      timestamp: now,
      ttl: itemTtl,
      accessCount: 0,
      lastAccess: now
    })

    if (this.config.enableStats) {
      this.stats.sets++
    }
  }

  /**
   * Получает значение из кэша
   */
  get<T>(key: string): T | null {
    const item = this.cache.get(key)
    
    if (!item) {
      if (this.config.enableStats) {
        this.stats.misses++
      }
      return null
    }

    const now = Date.now()
    
    // Проверяем TTL
    if (now - item.timestamp > item.ttl) {
      this.delete(key)
      if (this.config.enableStats) {
        this.stats.misses++
      }
      return null
    }

    // Обновляем статистику доступа
    item.accessCount++
    item.lastAccess = now

    if (this.config.enableStats) {
      this.stats.hits++
    }

    return item.value
  }

  /**
   * Проверяет, существует ли ключ в кэше
   */
  has(key: string): boolean {
    const item = this.cache.get(key)
    
    if (!item) {
      return false
    }

    const now = Date.now()
    
    // Проверяем TTL
    if (now - item.timestamp > item.ttl) {
      this.delete(key)
      return false
    }

    return true
  }

  /**
   * Удаляет элемент из кэша
   */
  delete(key: string): boolean {
    const deleted = this.cache.delete(key)
    
    if (deleted && this.config.enableStats) {
      this.stats.deletes++
    }

    return deleted
  }

  /**
   * Очищает весь кэш
   */
  clear(): void {
    this.cache.clear()
  }

  /**
   * Получает размер кэша
   */
  size(): number {
    return this.cache.size
  }

  /**
   * Получает все ключи кэша
   */
  keys(): string[] {
    return Array.from(this.cache.keys())
  }

  /**
   * Получает все значения кэша
   */
  values(): any[] {
    return Array.from(this.cache.values()).map(item => item.value)
  }

  /**
   * Получает все элементы кэша
   */
  entries(): [string, any][] {
    return Array.from(this.cache.entries()).map(([key, item]) => [key, item.value])
  }

  /**
   * Обновляет TTL элемента
   */
  touch(key: string, ttl?: number): boolean {
    const item = this.cache.get(key)
    
    if (!item) {
      return false
    }

    const now = Date.now()
    
    // Проверяем TTL
    if (now - item.timestamp > item.ttl) {
      this.delete(key)
      return false
    }

    // Обновляем TTL
    item.timestamp = now
    item.ttl = ttl || this.config.defaultTtl
    item.accessCount++
    item.lastAccess = now

    return true
  }

  /**
   * Получает статистику элемента
   */
  getItemStats(key: string): CacheItem | null {
    return this.cache.get(key) || null
  }

  /**
   * Получает статистику кэша
   */
  getStats(): Record<string, any> {
    const now = Date.now()
    const items = Array.from(this.cache.values())
    
    const expiredItems = items.filter(item => now - item.timestamp > item.ttl)
    const validItems = items.filter(item => now - item.timestamp <= item.ttl)

    const totalAccessCount = validItems.reduce((sum, item) => sum + item.accessCount, 0)
    const avgAccessCount = validItems.length > 0 ? totalAccessCount / validItems.length : 0

    return {
      size: this.cache.size,
      maxSize: this.config.maxSize,
      validItems: validItems.length,
      expiredItems: expiredItems.length,
      totalAccessCount,
      avgAccessCount,
      hits: this.stats.hits,
      misses: this.stats.misses,
      sets: this.stats.sets,
      deletes: this.stats.deletes,
      evictions: this.stats.evictions,
      hitRate: this.stats.hits + this.stats.misses > 0 
        ? this.stats.hits / (this.stats.hits + this.stats.misses) 
        : 0
    }
  }

  /**
   * Сбрасывает статистику
   */
  resetStats(): void {
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      evictions: 0
    }
  }

  /**
   * Обновляет конфигурацию
   */
  updateConfig(newConfig: Partial<CacheConfig>): void {
    this.config = { ...this.config, ...newConfig }
  }

  /**
   * Получает конфигурацию
   */
  getConfig(): CacheConfig {
    return { ...this.config }
  }

  /**
   * Экспортирует кэш
   */
  export(): Record<string, any> {
    const now = Date.now()
    const data: Record<string, any> = {}

    this.cache.forEach((item, key) => {
      // Экспортируем только валидные элементы
      if (now - item.timestamp <= item.ttl) {
        data[key] = {
          value: item.value,
          ttl: item.ttl - (now - item.timestamp), // Оставшееся время
          accessCount: item.accessCount,
          lastAccess: item.lastAccess
        }
      }
    })

    return data
  }

  /**
   * Импортирует кэш
   */
  import(data: Record<string, any>): void {
    const now = Date.now()

    Object.entries(data).forEach(([key, item]) => {
      this.cache.set(key, {
        value: item.value,
        timestamp: now,
        ttl: item.ttl,
        accessCount: item.accessCount || 0,
        lastAccess: item.lastAccess || now
      })
    })
  }

  /**
   * Приватные методы
   */
  private evictOldest(): void {
    let oldestKey: string | null = null
    let oldestTime = Date.now()

    this.cache.forEach((item, key) => {
      if (item.lastAccess < oldestTime) {
        oldestTime = item.lastAccess
        oldestKey = key
      }
    })

    if (oldestKey) {
      this.delete(oldestKey)
      if (this.config.enableStats) {
        this.stats.evictions++
      }
    }
  }

  private startCleanup(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer)
    }

    this.cleanupTimer = setInterval(() => {
      this.cleanup()
    }, this.config.cleanupInterval)
  }

  private cleanup(): void {
    const now = Date.now()
    const keysToDelete: string[] = []

    this.cache.forEach((item, key) => {
      if (now - item.timestamp > item.ttl) {
        keysToDelete.push(key)
      }
    })

    keysToDelete.forEach(key => {
      this.delete(key)
    })
  }

  /**
   * Уничтожает менеджер кэша
   */
  destroy(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer)
      this.cleanupTimer = null
    }
    this.clear()
  }
}

/**
 * Глобальный менеджер кэша
 */
let globalCacheManager: CacheManager | null = null

/**
 * Получает глобальный менеджер кэша
 */
export function getGlobalCacheManager(): CacheManager {
  if (!globalCacheManager) {
    globalCacheManager = new CacheManager()
  }
  return globalCacheManager
}

/**
 * Устанавливает глобальный менеджер кэша
 */
export function setGlobalCacheManager(manager: CacheManager): void {
  globalCacheManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const cacheManager = {
  set: <T>(key: string, value: T, ttl?: number) => getGlobalCacheManager().set(key, value, ttl),
  get: <T>(key: string) => getGlobalCacheManager().get<T>(key),
  has: (key: string) => getGlobalCacheManager().has(key),
  delete: (key: string) => getGlobalCacheManager().delete(key),
  clear: () => getGlobalCacheManager().clear(),
  size: () => getGlobalCacheManager().size(),
  keys: () => getGlobalCacheManager().keys(),
  values: () => getGlobalCacheManager().values(),
  entries: () => getGlobalCacheManager().entries(),
  touch: (key: string, ttl?: number) => getGlobalCacheManager().touch(key, ttl),
  getItemStats: (key: string) => getGlobalCacheManager().getItemStats(key),
  getStats: () => getGlobalCacheManager().getStats(),
  resetStats: () => getGlobalCacheManager().resetStats(),
  updateConfig: (newConfig: Partial<CacheConfig>) => getGlobalCacheManager().updateConfig(newConfig),
  getConfig: () => getGlobalCacheManager().getConfig(),
  export: () => getGlobalCacheManager().export(),
  import: (data: Record<string, any>) => getGlobalCacheManager().import(data),
  destroy: () => getGlobalCacheManager().destroy()
}

/**
 * Хук для использования менеджера кэша в Vue компонентах
 */
export function useCacheManager() {
  const manager = getGlobalCacheManager()
  
  return {
    set: manager.set.bind(manager),
    get: manager.get.bind(manager),
    has: manager.has.bind(manager),
    delete: manager.delete.bind(manager),
    clear: manager.clear.bind(manager),
    size: manager.size.bind(manager),
    keys: manager.keys.bind(manager),
    values: manager.values.bind(manager),
    entries: manager.entries.bind(manager),
    touch: manager.touch.bind(manager),
    getItemStats: manager.getItemStats.bind(manager),
    getStats: manager.getStats.bind(manager),
    resetStats: manager.resetStats.bind(manager),
    updateConfig: manager.updateConfig.bind(manager),
    getConfig: manager.getConfig.bind(manager),
    export: manager.export.bind(manager),
    import: manager.import.bind(manager),
    destroy: manager.destroy.bind(manager)
  }
}
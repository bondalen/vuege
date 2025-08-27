// Общие утилиты для работы с массивами и объектами

/**
 * Глубокое клонирование объекта
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item)) as unknown as T
  }
  
  if (typeof obj === 'object') {
    const cloned = {} as T
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        cloned[key] = deepClone(obj[key])
      }
    }
    return cloned
  }
  
  return obj
}

/**
 * Сравнение объектов
 */
export function deepEqual(obj1: any, obj2: any): boolean {
  if (obj1 === obj2) {
    return true
  }
  
  if (obj1 === null || obj2 === null) {
    return obj1 === obj2
  }
  
  if (typeof obj1 !== 'object' || typeof obj2 !== 'object') {
    return obj1 === obj2
  }
  
  if (obj1 instanceof Date && obj2 instanceof Date) {
    return obj1.getTime() === obj2.getTime()
  }
  
  if (Array.isArray(obj1) && Array.isArray(obj2)) {
    if (obj1.length !== obj2.length) {
      return false
    }
    for (let i = 0; i < obj1.length; i++) {
      if (!deepEqual(obj1[i], obj2[i])) {
        return false
      }
    }
    return true
  }
  
  const keys1 = Object.keys(obj1)
  const keys2 = Object.keys(obj2)
  
  if (keys1.length !== keys2.length) {
    return false
  }
  
  for (const key of keys1) {
    if (!keys2.includes(key)) {
      return false
    }
    if (!deepEqual(obj1[key], obj2[key])) {
      return false
    }
  }
  
  return true
}

/**
 * Получение значения из объекта по пути
 */
export function get(obj: any, path: string, defaultValue?: any): any {
  const keys = path.split('.')
  let result = obj
  
  for (const key of keys) {
    if (result === null || result === undefined) {
      return defaultValue
    }
    result = result[key]
  }
  
  return result !== undefined ? result : defaultValue
}

/**
 * Установка значения в объект по пути
 */
export function set(obj: any, path: string, value: any): any {
  const keys = path.split('.')
  const result = deepClone(obj)
  let current = result
  
  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i]
    if (!(key in current) || typeof current[key] !== 'object') {
      current[key] = {}
    }
    current = current[key]
  }
  
  current[keys[keys.length - 1]] = value
  return result
}

/**
 * Удаление свойства из объекта по пути
 */
export function unset(obj: any, path: string): any {
  const keys = path.split('.')
  const result = deepClone(obj)
  let current = result
  
  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i]
    if (!(key in current) || typeof current[key] !== 'object') {
      return result
    }
    current = current[key]
  }
  
  delete current[keys[keys.length - 1]]
  return result
}

/**
 * Фильтрация объекта по ключам
 */
export function pick(obj: any, keys: string[]): any {
  const result: any = {}
  for (const key of keys) {
    if (key in obj) {
      result[key] = obj[key]
    }
  }
  return result
}

/**
 * Исключение ключей из объекта
 */
export function omit(obj: any, keys: string[]): any {
  const result: any = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key) && !keys.includes(key)) {
      result[key] = obj[key]
    }
  }
  return result
}

/**
 * Слияние объектов
 */
export function merge(...objects: any[]): any {
  const result: any = {}
  
  for (const obj of objects) {
    if (obj && typeof obj === 'object') {
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
            result[key] = merge(result[key] || {}, obj[key])
          } else {
            result[key] = obj[key]
          }
        }
      }
    }
  }
  
  return result
}

/**
 * Группировка массива по ключу
 */
export function groupBy<T>(array: T[], key: string | ((item: T) => string)): Record<string, T[]> {
  const result: Record<string, T[]> = {}
  
  for (const item of array) {
    const groupKey = typeof key === 'function' ? key(item) : get(item, key)
    if (!result[groupKey]) {
      result[groupKey] = []
    }
    result[groupKey].push(item)
  }
  
  return result
}

/**
 * Сортировка массива по ключу
 */
export function sortBy<T>(array: T[], key: string | ((item: T) => any), order: 'asc' | 'desc' = 'asc'): T[] {
  const sorted = [...array]
  
  sorted.sort((a, b) => {
    const aValue = typeof key === 'function' ? key(a) : get(a, key)
    const bValue = typeof key === 'function' ? key(b) : get(b, key)
    
    if (aValue < bValue) {
      return order === 'asc' ? -1 : 1
    }
    if (aValue > bValue) {
      return order === 'asc' ? 1 : -1
    }
    return 0
  })
  
  return sorted
}

/**
 * Удаление дубликатов из массива
 */
export function unique<T>(array: T[], key?: string | ((item: T) => any)): T[] {
  if (!key) {
    return [...new Set(array)]
  }
  
  const seen = new Set()
  return array.filter(item => {
    const value = typeof key === 'function' ? key(item) : get(item, key)
    if (seen.has(value)) {
      return false
    }
    seen.add(value)
    return true
  })
}

/**
 * Разделение массива на части
 */
export function chunk<T>(array: T[], size: number): T[][] {
  const result: T[][] = []
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size))
  }
  return result
}

/**
 * Создание диапазона чисел
 */
export function range(start: number, end: number, step: number = 1): number[] {
  const result: number[] = []
  for (let i = start; i <= end; i += step) {
    result.push(i)
  }
  return result
}

/**
 * Задержка выполнения
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Генерация случайного ID
 */
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9)
}

/**
 * Генерация UUID
 */
export function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

/**
 * Проверка, является ли значение пустым
 */
export function isEmpty(value: any): boolean {
  if (value === null || value === undefined) {
    return true
  }
  
  if (typeof value === 'string') {
    return value.trim().length === 0
  }
  
  if (Array.isArray(value)) {
    return value.length === 0
  }
  
  if (typeof value === 'object') {
    return Object.keys(value).length === 0
  }
  
  return false
}

/**
 * Проверка, является ли значение числом
 */
export function isNumber(value: any): boolean {
  return typeof value === 'number' && !isNaN(value) && isFinite(value)
}

/**
 * Проверка, является ли значение строкой
 */
export function isString(value: any): boolean {
  return typeof value === 'string'
}

/**
 * Проверка, является ли значение булевым
 */
export function isBoolean(value: any): boolean {
  return typeof value === 'boolean'
}

/**
 * Проверка, является ли значение функцией
 */
export function isFunction(value: any): boolean {
  return typeof value === 'function'
}

/**
 * Проверка, является ли значение объектом
 */
export function isObject(value: any): boolean {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/**
 * Проверка, является ли значение массивом
 */
export function isArray(value: any): boolean {
  return Array.isArray(value)
}

/**
 * Преобразование значения в число
 */
export function toNumber(value: any, defaultValue: number = 0): number {
  if (isNumber(value)) {
    return value
  }
  
  const parsed = parseFloat(value)
  return isNumber(parsed) ? parsed : defaultValue
}

/**
 * Преобразование значения в строку
 */
export function toString(value: any, defaultValue: string = ''): string {
  if (value === null || value === undefined) {
    return defaultValue
  }
  
  return String(value)
}

/**
 * Преобразование значения в булево
 */
export function toBoolean(value: any, defaultValue: boolean = false): boolean {
  if (isBoolean(value)) {
    return value
  }
  
  if (isString(value)) {
    const lower = value.toLowerCase()
    return lower === 'true' || lower === '1' || lower === 'yes'
  }
  
  if (isNumber(value)) {
    return value !== 0
  }
  
  return defaultValue
}

/**
 * Хук для работы с вспомогательными функциями
 */
export function useHelpers() {
  return {
    // Объекты
    deepClone,
    deepEqual,
    get,
    set,
    merge,
    pick,
    omit,
    
    // Массивы
    chunk,
    unique,
    groupBy,
    sortBy,
    range,
    
    // Утилиты
    delay,
    generateId,
    generateUUID,
    
    // Проверки
    isEmpty,
    isNumber,
    isString,
    isBoolean,
    isFunction,
    isObject,
    isArray,
    
    // Преобразования
    toNumber,
    toString,
    toBoolean
  }
}

/**
 * Объект со всеми вспомогательными функциями для совместимости
 */
export const helpers = {
  deepClone,
  deepEqual,
  get,
  set,
  merge,
  pick,
  omit,
  groupBy,
  sortBy,
  unique,
  chunk,
  range,
  delay,
  generateId,
  generateUUID,
  isEmpty,
  isNumber,
  isString,
  isBoolean,
  isFunction,
  isObject,
  isArray,
  toNumber,
  toString,
  toBoolean
}

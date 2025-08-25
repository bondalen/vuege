// Утилиты для работы с локальным хранилищем

import { STORAGE_KEYS } from '../constants'

/**
 * Сохраняет данные в localStorage
 */
export function saveToStorage<T>(key: string, data: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(data))
  } catch (error) {
    console.error('Ошибка сохранения в localStorage:', error)
  }
}

/**
 * Загружает данные из localStorage
 */
export function loadFromStorage<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(key)
    if (item === null) {
      return defaultValue
    }
    return JSON.parse(item)
  } catch (error) {
    console.error('Ошибка загрузки из localStorage:', error)
    return defaultValue
  }
}

/**
 * Удаляет данные из localStorage
 */
export function removeFromStorage(key: string): void {
  try {
    localStorage.removeItem(key)
  } catch (error) {
    console.error('Ошибка удаления из localStorage:', error)
  }
}

/**
 * Очищает все данные из localStorage
 */
export function clearStorage(): void {
  try {
    localStorage.clear()
  } catch (error) {
    console.error('Ошибка очистки localStorage:', error)
  }
}

/**
 * Проверяет, существует ли ключ в localStorage
 */
export function hasStorageKey(key: string): boolean {
  try {
    return localStorage.getItem(key) !== null
  } catch (error) {
    console.error('Ошибка проверки ключа в localStorage:', error)
    return false
  }
}

/**
 * Получает размер localStorage
 */
export function getStorageSize(): number {
  try {
    let size = 0
    for (let key in localStorage) {
      if (localStorage.hasOwnProperty(key)) {
        size += localStorage[key].length + key.length
      }
    }
    return size
  } catch (error) {
    console.error('Ошибка получения размера localStorage:', error)
    return 0
  }
}

/**
 * Сохраняет настройки приложения
 */
export function saveSettings(settings: any): void {
  saveToStorage(STORAGE_KEYS.SETTINGS, settings)
}

/**
 * Загружает настройки приложения
 */
export function loadSettings(defaultSettings: any): any {
  return loadFromStorage(STORAGE_KEYS.SETTINGS, defaultSettings)
}

/**
 * Сохраняет токен авторизации
 */
export function saveAuthToken(token: string): void {
  saveToStorage(STORAGE_KEYS.AUTH_TOKEN, token)
}

/**
 * Загружает токен авторизации
 */
export function loadAuthToken(): string | null {
  return loadFromStorage<string | null>(STORAGE_KEYS.AUTH_TOKEN, null)
}

/**
 * Удаляет токен авторизации
 */
export function removeAuthToken(): void {
  removeFromStorage(STORAGE_KEYS.AUTH_TOKEN)
}

/**
 * Сохраняет пользовательские предпочтения
 */
export function saveUserPreferences(preferences: any): void {
  saveToStorage(STORAGE_KEYS.USER_PREFERENCES, preferences)
}

/**
 * Загружает пользовательские предпочтения
 */
export function loadUserPreferences(defaultPreferences: any): any {
  return loadFromStorage(STORAGE_KEYS.USER_PREFERENCES, defaultPreferences)
}

/**
 * Сохраняет данные в sessionStorage
 */
export function saveToSessionStorage<T>(key: string, data: T): void {
  try {
    sessionStorage.setItem(key, JSON.stringify(data))
  } catch (error) {
    console.error('Ошибка сохранения в sessionStorage:', error)
  }
}

/**
 * Загружает данные из sessionStorage
 */
export function loadFromSessionStorage<T>(key: string, defaultValue: T): T {
  try {
    const item = sessionStorage.getItem(key)
    if (item === null) {
      return defaultValue
    }
    return JSON.parse(item)
  } catch (error) {
    console.error('Ошибка загрузки из sessionStorage:', error)
    return defaultValue
  }
}

/**
 * Удаляет данные из sessionStorage
 */
export function removeFromSessionStorage(key: string): void {
  try {
    sessionStorage.removeItem(key)
  } catch (error) {
    console.error('Ошибка удаления из sessionStorage:', error)
  }
}

/**
 * Очищает все данные из sessionStorage
 */
export function clearSessionStorage(): void {
  try {
    sessionStorage.clear()
  } catch (error) {
    console.error('Ошибка очистки sessionStorage:', error)
  }
}

/**
 * Проверяет, поддерживается ли localStorage
 */
export function isLocalStorageSupported(): boolean {
  try {
    const test = '__localStorage_test__'
    localStorage.setItem(test, test)
    localStorage.removeItem(test)
    return true
  } catch {
    return false
  }
}

/**
 * Проверяет, поддерживается ли sessionStorage
 */
export function isSessionStorageSupported(): boolean {
  try {
    const test = '__sessionStorage_test__'
    sessionStorage.setItem(test, test)
    sessionStorage.removeItem(test)
    return true
  } catch {
    return false
  }
}
// Утилиты для работы с сетью

/**
 * Проверяет подключение к интернету
 */
export function isOnline(): boolean {
  return navigator.onLine
}

/**
 * Проверяет качество соединения
 */
export function getConnectionInfo(): {
  effectiveType: string
  downlink: number
  rtt: number
  saveData: boolean
} | null {
  if ('connection' in navigator) {
    const connection = (navigator as any).connection
    return {
      effectiveType: connection.effectiveType || 'unknown',
      downlink: connection.downlink || 0,
      rtt: connection.rtt || 0,
      saveData: connection.saveData || false
    }
  }
  return null
}

/**
 * Проверяет доступность URL
 */
export async function checkUrlAvailability(url: string, timeout: number = 5000): Promise<boolean> {
  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)
    
    const response = await fetch(url, {
      method: 'HEAD',
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    return response.ok
  } catch {
    return false
  }
}

/**
 * Выполняет ping до сервера
 */
export async function ping(url: string, timeout: number = 5000): Promise<number> {
  const startTime = performance.now()
  
  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)
    
    await fetch(url, {
      method: 'HEAD',
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    return Math.round(performance.now() - startTime)
  } catch {
    return -1
  }
}

/**
 * Загружает изображение
 */
export function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error(`Ошибка загрузки изображения: ${src}`))
    
    img.src = src
  })
}

/**
 * Загружает скрипт
 */
export function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    
    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Ошибка загрузки скрипта: ${src}`))
    
    script.src = src
    document.head.appendChild(script)
  })
}

/**
 * Загружает CSS
 */
export function loadCSS(href: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const link = document.createElement('link')
    
    link.onload = () => resolve()
    link.onerror = () => reject(new Error(`Ошибка загрузки CSS: ${href}`))
    
    link.rel = 'stylesheet'
    link.href = href
    document.head.appendChild(link)
  })
}

/**
 * Получает IP адрес пользователя
 */
export async function getClientIP(): Promise<string> {
  try {
    const response = await fetch('https://api.ipify.org?format=json')
    const data = await response.json()
    return data.ip
  } catch {
    return 'unknown'
  }
}

/**
 * Получает информацию о местоположении по IP
 */
export async function getLocationByIP(): Promise<{
  country: string
  region: string
  city: string
  lat: number
  lon: number
} | null> {
  try {
    const ip = await getClientIP()
    const response = await fetch(`http://ip-api.com/json/${ip}`)
    const data = await response.json()
    
    if (data.status === 'success') {
      return {
        country: data.country,
        region: data.regionName,
        city: data.city,
        lat: data.lat,
        lon: data.lon
      }
    }
    
    return null
  } catch {
    return null
  }
}

/**
 * Получает информацию о погоде
 */
export async function getWeather(lat: number, lon: number, apiKey: string): Promise<any> {
  try {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric&lang=ru`
    )
    return await response.json()
  } catch {
    return null
  }
}

/**
 * Создает WebSocket соединение
 */
export function createWebSocket(url: string, protocols?: string | string[]): WebSocket {
  return new WebSocket(url, protocols)
}

/**
 * Создает EventSource соединение
 */
export function createEventSource(url: string): EventSource {
  return new EventSource(url)
}

/**
 * Выполняет запрос с retry
 */
export async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  maxRetries: number = 3,
  delay: number = 1000
): Promise<Response> {
  let lastError: Error
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fetch(url, options)
    } catch (error) {
      lastError = error as Error
      
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)))
      }
    }
  }
  
  throw lastError!
}

/**
 * Выполняет запрос с таймаутом
 */
export async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeout: number = 5000
): Promise<Response> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    return response
  } catch (error) {
    clearTimeout(timeoutId)
    throw error
  }
}

/**
 * Создает URL с параметрами
 */
export function createUrl(baseUrl: string, params: Record<string, any>): string {
  const url = new URL(baseUrl)
  
  Object.keys(params).forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      url.searchParams.append(key, params[key].toString())
    }
  })
  
  return url.toString()
}

/**
 * Парсит URL параметры
 */
export function parseUrlParams(url: string): Record<string, string> {
  const urlObj = new URL(url)
  const params: Record<string, string> = {}
  
  urlObj.searchParams.forEach((value, key) => {
    params[key] = value
  })
  
  return params
}

/**
 * Кодирует URL параметры
 */
export function encodeUrlParams(params: Record<string, any>): string {
  return Object.keys(params)
    .filter(key => params[key] !== undefined && params[key] !== null)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&')
}

/**
 * Декодирует URL параметры
 */
export function decodeUrlParams(queryString: string): Record<string, string> {
  const params: Record<string, string> = {}
  
  if (!queryString) return params
  
  const pairs = queryString.substring(1).split('&')
  
  for (const pair of pairs) {
    const [key, value] = pair.split('=')
    if (key) {
      params[decodeURIComponent(key)] = decodeURIComponent(value || '')
    }
  }
  
  return params
}

/**
 * Проверяет, является ли URL валидным
 */
export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Получает домен из URL
 */
export function getDomain(url: string): string {
  try {
    return new URL(url).hostname
  } catch {
    return ''
  }
}

/**
 * Получает протокол из URL
 */
export function getProtocol(url: string): string {
  try {
    return new URL(url).protocol
  } catch {
    return ''
  }
}

/**
 * Получает путь из URL
 */
export function getPath(url: string): string {
  try {
    return new URL(url).pathname
  } catch {
    return ''
  }
}

/**
 * Создает абсолютный URL из относительного
 */
export function makeAbsoluteUrl(relativeUrl: string, baseUrl: string): string {
  try {
    return new URL(relativeUrl, baseUrl).toString()
  } catch {
    return relativeUrl
  }
}

/**
 * Создает относительный URL
 */
export function makeRelativeUrl(absoluteUrl: string, baseUrl: string): string {
  try {
    const url = new URL(absoluteUrl)
    const base = new URL(baseUrl)
    
    if (url.origin === base.origin) {
      return url.pathname + url.search + url.hash
    }
    
    return absoluteUrl
  } catch {
    return absoluteUrl
  }
}
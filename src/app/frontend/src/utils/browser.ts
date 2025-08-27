// Утилиты для работы с браузером

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

/**
 * Проверяет, поддерживается ли IndexedDB
 */
export function isIndexedDBSupported(): boolean {
  return 'indexedDB' in window
}

/**
 * Проверяет, поддерживается ли Web Workers
 */
export function isWebWorkerSupported(): boolean {
  return typeof Worker !== 'undefined'
}

/**
 * Проверяет, поддерживается ли Service Workers
 */
export function isServiceWorkerSupported(): boolean {
  return 'serviceWorker' in navigator
}

/**
 * Проверяет, поддерживается ли Push API
 */
export function isPushAPISupported(): boolean {
  return 'PushManager' in window
}

/**
 * Проверяет, поддерживается ли Notifications API
 */
export function isNotificationsSupported(): boolean {
  return 'Notification' in window
}

/**
 * Проверяет, поддерживается ли Geolocation API
 */
export function isGeolocationSupported(): boolean {
  return 'geolocation' in navigator
}

/**
 * Проверяет, поддерживается ли Camera API
 */
export function isCameraSupported(): boolean {
  return 'mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices
}

/**
 * Проверяет, поддерживается ли File API
 */
export function isFileAPISupported(): boolean {
  return 'File' in window && 'FileReader' in window && 'FileList' in window
}

/**
 * Проверяет, поддерживается ли Drag and Drop API
 */
export function isDragAndDropSupported(): boolean {
  return 'draggable' in document.createElement('div')
}

/**
 * Получает информацию о браузере
 */
export function getBrowserInfo(): {
  name: string
  version: string
  userAgent: string
  platform: string
  language: string
  cookieEnabled: boolean
  online: boolean
} {
  const userAgent = navigator.userAgent
  let name = 'Unknown'
  let version = 'Unknown'
  
  // Определение браузера
  if (userAgent.includes('Chrome')) {
    name = 'Chrome'
    const match = userAgent.match(/Chrome\/(\d+)/)
    if (match) version = match[1]
  } else if (userAgent.includes('Firefox')) {
    name = 'Firefox'
    const match = userAgent.match(/Firefox\/(\d+)/)
    if (match) version = match[1]
  } else if (userAgent.includes('Safari')) {
    name = 'Safari'
    const match = userAgent.match(/Version\/(\d+)/)
    if (match) version = match[1]
  } else if (userAgent.includes('Edge')) {
    name = 'Edge'
    const match = userAgent.match(/Edge\/(\d+)/)
    if (match) version = match[1]
  } else if (userAgent.includes('MSIE') || userAgent.includes('Trident')) {
    name = 'Internet Explorer'
    const match = userAgent.match(/MSIE (\d+)/)
    if (match) version = match[1]
  }
  
  return {
    name,
    version,
    userAgent,
    platform: navigator.platform,
    language: navigator.language,
    cookieEnabled: navigator.cookieEnabled,
    online: navigator.onLine
  }
}

/**
 * Получает размеры экрана
 */
export function getScreenSize(): { width: number; height: number } {
  return {
    width: screen.width,
    height: screen.height
  }
}

/**
 * Получает размеры окна браузера
 */
export function getWindowSize(): { width: number; height: number } {
  return {
    width: window.innerWidth,
    height: window.innerHeight
  }
}

/**
 * Получает размеры viewport
 */
export function getViewportSize(): { width: number; height: number } {
  return {
    width: document.documentElement.clientWidth,
    height: document.documentElement.clientHeight
  }
}

/**
 * Проверяет, является ли устройство мобильным
 */
export function isMobile(): boolean {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

/**
 * Проверяет, является ли устройство планшетом
 */
export function isTablet(): boolean {
  return /iPad|Android(?=.*\bMobile\b)(?=.*\bSafari\b)/i.test(navigator.userAgent)
}

/**
 * Проверяет, является ли устройство десктопом
 */
export function isDesktop(): boolean {
  return !isMobile() && !isTablet()
}

/**
 * Проверяет, поддерживается ли touch
 */
export function isTouchSupported(): boolean {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

/**
 * Проверяет, поддерживается ли pointer
 */
export function isPointerSupported(): boolean {
  return 'onpointerdown' in window
}

/**
 * Получает текущий URL
 */
export function getCurrentUrl(): string {
  return window.location.href
}

/**
 * Получает базовый URL
 */
export function getBaseUrl(): string {
  return window.location.origin
}

/**
 * Получает путь URL
 */
export function getPathname(): string {
  return window.location.pathname
}

/**
 * Получает параметры URL
 */
export function getUrlParams(): URLSearchParams {
  return new URLSearchParams(window.location.search)
}

/**
 * Получает значение параметра URL
 */
export function getUrlParam(name: string): string | null {
  return getUrlParams().get(name)
}

/**
 * Устанавливает параметр URL
 */
export function setUrlParam(name: string, value: string): void {
  const params = getUrlParams()
  params.set(name, value)
  const newUrl = `${window.location.pathname}?${params.toString()}`
  window.history.pushState({}, '', newUrl)
}

/**
 * Удаляет параметр URL
 */
export function removeUrlParam(name: string): void {
  const params = getUrlParams()
  params.delete(name)
  const newUrl = params.toString() ? `${window.location.pathname}?${params.toString()}` : window.location.pathname
  window.history.pushState({}, '', newUrl)
}

/**
 * Копирует текст в буфер обмена
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text)
      return true
    } else {
      // Fallback для старых браузеров
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      const result = document.execCommand('copy')
      document.body.removeChild(textArea)
      return result
    }
  } catch {
    return false
  }
}

/**
 * Читает текст из буфера обмена
 */
export async function readFromClipboard(): Promise<string> {
  try {
    if (navigator.clipboard) {
      return await navigator.clipboard.readText()
    } else {
      throw new Error('Clipboard API не поддерживается')
    }
  } catch {
    return ''
  }
}

/**
 * Открывает URL в новой вкладке
 */
export function openInNewTab(url: string): void {
  window.open(url, '_blank', 'noopener,noreferrer')
}

/**
 * Открывает URL в том же окне
 */
export function openInSameWindow(url: string): void {
  window.location.href = url
}

/**
 * Обновляет страницу
 */
export function reloadPage(): void {
  window.location.reload()
}

/**
 * Переходит назад в истории
 */
export function goBack(): void {
  window.history.back()
}

/**
 * Переходит вперед в истории
 */
export function goForward(): void {
  window.history.forward()
}

/**
 * Показывает диалог подтверждения
 */
export function showConfirmDialog(message: string): Promise<boolean> {
  return Promise.resolve(confirm(message))
}

/**
 * Показывает диалог ввода
 */
export function showPromptDialog(message: string, defaultValue?: string): Promise<string | null> {
  return Promise.resolve(prompt(message, defaultValue))
}

/**
 * Показывает диалог выбора файла
 */
export function showFileDialog(accept?: string, multiple?: boolean): Promise<FileList | null> {
  return new Promise((resolve) => {
    const input = document.createElement('input')
    input.type = 'file'
    if (accept) input.accept = accept
    if (multiple) input.multiple = multiple
    
    input.onchange = () => {
      resolve(input.files)
    }
    
    input.click()
  })
}

/**
 * Показывает диалог выбора директории
 */
export function showDirectoryDialog(): Promise<FileList | null> {
  return new Promise((resolve) => {
    const input = document.createElement('input')
    input.type = 'file'
    input.webkitdirectory = true
    
    input.onchange = () => {
      resolve(input.files)
    }
    
    input.click()
  })
}

/**
 * Хук для работы с браузером
 */
export function useBrowser() {
  return {
    // Проверки поддержки
    isLocalStorageSupported,
    isSessionStorageSupported,
    isIndexedDBSupported,
    isWebWorkerSupported,
    isServiceWorkerSupported,
    isPushAPISupported,
    isNotificationsSupported,
    isGeolocationSupported,
    isCameraSupported,
    isFileAPISupported,
    isDragAndDropSupported,
    
    // Информация о браузере
    getBrowserInfo,
    getScreenSize,
    getWindowSize,
    
    // Буфер обмена
    copyToClipboard,
    readFromClipboard,
    
    // Навигация
    openInNewTab,
    openInSameWindow,
    reloadPage,
    goBack,
    goForward,
    
    // Диалоги
    showConfirmDialog,
    showPromptDialog,
    showFileDialog,
    showDirectoryDialog
  }
}

/**
 * Объект со всеми функциями для работы с браузером
 */
export const browser = {
  // Проверки поддержки
  isLocalStorageSupported,
  isSessionStorageSupported,
  isIndexedDBSupported,
  isWebWorkerSupported,
  isServiceWorkerSupported,
  isPushAPISupported,
  isNotificationsSupported,
  isGeolocationSupported,
  isCameraSupported,
  isFileAPISupported,
  isDragAndDropSupported,
  
  // Информация о браузере
  getBrowserInfo,
  getScreenSize,
  getWindowSize,
  
  // Буфер обмена
  copyToClipboard,
  readFromClipboard,
  
  // Навигация
  openInNewTab,
  openInSameWindow,
  reloadPage,
  goBack,
  goForward,
  
  // Диалоги
  showConfirmDialog,
  showPromptDialog,
  showFileDialog,
  showDirectoryDialog
}
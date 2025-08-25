// Утилиты для работы с файлами

/**
 * Получает расширение файла
 */
export function getFileExtension(filename: string): string {
  const parts = filename.split('.')
  return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : ''
}

/**
 * Получает имя файла без расширения
 */
export function getFileNameWithoutExtension(filename: string): string {
  const lastDotIndex = filename.lastIndexOf('.')
  return lastDotIndex > 0 ? filename.substring(0, lastDotIndex) : filename
}

/**
 * Получает размер файла в читаемом формате
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Б'
  
  const k = 1024
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Проверяет, является ли файл изображением
 */
export function isImageFile(filename: string): boolean {
  const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
  const extension = getFileExtension(filename)
  return imageExtensions.includes(extension)
}

/**
 * Проверяет, является ли файл документом
 */
export function isDocumentFile(filename: string): boolean {
  const documentExtensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
  const extension = getFileExtension(filename)
  return documentExtensions.includes(extension)
}

/**
 * Проверяет, является ли файл таблицей
 */
export function isSpreadsheetFile(filename: string): boolean {
  const spreadsheetExtensions = ['xls', 'xlsx', 'csv', 'ods']
  const extension = getFileExtension(filename)
  return spreadsheetExtensions.includes(extension)
}

/**
 * Проверяет, является ли файл презентацией
 */
export function isPresentationFile(filename: string): boolean {
  const presentationExtensions = ['ppt', 'pptx', 'odp']
  const extension = getFileExtension(filename)
  return presentationExtensions.includes(extension)
}

/**
 * Проверяет, является ли файл архивом
 */
export function isArchiveFile(filename: string): boolean {
  const archiveExtensions = ['zip', 'rar', '7z', 'tar', 'gz', 'bz2']
  const extension = getFileExtension(filename)
  return archiveExtensions.includes(extension)
}

/**
 * Проверяет, является ли файл видео
 */
export function isVideoFile(filename: string): boolean {
  const videoExtensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv']
  const extension = getFileExtension(filename)
  return videoExtensions.includes(extension)
}

/**
 * Проверяет, является ли файл аудио
 */
export function isAudioFile(filename: string): boolean {
  const audioExtensions = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma']
  const extension = getFileExtension(filename)
  return audioExtensions.includes(extension)
}

/**
 * Получает MIME тип файла
 */
export function getMimeType(filename: string): string {
  const extension = getFileExtension(filename)
  
  const mimeTypes: Record<string, string> = {
    // Изображения
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'webp': 'image/webp',
    'svg': 'image/svg+xml',
    
    // Документы
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'rtf': 'application/rtf',
    'odt': 'application/vnd.oasis.opendocument.text',
    
    // Таблицы
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv': 'text/csv',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    
    // Презентации
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'odp': 'application/vnd.oasis.opendocument.presentation',
    
    // Архивы
    'zip': 'application/zip',
    'rar': 'application/vnd.rar',
    '7z': 'application/x-7z-compressed',
    'tar': 'application/x-tar',
    'gz': 'application/gzip',
    'bz2': 'application/x-bzip2',
    
    // Видео
    'mp4': 'video/mp4',
    'avi': 'video/x-msvideo',
    'mov': 'video/quicktime',
    'wmv': 'video/x-ms-wmv',
    'flv': 'video/x-flv',
    'webm': 'video/webm',
    'mkv': 'video/x-matroska',
    
    // Аудио
    'mp3': 'audio/mpeg',
    'wav': 'audio/wav',
    'flac': 'audio/flac',
    'aac': 'audio/aac',
    'ogg': 'audio/ogg',
    'wma': 'audio/x-ms-wma'
  }
  
  return mimeTypes[extension] || 'application/octet-stream'
}

/**
 * Создает URL для файла
 */
export function createFileUrl(file: File): string {
  return URL.createObjectURL(file)
}

/**
 * Освобождает URL файла
 */
export function revokeFileUrl(url: string): void {
  URL.revokeObjectURL(url)
}

/**
 * Читает файл как текст
 */
export function readFileAsText(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    
    reader.onload = () => {
      resolve(reader.result as string)
    }
    
    reader.onerror = () => {
      reject(new Error('Ошибка чтения файла'))
    }
    
    reader.readAsText(file)
  })
}

/**
 * Читает файл как Data URL
 */
export function readFileAsDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    
    reader.onload = () => {
      resolve(reader.result as string)
    }
    
    reader.onerror = () => {
      reject(new Error('Ошибка чтения файла'))
    }
    
    reader.readAsDataURL(file)
  })
}

/**
 * Читает файл как ArrayBuffer
 */
export function readFileAsArrayBuffer(file: File): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    
    reader.onload = () => {
      resolve(reader.result as ArrayBuffer)
    }
    
    reader.onerror = () => {
      reject(new Error('Ошибка чтения файла'))
    }
    
    reader.readAsArrayBuffer(file)
  })
}

/**
 * Скачивает файл
 */
export function downloadFile(url: string, filename?: string): void {
  const link = document.createElement('a')
  link.href = url
  link.download = filename || 'download'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Скачивает файл из Blob
 */
export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  downloadFile(url, filename)
  URL.revokeObjectURL(url)
}

/**
 * Создает файл из строки
 */
export function createFileFromString(content: string, filename: string, mimeType: string = 'text/plain'): File {
  const blob = new Blob([content], { type: mimeType })
  return new File([blob], filename, { type: mimeType })
}

/**
 * Проверяет размер файла
 */
export function validateFileSize(file: File, maxSize: number): boolean {
  return file.size <= maxSize
}

/**
 * Проверяет тип файла
 */
export function validateFileType(file: File, allowedTypes: string[]): boolean {
  const extension = getFileExtension(file.name)
  return allowedTypes.includes(extension)
}

/**
 * Получает иконку для типа файла
 */
export function getFileIcon(filename: string): string {
  if (isImageFile(filename)) return 'image'
  if (isDocumentFile(filename)) return 'description'
  if (isSpreadsheetFile(filename)) return 'table_chart'
  if (isPresentationFile(filename)) return 'slideshow'
  if (isArchiveFile(filename)) return 'folder_zip'
  if (isVideoFile(filename)) return 'video_file'
  if (isAudioFile(filename)) return 'audio_file'
  return 'insert_drive_file'
}

/**
 * Форматирует имя файла для отображения
 */
export function formatFileName(filename: string, maxLength: number = 30): string {
  if (filename.length <= maxLength) {
    return filename
  }
  
  const extension = getFileExtension(filename)
  const nameWithoutExt = getFileNameWithoutExtension(filename)
  const maxNameLength = maxLength - extension.length - 4 // 4 для "..." и "."
  
  if (nameWithoutExt.length <= maxNameLength) {
    return filename
  }
  
  const truncatedName = nameWithoutExt.substring(0, maxNameLength)
  return `${truncatedName}...${extension ? '.' + extension : ''}`
}
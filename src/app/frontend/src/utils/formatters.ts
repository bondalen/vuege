// Утилиты для форматирования данных

import { DATE_FORMATS } from '../constants'

/**
 * Форматирует дату для отображения
 */
export function formatDate(date: string | Date | null | undefined, format: string = DATE_FORMATS.DISPLAY): string {
  if (!date) return '-'
  
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  if (isNaN(dateObj.getTime())) return '-'
  
  const day = dateObj.getDate().toString().padStart(2, '0')
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0')
  const year = dateObj.getFullYear()
  
  switch (format) {
    case DATE_FORMATS.DISPLAY:
      return `${day}.${month}.${year}`
    case DATE_FORMATS.API:
      return `${year}-${month}-${day}`
    case DATE_FORMATS.DATETIME:
      const hours = dateObj.getHours().toString().padStart(2, '0')
      const minutes = dateObj.getMinutes().toString().padStart(2, '0')
      return `${day}.${month}.${year} ${hours}:${minutes}`
    default:
      return `${day}.${month}.${year}`
  }
}

/**
 * Форматирует год из даты
 */
export function formatYear(date: string | Date | null | undefined): string {
  if (!date) return '?'
  
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  if (isNaN(dateObj.getTime())) return '?'
  
  return dateObj.getFullYear().toString()
}

/**
 * Форматирует координаты
 */
export function formatCoordinates(latitude: number | null | undefined, longitude: number | null | undefined): string {
  if (latitude === null || latitude === undefined || longitude === null || longitude === undefined) {
    return '-'
  }
  
  return `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`
}

/**
 * Форматирует полное имя
 */
export function formatFullName(firstName: string, lastName: string, middleName?: string): string {
  const parts = [firstName, lastName]
  if (middleName) {
    parts.splice(1, 0, middleName)
  }
  return parts.join(' ')
}

/**
 * Форматирует название с типом
 */
export function formatNameWithType(name: string, type: string): string {
  return `${name} (${type})`
}

/**
 * Обрезает текст до указанной длины
 */
export function truncateText(text: string, maxLength: number = 100): string {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

/**
 * Форматирует размер файла
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Б'
  
  const k = 1024
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Форматирует номер телефона
 */
export function formatPhoneNumber(phone: string): string {
  if (!phone) return '-'
  
  // Убираем все нецифровые символы
  const digits = phone.replace(/\D/g, '')
  
  if (digits.length === 11) {
    return `+${digits[0]} (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7, 9)}-${digits.slice(9)}`
  }
  
  if (digits.length === 10) {
    return `+7 (${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 8)}-${digits.slice(8)}`
  }
  
  return phone
}

/**
 * Форматирует ИНН
 */
export function formatInn(inn: string): string {
  if (!inn) return '-'
  
  const digits = inn.replace(/\D/g, '')
  
  if (digits.length === 10) {
    return `${digits.slice(0, 2)}-${digits.slice(2, 5)}-${digits.slice(5, 9)}-${digits.slice(9)}`
  }
  
  if (digits.length === 12) {
    return `${digits.slice(0, 2)}-${digits.slice(2, 5)}-${digits.slice(5, 9)}-${digits.slice(9, 11)}-${digits.slice(11)}`
  }
  
  return inn
}

/**
 * Форматирует ОГРН
 */
export function formatOgrn(ogrn: string): string {
  if (!ogrn) return '-'
  
  const digits = ogrn.replace(/\D/g, '')
  
  if (digits.length === 13) {
    return `${digits.slice(0, 1)}-${digits.slice(1, 5)}-${digits.slice(5, 9)}-${digits.slice(9, 13)}`
  }
  
  if (digits.length === 15) {
    return `${digits.slice(0, 1)}-${digits.slice(1, 5)}-${digits.slice(5, 9)}-${digits.slice(9, 15)}`
  }
  
  return ogrn
}
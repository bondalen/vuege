// Утилиты для работы с датами

import { DATE_FORMATS } from '../constants'

/**
 * Форматирует дату в указанном формате
 */
export function formatDate(date: Date | string | null | undefined, format: string = DATE_FORMATS.DISPLAY): string {
  if (!date) return '-'
  
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  if (isNaN(dateObj.getTime())) return '-'
  
  const day = dateObj.getDate().toString().padStart(2, '0')
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0')
  const year = dateObj.getFullYear()
  const hours = dateObj.getHours().toString().padStart(2, '0')
  const minutes = dateObj.getMinutes().toString().padStart(2, '0')
  const seconds = dateObj.getSeconds().toString().padStart(2, '0')
  
  switch (format) {
    case DATE_FORMATS.DISPLAY:
      return `${day}.${month}.${year}`
    case DATE_FORMATS.API:
      return `${year}-${month}-${day}`
    case DATE_FORMATS.DATETIME:
      return `${day}.${month}.${year} ${hours}:${minutes}`
    case DATE_FORMATS.TIME:
      return `${hours}:${minutes}`
    case 'full':
      return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`
    case 'month-year':
      return `${month}.${year}`
    case 'year':
      return year.toString()
    default:
      return `${day}.${month}.${year}`
  }
}

/**
 * Получает относительное время (например, "2 часа назад")
 */
export function getRelativeTime(date: Date | string): string {
  const now = new Date()
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000)
  
  if (diffInSeconds < 60) {
    return 'только что'
  }
  
  const diffInMinutes = Math.floor(diffInSeconds / 60)
  if (diffInMinutes < 60) {
    return `${diffInMinutes} мин. назад`
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60)
  if (diffInHours < 24) {
    return `${diffInHours} ч. назад`
  }
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays < 7) {
    return `${diffInDays} дн. назад`
  }
  
  const diffInWeeks = Math.floor(diffInDays / 7)
  if (diffInWeeks < 4) {
    return `${diffInWeeks} нед. назад`
  }
  
  const diffInMonths = Math.floor(diffInDays / 30)
  if (diffInMonths < 12) {
    return `${diffInMonths} мес. назад`
  }
  
  const diffInYears = Math.floor(diffInDays / 365)
  return `${diffInYears} лет назад`
}

/**
 * Проверяет, является ли дата сегодняшней
 */
export function isToday(date: Date | string): boolean {
  const today = new Date()
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  return dateObj.toDateString() === today.toDateString()
}

/**
 * Проверяет, является ли дата вчерашней
 */
export function isYesterday(date: Date | string): boolean {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  return dateObj.toDateString() === yesterday.toDateString()
}

/**
 * Проверяет, является ли дата в этом году
 */
export function isThisYear(date: Date | string): boolean {
  const thisYear = new Date().getFullYear()
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  return dateObj.getFullYear() === thisYear
}

/**
 * Получает начало дня
 */
export function getStartOfDay(date: Date | string): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const startOfDay = new Date(dateObj)
  startOfDay.setHours(0, 0, 0, 0)
  return startOfDay
}

/**
 * Получает конец дня
 */
export function getEndOfDay(date: Date | string): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const endOfDay = new Date(dateObj)
  endOfDay.setHours(23, 59, 59, 999)
  return endOfDay
}

/**
 * Получает начало недели
 */
export function getStartOfWeek(date: Date | string): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const startOfWeek = new Date(dateObj)
  const day = startOfWeek.getDay()
  const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1)
  startOfWeek.setDate(diff)
  startOfWeek.setHours(0, 0, 0, 0)
  return startOfWeek
}

/**
 * Получает конец недели
 */
export function getEndOfWeek(date: Date | string): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const endOfWeek = new Date(dateObj)
  const day = endOfWeek.getDay()
  const diff = endOfWeek.getDate() - day + (day === 0 ? 0 : 7)
  endOfWeek.setDate(diff)
  endOfWeek.setHours(23, 59, 59, 999)
  return endOfWeek
}

/**
 * Получает начало месяца
 */
export function getStartOfMonth(date: Date | string): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const startOfMonth = new Date(dateObj.getFullYear(), dateObj.getMonth(), 1)
  return startOfMonth
}

/**
 * Получает конец месяца
 */
export function getEndOfMonth(date: Date | string): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const endOfMonth = new Date(dateObj.getFullYear(), dateObj.getMonth() + 1, 0)
  endOfMonth.setHours(23, 59, 59, 999)
  return endOfMonth
}

/**
 * Добавляет дни к дате
 */
export function addDays(date: Date | string, days: number): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const result = new Date(dateObj)
  result.setDate(result.getDate() + days)
  return result
}

/**
 * Добавляет месяцы к дате
 */
export function addMonths(date: Date | string, months: number): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const result = new Date(dateObj)
  result.setMonth(result.getMonth() + months)
  return result
}

/**
 * Добавляет годы к дате
 */
export function addYears(date: Date | string, years: number): Date {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const result = new Date(dateObj)
  result.setFullYear(result.getFullYear() + years)
  return result
}

/**
 * Получает разницу в днях между двумя датами
 */
export function getDaysDifference(date1: Date | string, date2: Date | string): number {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2
  
  const timeDiff = dateObj2.getTime() - dateObj1.getTime()
  return Math.ceil(timeDiff / (1000 * 3600 * 24))
}

/**
 * Получает возраст в годах
 */
export function getAge(birthDate: Date | string, deathDate?: Date | string): number {
  const birth = typeof birthDate === 'string' ? new Date(birthDate) : birthDate
  const death = deathDate ? (typeof deathDate === 'string' ? new Date(deathDate) : deathDate) : new Date()
  
  let age = death.getFullYear() - birth.getFullYear()
  const monthDiff = death.getMonth() - birth.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && death.getDate() < birth.getDate())) {
    age--
  }
  
  return age
}

/**
 * Проверяет, является ли год високосным
 */
export function isLeapYear(year: number): boolean {
  return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0)
}

/**
 * Получает количество дней в месяце
 */
export function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate()
}

/**
 * Получает название месяца на русском языке
 */
export function getMonthName(month: number): string {
  const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ]
  return months[month]
}

/**
 * Получает сокращенное название месяца на русском языке
 */
export function getShortMonthName(month: number): string {
  const months = [
    'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
    'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'
  ]
  return months[month]
}

/**
 * Получает название дня недели на русском языке
 */
export function getDayName(day: number): string {
  const days = [
    'Воскресенье', 'Понедельник', 'Вторник', 'Среда',
    'Четверг', 'Пятница', 'Суббота'
  ]
  return days[day]
}

/**
 * Получает сокращенное название дня недели на русском языке
 */
export function getShortDayName(day: number): string {
  const days = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
  return days[day]
}
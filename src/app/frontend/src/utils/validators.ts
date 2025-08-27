// Утилиты для валидации данных

/**
 * Проверяет, является ли строка валидным email
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Проверяет, является ли строка валидным ИНН
 */
export function isValidInn(inn: string): boolean {
  const digits = inn.replace(/\D/g, '')
  
  if (digits.length !== 10 && digits.length !== 12) {
    return false
  }
  
  // Алгоритм проверки контрольных цифр ИНН
  const weights10 = [2, 4, 10, 3, 5, 9, 4, 6, 8]
  const weights11 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
  const weights12 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
  
  if (digits.length === 10) {
    const sum = weights10.reduce((acc, weight, index) => acc + weight * parseInt(digits[index]), 0)
    const control = (sum % 11) % 10
    return control === parseInt(digits[9])
  }
  
  if (digits.length === 12) {
    const sum11 = weights11.reduce((acc, weight, index) => acc + weight * parseInt(digits[index]), 0)
    const control11 = (sum11 % 11) % 10
    
    const sum12 = weights12.reduce((acc, weight, index) => acc + weight * parseInt(digits[index]), 0)
    const control12 = (sum12 % 11) % 10
    
    return control11 === parseInt(digits[10]) && control12 === parseInt(digits[11])
  }
  
  return false
}

/**
 * Проверяет, является ли строка валидным ОГРН
 */
export function isValidOgrn(ogrn: string): boolean {
  const digits = ogrn.replace(/\D/g, '')
  
  if (digits.length !== 13 && digits.length !== 15) {
    return false
  }
  
  // Алгоритм проверки контрольной цифры ОГРН
  if (digits.length === 13) {
    const sum = digits.slice(0, 12).split('').reduce((acc, digit, index) => {
      return acc + parseInt(digit) * (index < 11 ? 1 : 3)
    }, 0)
    const control = (sum % 11) % 10
    return control === parseInt(digits[12])
  }
  
  if (digits.length === 15) {
    const sum = digits.slice(0, 14).split('').reduce((acc, digit, index) => {
      return acc + parseInt(digit) * (index < 13 ? 1 : 3)
    }, 0)
    const control = (sum % 13) % 10
    return control === parseInt(digits[14])
  }
  
  return false
}

/**
 * Проверяет, является ли строка валидным номером телефона
 */
export function isValidPhone(phone: string): boolean {
  const digits = phone.replace(/\D/g, '')
  return digits.length === 10 || digits.length === 11
}

/**
 * Проверяет, является ли строка валидной датой
 */
export function isValidDate(date: string): boolean {
  const dateObj = new Date(date)
  return !isNaN(dateObj.getTime())
}

/**
 * Проверяет, является ли дата в будущем
 */
export function isFutureDate(date: string): boolean {
  const dateObj = new Date(date)
  const now = new Date()
  return dateObj > now
}

/**
 * Проверяет, является ли дата в прошлом
 */
export function isPastDate(date: string): boolean {
  const dateObj = new Date(date)
  const now = new Date()
  return dateObj < now
}

/**
 * Проверяет, является ли строка валидными координатами
 */
export function isValidCoordinates(latitude: number, longitude: number): boolean {
  return latitude >= -90 && latitude <= 90 && longitude >= -180 && longitude <= 180
}

/**
 * Проверяет, является ли строка непустой
 */
export function isNotEmpty(value: string): boolean {
  return value.trim().length > 0
}

/**
 * Проверяет минимальную длину строки
 */
export function hasMinLength(value: string, minLength: number): boolean {
  return value.length >= minLength
}

/**
 * Проверяет максимальную длину строки
 */
export function hasMaxLength(value: string, maxLength: number): boolean {
  return value.length <= maxLength
}

/**
 * Проверяет, является ли число положительным
 */
export function isPositive(value: number): boolean {
  return value > 0
}

/**
 * Проверяет, является ли число неотрицательным
 */
export function isNonNegative(value: number): boolean {
  return value >= 0
}

/**
 * Проверяет, находится ли число в диапазоне
 */
export function isInRange(value: number, min: number, max: number): boolean {
  return value >= min && value <= max
}

/**
 * Проверяет, является ли строка валидным URL
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
 * Проверяет, является ли строка валидным IP адресом
 */
export function isValidIpAddress(ip: string): boolean {
  const ipv4Regex = /^(\d{1,3}\.){3}\d{1,3}$/
  const ipv6Regex = /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/
  
  if (ipv4Regex.test(ip)) {
    const parts = ip.split('.')
    return parts.every(part => {
      const num = parseInt(part)
      return num >= 0 && num <= 255
    })
  }
  
  return ipv6Regex.test(ip)
}

/**
 * Проверяет, содержит ли строка только буквы
 */
export function containsOnlyLetters(value: string): boolean {
  return /^[а-яёa-z\s]+$/i.test(value)
}

/**
 * Проверяет, содержит ли строка только цифры
 */
export function containsOnlyDigits(value: string): boolean {
  return /^\d+$/.test(value)
}

/**
 * Проверяет, содержит ли строка только буквы и цифры
 */
export function containsOnlyLettersAndDigits(value: string): boolean {
  return /^[а-яёa-z0-9\s]+$/i.test(value)
}

/**
 * Composable функция для использования всех валидаторов
 */
export function useValidators() {
  return {
    isValidEmail,
    isValidInn,
    isValidOgrn,
    isValidPhone,
    isValidDate,
    isFutureDate,
    isPastDate,
    isValidCoordinates,
    isNotEmpty,
    hasMinLength,
    hasMaxLength,
    isPositive,
    isNonNegative,
    isInRange,
    isValidUrl,
    isValidIpAddress,
    containsOnlyLetters,
    containsOnlyDigits,
    containsOnlyLettersAndDigits
  }
}

/**
 * Объект со всеми валидаторами для совместимости
 */
export const validators = {
  validateEmail: isValidEmail,
  validatePhone: isValidPhone,
  validateInn: isValidInn,
  validateOgrn: isValidOgrn,
  validateDate: isValidDate,
  validateCoordinates: isValidCoordinates,
  validateRequired: isNotEmpty,
  validateMinLength: hasMinLength,
  validateMaxLength: hasMaxLength,
  validatePattern: (value: string, pattern: RegExp) => pattern.test(value),
  validateRange: isInRange,
  validateCustom: (value: any, validator: (value: any) => boolean) => validator(value)
}

// Утилиты для валидации данных

/**
 * Правила валидации
 */
export interface ValidationRule {
  required?: boolean
  minLength?: number
  maxLength?: number
  pattern?: RegExp
  email?: boolean
  url?: boolean
  number?: boolean
  integer?: boolean
  positive?: boolean
  min?: number
  max?: number
  custom?: (value: any) => boolean | string
}

/**
 * Результат валидации
 */
export interface ValidationResult {
  isValid: boolean
  errors: string[]
}

/**
 * Валидирует значение по правилам
 */
export function validate(value: any, rules: ValidationRule): ValidationResult {
  const errors: string[] = []
  
  // Проверка на обязательность
  if (rules.required && (value === null || value === undefined || value === '')) {
    errors.push('Поле обязательно для заполнения')
  }
  
  if (value !== null && value !== undefined && value !== '') {
    const stringValue = String(value)
    
    // Проверка минимальной длины
    if (rules.minLength && stringValue.length < rules.minLength) {
      errors.push(`Минимальная длина: ${rules.minLength} символов`)
    }
    
    // Проверка максимальной длины
    if (rules.maxLength && stringValue.length > rules.maxLength) {
      errors.push(`Максимальная длина: ${rules.maxLength} символов`)
    }
    
    // Проверка по регулярному выражению
    if (rules.pattern && !rules.pattern.test(stringValue)) {
      errors.push('Неверный формат')
    }
    
    // Проверка email
    if (rules.email && !isValidEmail(stringValue)) {
      errors.push('Неверный формат email')
    }
    
    // Проверка URL
    if (rules.url && !isValidUrl(stringValue)) {
      errors.push('Неверный формат URL')
    }
    
    // Проверка числа
    if (rules.number && !isNumber(stringValue)) {
      errors.push('Должно быть числом')
    }
    
    // Проверка целого числа
    if (rules.integer && !isInteger(stringValue)) {
      errors.push('Должно быть целым числом')
    }
    
    // Проверка положительного числа
    if (rules.positive && !isPositive(stringValue)) {
      errors.push('Должно быть положительным числом')
    }
    
    // Проверка минимального значения
    if (rules.min !== undefined && isNumber(stringValue) && parseFloat(stringValue) < rules.min) {
      errors.push(`Минимальное значение: ${rules.min}`)
    }
    
    // Проверка максимального значения
    if (rules.max !== undefined && isNumber(stringValue) && parseFloat(stringValue) > rules.max) {
      errors.push(`Максимальное значение: ${rules.max}`)
    }
    
    // Пользовательская валидация
    if (rules.custom) {
      const customResult = rules.custom(value)
      if (customResult !== true) {
        errors.push(typeof customResult === 'string' ? customResult : 'Неверное значение')
      }
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

/**
 * Валидирует объект по схеме
 */
export function validateObject(obj: any, schema: Record<string, ValidationRule>): ValidationResult {
  const errors: string[] = []
  
  for (const [field, rules] of Object.entries(schema)) {
    const result = validate(obj[field], rules)
    if (!result.isValid) {
      errors.push(...result.errors.map(error => `${field}: ${error}`))
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

/**
 * Проверяет, является ли значение валидным email
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Проверяет, является ли значение валидным URL
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
 * Проверяет, является ли значение числом
 */
export function isNumber(value: any): boolean {
  return typeof value === 'number' && !isNaN(value) && isFinite(value)
}

/**
 * Проверяет, является ли значение целым числом
 */
export function isInteger(value: any): boolean {
  return Number.isInteger(Number(value))
}

/**
 * Проверяет, является ли значение положительным числом
 */
export function isPositive(value: any): boolean {
  const num = Number(value)
  return isNumber(num) && num > 0
}

/**
 * Проверяет, является ли значение неотрицательным числом
 */
export function isNonNegative(value: any): boolean {
  const num = Number(value)
  return isNumber(num) && num >= 0
}

/**
 * Проверяет, находится ли число в диапазоне
 */
export function isInRange(value: any, min: number, max: number): boolean {
  const num = Number(value)
  return isNumber(num) && num >= min && num <= max
}

/**
 * Проверяет, является ли значение валидным ИНН
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
 * Проверяет, является ли значение валидным ОГРН
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
 * Проверяет, является ли значение валидным номером телефона
 */
export function isValidPhone(phone: string): boolean {
  const digits = phone.replace(/\D/g, '')
  return digits.length === 10 || digits.length === 11
}

/**
 * Проверяет, является ли значение валидной датой
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
 * Проверяет, является ли значение валидными координатами
 */
export function isValidCoordinates(latitude: number, longitude: number): boolean {
  return latitude >= -90 && latitude <= 90 && longitude >= -180 && longitude <= 180
}

/**
 * Проверяет, является ли значение непустой строкой
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
 * Проверяет, является ли значение валидным IP адресом
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
 * Проверяет, является ли значение валидным паролем
 */
export function isValidPassword(password: string): boolean {
  // Минимум 8 символов, хотя бы одна буква и одна цифра
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/
  return passwordRegex.test(password)
}

/**
 * Проверяет, является ли значение валидным именем пользователя
 */
export function isValidUsername(username: string): boolean {
  // 3-20 символов, только буквы, цифры, подчеркивания и дефисы
  const usernameRegex = /^[a-zA-Z0-9_-]{3,20}$/
  return usernameRegex.test(username)
}

/**
 * Проверяет, является ли значение валидным именем файла
 */
export function isValidFilename(filename: string): boolean {
  // Не содержит запрещенные символы
  const invalidChars = /[<>:"/\\|?*]/
  return !invalidChars.test(filename) && filename.length > 0 && filename.length <= 255
}

/**
 * Проверяет, является ли значение валидным размером файла
 */
export function isValidFileSize(size: number, maxSize: number): boolean {
  return size >= 0 && size <= maxSize
}

/**
 * Проверяет, является ли значение валидным типом файла
 */
export function isValidFileType(filename: string, allowedTypes: string[]): boolean {
  const extension = filename.split('.').pop()?.toLowerCase()
  return extension ? allowedTypes.includes(extension) : false
}
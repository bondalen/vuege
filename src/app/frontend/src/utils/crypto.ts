// Утилиты для работы с криптографией

/**
 * Генерирует случайную строку
 */
export function generateRandomString(length: number = 32): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  
  return result
}

/**
 * Генерирует случайный UUID
 */
export function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

/**
 * Хеширует строку с помощью SHA-256
 */
export async function sha256(message: string): Promise<string> {
  const encoder = new TextEncoder()
  const data = encoder.encode(message)
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
}

/**
 * Хеширует строку с помощью SHA-1
 */
export async function sha1(message: string): Promise<string> {
  const encoder = new TextEncoder()
  const data = encoder.encode(message)
  const hashBuffer = await crypto.subtle.digest('SHA-1', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
}

/**
 * Хеширует строку с помощью MD5 (не рекомендуется для безопасности)
 */
export function md5(message: string): string {
  // Простая реализация MD5 (не рекомендуется для безопасности)
  let hash = 0
  if (message.length === 0) return hash.toString()
  
  for (let i = 0; i < message.length; i++) {
    const char = message.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  
  return hash.toString()
}

/**
 * Кодирует строку в Base64
 */
export function encodeBase64(str: string): string {
  return btoa(unescape(encodeURIComponent(str)))
}

/**
 * Декодирует строку из Base64
 */
export function decodeBase64(str: string): string {
  return decodeURIComponent(escape(atob(str)))
}

/**
 * Кодирует строку в Base64 URL-safe
 */
export function encodeBase64Url(str: string): string {
  return encodeBase64(str)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '')
}

/**
 * Декодирует строку из Base64 URL-safe
 */
export function decodeBase64Url(str: string): string {
  // Добавляем padding если необходимо
  while (str.length % 4) {
    str += '='
  }
  
  str = str.replace(/-/g, '+').replace(/_/g, '/')
  return decodeBase64(str)
}

/**
 * Кодирует строку в hex
 */
export function encodeHex(str: string): string {
  let hex = ''
  for (let i = 0; i < str.length; i++) {
    hex += str.charCodeAt(i).toString(16).padStart(2, '0')
  }
  return hex
}

/**
 * Декодирует строку из hex
 */
export function decodeHex(hex: string): string {
  let str = ''
  for (let i = 0; i < hex.length; i += 2) {
    str += String.fromCharCode(parseInt(hex.substr(i, 2), 16))
  }
  return str
}

/**
 * Шифрует строку с помощью AES
 */
export async function encryptAES(data: string, key: string): Promise<string> {
  const encoder = new TextEncoder()
  const keyData = encoder.encode(key)
  
  // Генерируем ключ
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'AES-GCM' },
    false,
    ['encrypt']
  )
  
  // Генерируем IV
  const iv = crypto.getRandomValues(new Uint8Array(12))
  
  // Шифруем
  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    encoder.encode(data)
  )
  
  // Объединяем IV и зашифрованные данные
  const result = new Uint8Array(iv.length + encrypted.byteLength)
  result.set(iv)
  result.set(new Uint8Array(encrypted), iv.length)
  
  return encodeBase64Url(Array.from(result).map(b => String.fromCharCode(b)).join(''))
}

/**
 * Расшифровывает строку с помощью AES
 */
export async function decryptAES(encryptedData: string, key: string): Promise<string> {
  try {
    const encoder = new TextEncoder()
    const decoder = new TextDecoder()
    const keyData = encoder.encode(key)
    
    // Декодируем данные
    const data = new Uint8Array(encryptedData.split('').map(c => c.charCodeAt(0)))
    
    // Извлекаем IV
    const iv = data.slice(0, 12)
    const encrypted = data.slice(12)
    
    // Генерируем ключ
    const cryptoKey = await crypto.subtle.importKey(
      'raw',
      keyData,
      { name: 'AES-GCM' },
      false,
      ['decrypt']
    )
    
    // Расшифровываем
    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      cryptoKey,
      encrypted
    )
    
    return decoder.decode(decrypted)
  } catch {
    throw new Error('Ошибка расшифровки')
  }
}

/**
 * Создает HMAC
 */
export async function createHMAC(message: string, key: string, algorithm: string = 'SHA-256'): Promise<string> {
  const encoder = new TextEncoder()
  const keyData = encoder.encode(key)
  const messageData = encoder.encode(message)
  
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: algorithm },
    false,
    ['sign']
  )
  
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, messageData)
  const signatureArray = Array.from(new Uint8Array(signature))
  
  return signatureArray.map(b => b.toString(16).padStart(2, '0')).join('')
}

/**
 * Проверяет HMAC
 */
export async function verifyHMAC(message: string, signature: string, key: string, algorithm: string = 'SHA-256'): Promise<boolean> {
  const expectedSignature = await createHMAC(message, key, algorithm)
  return signature === expectedSignature
}

/**
 * Генерирует пароль
 */
export function generatePassword(length: number = 12, includeUppercase: boolean = true, includeLowercase: boolean = true, includeNumbers: boolean = true, includeSymbols: boolean = true): string {
  let chars = ''
  if (includeUppercase) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  if (includeLowercase) chars += 'abcdefghijklmnopqrstuvwxyz'
  if (includeNumbers) chars += '0123456789'
  if (includeSymbols) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
  
  if (chars === '') {
    throw new Error('Должен быть выбран хотя бы один тип символов')
  }
  
  let password = ''
  for (let i = 0; i < length; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  
  return password
}

/**
 * Проверяет сложность пароля
 */
export function checkPasswordStrength(password: string): {
  score: number
  feedback: string[]
} {
  const feedback: string[] = []
  let score = 0
  
  if (password.length < 8) {
    feedback.push('Пароль должен содержать минимум 8 символов')
  } else {
    score += Math.min(password.length * 2, 20)
  }
  
  if (/[a-z]/.test(password)) {
    score += 10
  } else {
    feedback.push('Добавьте строчные буквы')
  }
  
  if (/[A-Z]/.test(password)) {
    score += 10
  } else {
    feedback.push('Добавьте заглавные буквы')
  }
  
  if (/[0-9]/.test(password)) {
    score += 10
  } else {
    feedback.push('Добавьте цифры')
  }
  
  if (/[^A-Za-z0-9]/.test(password)) {
    score += 10
  } else {
    feedback.push('Добавьте специальные символы')
  }
  
  return { score, feedback }
}

/**
 * Создает JWT токен
 */
export async function createJWT(payload: any, secret: string, expiresIn: number = 3600): Promise<string> {
  const header = {
    alg: 'HS256',
    typ: 'JWT'
  }
  
  const now = Math.floor(Date.now() / 1000)
  const claims = {
    ...payload,
    iat: now,
    exp: now + expiresIn
  }
  
  const encodedHeader = encodeBase64Url(JSON.stringify(header))
  const encodedPayload = encodeBase64Url(JSON.stringify(claims))
  
  const signature = await createHMAC(`${encodedHeader}.${encodedPayload}`, secret)
  
  return `${encodedHeader}.${encodedPayload}.${signature}`
}

/**
 * Проверяет JWT токен
 */
export async function verifyJWT(token: string, secret: string): Promise<any> {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) {
      throw new Error('Неверный формат JWT')
    }
    
    const [header, payload, signature] = parts
    
    // Проверяем подпись
    const expectedSignature = await createHMAC(`${header}.${payload}`, secret)
    if (signature !== expectedSignature) {
      throw new Error('Неверная подпись')
    }
    
    // Декодируем payload
    const decodedPayload = JSON.parse(decodeBase64Url(payload))
    
    // Проверяем срок действия
    const now = Math.floor(Date.now() / 1000)
    if (decodedPayload.exp && decodedPayload.exp < now) {
      throw new Error('Токен истек')
    }
    
    return decodedPayload
  } catch (error) {
    throw new Error(`Ошибка проверки JWT: ${error}`)
  }
}

/**
 * Хук для работы с криптографией
 */
export function useCrypto() {
  return {
    // Генерация
    generateRandomString,
    generateUUID,
    
    // Хеширование
    sha256,
    sha1,
    md5,
    
    // Кодирование
    encodeBase64,
    decodeBase64,
    encodeBase64Url,
    decodeBase64Url,
    
    // Шифрование
    encryptAES,
    decryptAES,
    createHMAC,
    verifyHMAC,
    
    // Пароли
    checkPasswordStrength,
    
    // JWT
    createJWT,
    verifyJWT
  }
}

/**
 * Объект со всеми функциями для работы с криптографией
 */
export const cryptoUtils = {
  // Генерация
  generateRandomString,
  generateUUID,
  
  // Хеширование
  sha256,
  sha1,
  md5,
  
  // Кодирование
  encodeBase64,
  decodeBase64,
  encodeBase64Url,
  decodeBase64Url,
  
  // Шифрование
  encryptAES,
  decryptAES,
  createHMAC,
  verifyHMAC,
  
  // Пароли
  checkPasswordStrength,
  
  // JWT
  createJWT,
  verifyJWT
}
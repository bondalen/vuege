// Утилиты для работы с ошибками

import { ERROR_MESSAGES } from '../constants'

/**
 * Класс для пользовательских ошибок приложения
 */
export class VuegeError extends Error {
  public code: string
  public details?: any

  constructor(message: string, code: string = 'UNKNOWN_ERROR', details?: any) {
    super(message)
    this.name = 'VuegeError'
    this.code = code
    this.details = details
  }
}

/**
 * Обрабатывает GraphQL ошибки
 */
export function handleGraphQLError(error: any): string {
  if (error.graphQLErrors && error.graphQLErrors.length > 0) {
    return error.graphQLErrors[0].message
  }
  
  if (error.networkError) {
    return ERROR_MESSAGES.NETWORK_ERROR
  }
  
  if (error.message) {
    return error.message
  }
  
  return ERROR_MESSAGES.UNKNOWN_ERROR
}

/**
 * Обрабатывает HTTP ошибки
 */
export function handleHttpError(status: number, message?: string): string {
  switch (status) {
    case 400:
      return message || 'Некорректный запрос'
    case 401:
      return ERROR_MESSAGES.UNAUTHORIZED
    case 403:
      return ERROR_MESSAGES.FORBIDDEN
    case 404:
      return ERROR_MESSAGES.NOT_FOUND
    case 422:
      return ERROR_MESSAGES.VALIDATION_ERROR
    case 500:
      return ERROR_MESSAGES.SERVER_ERROR
    default:
      return message || ERROR_MESSAGES.UNKNOWN_ERROR
  }
}

/**
 * Логирует ошибку в консоль
 */
export function logError(error: any, context?: string): void {
  const timestamp = new Date().toISOString()
  const errorInfo = {
    timestamp,
    context,
    error: error instanceof Error ? {
      name: error.name,
      message: error.message,
      stack: error.stack
    } : error
  }
  
  console.error('Vuege Error:', errorInfo)
  
  // В продакшене можно отправлять ошибки в систему мониторинга
  if (import.meta.env.PROD) {
    // sendErrorToMonitoring(errorInfo)
  }
}

/**
 * Создает пользовательскую ошибку валидации
 */
export function createValidationError(field: string, message: string): VuegeError {
  return new VuegeError(
    `Ошибка валидации поля "${field}": ${message}`,
    'VALIDATION_ERROR',
    { field, message }
  )
}

/**
 * Создает ошибку аутентификации
 */
export function createAuthError(message?: string): VuegeError {
  return new VuegeError(
    message || ERROR_MESSAGES.UNAUTHORIZED,
    'AUTH_ERROR'
  )
}

/**
 * Создает ошибку доступа
 */
export function createForbiddenError(message?: string): VuegeError {
  return new VuegeError(
    message || ERROR_MESSAGES.FORBIDDEN,
    'FORBIDDEN_ERROR'
  )
}

/**
 * Создает ошибку "не найдено"
 */
export function createNotFoundError(resource: string): VuegeError {
  return new VuegeError(
    `${resource} не найден`,
    'NOT_FOUND_ERROR',
    { resource }
  )
}

/**
 * Проверяет, является ли ошибка ошибкой сети
 */
export function isNetworkError(error: any): boolean {
  return error.networkError || 
         error.message?.includes('Network Error') ||
         error.message?.includes('Failed to fetch')
}

/**
 * Проверяет, является ли ошибка ошибкой аутентификации
 */
export function isAuthError(error: any): boolean {
  return error.code === 'AUTH_ERROR' ||
         error.message?.includes('Unauthorized') ||
         error.message?.includes('Authentication')
}

/**
 * Проверяет, является ли ошибка ошибкой валидации
 */
export function isValidationError(error: any): boolean {
  return error.code === 'VALIDATION_ERROR' ||
         error.message?.includes('Validation') ||
         error.message?.includes('Invalid')
}

/**
 * Получает сообщение об ошибке для пользователя
 */
export function getUserFriendlyMessage(error: any): string {
  if (error instanceof VuegeError) {
    return error.message
  }
  
  if (isNetworkError(error)) {
    return ERROR_MESSAGES.NETWORK_ERROR
  }
  
  if (isAuthError(error)) {
    return ERROR_MESSAGES.UNAUTHORIZED
  }
  
  if (isValidationError(error)) {
    return ERROR_MESSAGES.VALIDATION_ERROR
  }
  
  return error.message || ERROR_MESSAGES.UNKNOWN_ERROR
}

/**
 * Форматирует ошибку для отображения
 */
export function formatError(error: any): {
  title: string
  message: string
  details?: string
} {
  const message = getUserFriendlyMessage(error)
  
  if (error instanceof VuegeError) {
    return {
      title: 'Ошибка',
      message,
      details: error.details ? JSON.stringify(error.details, null, 2) : undefined
    }
  }
  
  return {
    title: 'Ошибка',
    message,
    details: error.stack
  }
}
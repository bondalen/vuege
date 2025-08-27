// Утилиты для работы с API

import { API_BASE_URL, GRAPHQL_ENDPOINT } from '../constants'
import { loadAuthToken } from './storage'
import { handleHttpError, logError } from './errors'

/**
 * Базовые заголовки для API запросов
 */
export function getDefaultHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
  
  const token = loadAuthToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  return headers
}

/**
 * Выполняет HTTP GET запрос
 */
export async function apiGet<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
  try {
    const url = new URL(endpoint, API_BASE_URL)
    
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== undefined && params[key] !== null) {
          url.searchParams.append(key, params[key].toString())
        }
      })
    }
    
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: getDefaultHeaders()
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    return await response.json()
  } catch (error) {
    logError(error, `API GET ${endpoint}`)
    throw error
  }
}

/**
 * Выполняет HTTP POST запрос
 */
export async function apiPost<T>(endpoint: string, data?: any): Promise<T> {
  try {
    const url = new URL(endpoint, API_BASE_URL)
    
    const response = await fetch(url.toString(), {
      method: 'POST',
      headers: getDefaultHeaders(),
      body: data ? JSON.stringify(data) : undefined
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    return await response.json()
  } catch (error) {
    logError(error, `API POST ${endpoint}`)
    throw error
  }
}

/**
 * Выполняет HTTP PUT запрос
 */
export async function apiPut<T>(endpoint: string, data?: any): Promise<T> {
  try {
    const url = new URL(endpoint, API_BASE_URL)
    
    const response = await fetch(url.toString(), {
      method: 'PUT',
      headers: getDefaultHeaders(),
      body: data ? JSON.stringify(data) : undefined
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    return await response.json()
  } catch (error) {
    logError(error, `API PUT ${endpoint}`)
    throw error
  }
}

/**
 * Выполняет HTTP DELETE запрос
 */
export async function apiDelete<T>(endpoint: string): Promise<T> {
  try {
    const url = new URL(endpoint, API_BASE_URL)
    
    const response = await fetch(url.toString(), {
      method: 'DELETE',
      headers: getDefaultHeaders()
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    return await response.json()
  } catch (error) {
    logError(error, `API DELETE ${endpoint}`)
    throw error
  }
}

/**
 * Выполняет GraphQL запрос
 */
export async function graphqlQuery<T>(query: string, variables?: Record<string, any>): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${GRAPHQL_ENDPOINT}`, {
      method: 'POST',
      headers: getDefaultHeaders(),
      body: JSON.stringify({
        query,
        variables
      })
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    const result = await response.json()
    
    if (result.errors && result.errors.length > 0) {
      throw new Error(result.errors[0].message)
    }
    
    return result.data
  } catch (error) {
    logError(error, `GraphQL Query`)
    throw error
  }
}

/**
 * Выполняет GraphQL мутацию
 */
export async function graphqlMutation<T>(mutation: string, variables?: Record<string, any>): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${GRAPHQL_ENDPOINT}`, {
      method: 'POST',
      headers: getDefaultHeaders(),
      body: JSON.stringify({
        query: mutation,
        variables
      })
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    const result = await response.json()
    
    if (result.errors && result.errors.length > 0) {
      throw new Error(result.errors[0].message)
    }
    
    return result.data
  } catch (error) {
    logError(error, `GraphQL Mutation`)
    throw error
  }
}

/**
 * Загружает файл
 */
export async function downloadFile(endpoint: string, filename?: string): Promise<void> {
  try {
    const url = new URL(endpoint, API_BASE_URL)
    
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        ...getDefaultHeaders(),
        'Accept': '*/*'
      }
    })
    
    if (!response.ok) {
      throw new Error(handleHttpError(response.status, response.statusText))
    }
    
    const blob = await response.blob()
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
  } catch (error) {
    logError(error, `Download File ${endpoint}`)
    throw error
  }
}

/**
 * Загружает файл на сервер
 */
export async function uploadFile(endpoint: string, file: File, onProgress?: (progress: number) => void): Promise<any> {
  try {
    const url = new URL(endpoint, API_BASE_URL)
    const formData = new FormData()
    formData.append('file', file)
    
    const headers = getDefaultHeaders()
    delete headers['Content-Type'] // Убираем Content-Type для FormData
    
    const xhr = new XMLHttpRequest()
    
    return new Promise((resolve, reject) => {
      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable && onProgress) {
          const progress = (event.loaded / event.total) * 100
          onProgress(progress)
        }
      })
      
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText)
            resolve(response)
          } catch {
            resolve(xhr.responseText)
          }
        } else {
          reject(new Error(handleHttpError(xhr.status, xhr.statusText)))
        }
      })
      
      xhr.addEventListener('error', () => {
        reject(new Error('Ошибка сети при загрузке файла'))
      })
      
      xhr.open('POST', url.toString())
      
      // Добавляем заголовки
      Object.keys(headers).forEach(key => {
        xhr.setRequestHeader(key, headers[key])
      })
      
      xhr.send(formData)
    })
  } catch (error) {
    logError(error, `Upload File ${endpoint}`)
    throw error
  }
}

/**
 * Проверяет доступность API
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    
    return response.ok
  } catch {
    return false
  }
}

/**
 * Хук для работы с API
 */
export function useApi() {
  return {
    // Заголовки
    getDefaultHeaders,
    
    // HTTP методы
    apiGet,
    apiPost,
    apiPut,
    apiDelete,
    
    // GraphQL
    graphqlQuery,
    graphqlMutation,
    
    // Файлы
    downloadFile,
    uploadFile,
    
    // Утилиты
    checkApiHealth
  }
}

/**
 * Объект со всеми API функциями для совместимости
 */
export const api = {
  getDefaultHeaders,
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  graphqlQuery,
  graphqlMutation,
  downloadFile,
  uploadFile,
  checkApiHealth
}

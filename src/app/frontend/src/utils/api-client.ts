// Утилиты для работы с API и GraphQL

import { ApolloClient, InMemoryCache, createHttpLink, from } from '@apollo/client/core'
import { setContext } from '@apollo/client/link/context'
import { onError } from '@apollo/client/link/error'
import { RetryLink } from '@apollo/client/link/retry'
import { BatchHttpLink } from '@apollo/client/link/batch-http'
import type { DocumentNode, OperationVariables, ApolloQueryResult, FetchResult } from '@apollo/client/core'
import type { NormalizedCacheObject } from '@apollo/client/cache'

/**
 * Интерфейс для конфигурации API клиента
 */
export interface ApiClientConfig {
  uri: string
  wsUri?: string
  headers?: Record<string, string>
  timeout?: number
  retries?: number
  batchSize?: number
  batchDelay?: number
  enableBatching?: boolean
  enableRetries?: boolean
  enableErrorHandling?: boolean
  enableAuth?: boolean
  authTokenKey?: string
  onError?: (error: any) => void
  onRequest?: (operation: any) => void
  onResponse?: (response: any) => void
}

/**
 * Интерфейс для запроса
 */
export interface ApiRequest {
  url: string
  method: string
  headers?: Record<string, string>
  body?: any
  params?: Record<string, any>
  timeout?: number
  retries?: number
}

/**
 * Интерфейс для ответа
 */
export interface ApiResponse<T = any> {
  data: T
  status: number
  statusText: string
  headers: Record<string, string>
  ok: boolean
}

/**
 * Интерфейс для GraphQL запроса
 */
export interface GraphQLRequest {
  query: DocumentNode
  variables?: OperationVariables
  operationName?: string
  context?: Record<string, any>
}

/**
 * Интерфейс для GraphQL ответа
 */
export interface GraphQLResponse<T = any> {
  data: T
  errors?: any[]
  extensions?: Record<string, any>
}

/**
 * Класс для управления API клиентом
 */
export class ApiClientManager {
  private apolloClient: ApolloClient<NormalizedCacheObject>
  private config: ApiClientConfig
  private requestQueue: Map<string, Promise<any>>
  private cache: Map<string, { data: any; timestamp: number; ttl: number }>

  constructor(config: ApiClientConfig) {
    this.config = {
      uri: '/graphql',
      timeout: 30000,
      retries: 3,
      batchSize: 10,
      batchDelay: 10,
      enableBatching: true,
      enableRetries: true,
      enableErrorHandling: true,
      enableAuth: true,
      authTokenKey: 'authToken',
      ...config
    }

    this.requestQueue = new Map()
    this.cache = new Map()

    this.apolloClient = this.createApolloClient()
  }

  /**
   * Создает Apollo клиент
   */
  private createApolloClient(): ApolloClient<NormalizedCacheObject> {
    const links: any[] = []

    // HTTP линк
    const httpLink = this.config.enableBatching
      ? new BatchHttpLink({
          uri: this.config.uri,
          batchSize: this.config.batchSize,
          batchDelay: this.config.batchDelay,
          headers: this.config.headers
        })
      : createHttpLink({
          uri: this.config.uri,
          headers: this.config.headers
        })

    links.push(httpLink)

    // Retry линк
    if (this.config.enableRetries) {
      const retryLink = new RetryLink({
        delay: {
          initial: 300,
          max: 3000,
          jitter: true
        },
        attempts: {
          max: this.config.retries,
          retryIf: (error, _operation) => {
            return !!error && error.networkError
          }
        }
      })
      links.unshift(retryLink)
    }

    // Auth линк
    if (this.config.enableAuth) {
      const authLink = setContext((_, { headers }) => {
        const token = this.getAuthToken()
        return {
          headers: {
            ...headers,
            authorization: token ? `Bearer ${token}` : '',
            ...this.config.headers
          }
        }
      })
      links.unshift(authLink)
    }

    // Error handling линк
    if (this.config.enableErrorHandling) {
      const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
        if (graphQLErrors) {
          graphQLErrors.forEach(({ message, locations, path }) => {
            console.error(
              `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
            )
            if (this.config.onError) {
              this.config.onError({ type: 'graphql', error: { message, locations, path } })
            }
          })
        }

        if (networkError) {
          console.error(`[Network error]: ${networkError}`)
          if (this.config.onError) {
            this.config.onError({ type: 'network', error: networkError })
          }
        }
      })
      links.unshift(errorLink)
    }

    return new ApolloClient({
      link: from(links),
      cache: new InMemoryCache({
        typePolicies: {
          Query: {
            fields: {
              // Настройки кэширования для различных типов
              organizations: {
                merge(existing = [], incoming) {
                  return incoming
                }
              },
              states: {
                merge(existing = [], incoming) {
                  return incoming
                }
              },
              people: {
                merge(existing = [], incoming) {
                  return incoming
                }
              },
              locations: {
                merge(existing = [], incoming) {
                  return incoming
                }
              }
            }
          }
        }
      }),
      defaultOptions: {
        watchQuery: {
          errorPolicy: 'all',
          fetchPolicy: 'cache-and-network'
        },
        query: {
          errorPolicy: 'all',
          fetchPolicy: 'cache-first'
        },
        mutate: {
          errorPolicy: 'all'
        }
      }
    })
  }

  /**
   * Получает Apollo клиент
   */
  getApolloClient(): ApolloClient<NormalizedCacheObject> {
    return this.apolloClient
  }

  /**
   * Выполняет GraphQL запрос
   */
  async query<T = any>(
    query: DocumentNode,
    variables?: OperationVariables,
    context?: Record<string, any>
  ): Promise<ApolloQueryResult<T>> {
    const cacheKey = this.generateCacheKey(query, variables)
    
    // Проверяем кэш
    const cached = this.getFromCache(cacheKey)
    if (cached) {
      return cached
    }

    // Проверяем очередь запросов
    if (this.requestQueue.has(cacheKey)) {
      return this.requestQueue.get(cacheKey)!
    }

    const promise = this.apolloClient.query<T>({
      query,
      variables,
      context,
      fetchPolicy: 'network-only'
    })

    this.requestQueue.set(cacheKey, promise)

    try {
      const result = await promise
      this.setCache(cacheKey, result, 5 * 60 * 1000) // 5 минут
      return result
    } finally {
      this.requestQueue.delete(cacheKey)
    }
  }

  /**
   * Выполняет GraphQL мутацию
   */
  async mutate<T = any>(
    mutation: DocumentNode,
    variables?: OperationVariables,
    context?: Record<string, any>
  ): Promise<FetchResult<T>> {
    return this.apolloClient.mutate<T>({
      mutation,
      variables,
      context
    })
  }

  /**
   * Выполняет HTTP запрос
   */
  async request<T = any>(request: ApiRequest): Promise<ApiResponse<T>> {
    const { url, method, headers = {}, body, params, timeout = this.config.timeout } = request

    // Добавляем параметры к URL
    const urlWithParams = params ? this.buildUrl(url, params) : url

    // Добавляем заголовки авторизации
    const authHeaders = this.config.enableAuth ? this.getAuthHeaders() : {}
    const finalHeaders = { ...authHeaders, ...headers }

    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)

    try {
      const response = await fetch(urlWithParams, {
        method,
        headers: finalHeaders,
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      const responseData = await response.json()

      return {
        data: responseData,
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries()),
        ok: response.ok
      }
    } catch (error) {
      clearTimeout(timeoutId)
      throw error
    }
  }

  /**
   * Выполняет GET запрос
   */
  async get<T = any>(url: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    return this.request<T>({ url, method: 'GET', params })
  }

  /**
   * Выполняет POST запрос
   */
  async post<T = any>(url: string, body?: any): Promise<ApiResponse<T>> {
    return this.request<T>({ url, method: 'POST', body })
  }

  /**
   * Выполняет PUT запрос
   */
  async put<T = any>(url: string, body?: any): Promise<ApiResponse<T>> {
    return this.request<T>({ url, method: 'PUT', body })
  }

  /**
   * Выполняет DELETE запрос
   */
  async delete<T = any>(url: string): Promise<ApiResponse<T>> {
    return this.request<T>({ url, method: 'DELETE' })
  }

  /**
   * Загружает файл
   */
  async uploadFile(url: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse> {
    const formData = new FormData()
    formData.append('file', file)

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
          resolve({
            data: xhr.response,
            status: xhr.status,
            statusText: xhr.statusText,
            headers: {},
            ok: true
          })
        } else {
          reject(new Error(`Upload failed: ${xhr.status} ${xhr.statusText}`))
        }
      })

      xhr.addEventListener('error', () => {
        reject(new Error('Upload failed'))
      })

      xhr.open('POST', url)
      
      // Добавляем заголовки авторизации
      if (this.config.enableAuth) {
        const token = this.getAuthToken()
        if (token) {
          xhr.setRequestHeader('Authorization', `Bearer ${token}`)
        }
      }

      xhr.send(formData)
    })
  }

  /**
   * Скачивает файл
   */
  async downloadFile(url: string, filename?: string): Promise<void> {
    const response = await this.get(url)
    
    if (!response.ok) {
      throw new Error(`Download failed: ${response.status} ${response.statusText}`)
    }

    const blob = new Blob([response.data])
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
  }

  /**
   * Получает токен авторизации
   */
  private getAuthToken(): string | null {
    return localStorage.getItem(this.config.authTokenKey!)
  }

  /**
   * Получает заголовки авторизации
   */
  private getAuthHeaders(): Record<string, string> {
    const token = this.getAuthToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  /**
   * Строит URL с параметрами
   */
  private buildUrl(url: string, params: Record<string, any>): string {
    const urlObj = new URL(url, window.location.origin)
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        urlObj.searchParams.append(key, String(value))
      }
    })
    return urlObj.toString()
  }

  /**
   * Генерирует ключ кэша
   */
  private generateCacheKey(query: DocumentNode, variables?: OperationVariables): string {
    return `${query.loc?.source.body}-${JSON.stringify(variables)}`
  }

  /**
   * Получает данные из кэша
   */
  private getFromCache(key: string): any {
    const cached = this.cache.get(key)
    if (cached && Date.now() - cached.timestamp < cached.ttl) {
      return cached.data
    }
    this.cache.delete(key)
    return null
  }

  /**
   * Сохраняет данные в кэш
   */
  private setCache(key: string, data: any, ttl: number): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    })
  }

  /**
   * Очищает кэш
   */
  clearCache(): void {
    this.cache.clear()
    this.apolloClient.clearStore()
  }

  /**
   * Получает статистику кэша
   */
  getCacheStats(): Record<string, any> {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys()),
      apolloCacheSize: this.apolloClient.cache.extract()
    }
  }

  /**
   * Устанавливает токен авторизации
   */
  setAuthToken(token: string): void {
    localStorage.setItem(this.config.authTokenKey!, token)
  }

  /**
   * Удаляет токен авторизации
   */
  removeAuthToken(): void {
    localStorage.removeItem(this.config.authTokenKey!)
  }

  /**
   * Проверяет, авторизован ли пользователь
   */
  isAuthenticated(): boolean {
    return !!this.getAuthToken()
  }

  /**
   * Обновляет конфигурацию
   */
  updateConfig(newConfig: Partial<ApiClientConfig>): void {
    this.config = { ...this.config, ...newConfig }
  }

  /**
   * Получает конфигурацию
   */
  getConfig(): ApiClientConfig {
    return { ...this.config }
  }
}

/**
 * Глобальный менеджер API клиента
 */
let globalApiClientManager: ApiClientManager | null = null

/**
 * Получает глобальный менеджер API клиента
 */
export function getGlobalApiClientManager(): ApiClientManager {
  if (!globalApiClientManager) {
    globalApiClientManager = new ApiClientManager({
      uri: '/graphql'
    })
  }
  return globalApiClientManager
}

/**
 * Устанавливает глобальный менеджер API клиента
 */
export function setGlobalApiClientManager(manager: ApiClientManager): void {
  globalApiClientManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const apiClient = {
  getApolloClient: () => getGlobalApiClientManager().getApolloClient(),
  query: <T = any>(query: DocumentNode, variables?: OperationVariables, context?: Record<string, any>) => 
    getGlobalApiClientManager().query<T>(query, variables, context),
  mutate: <T = any>(mutation: DocumentNode, variables?: OperationVariables, context?: Record<string, any>) => 
    getGlobalApiClientManager().mutate<T>(mutation, variables, context),
  request: <T = any>(request: ApiRequest) => getGlobalApiClientManager().request<T>(request),
  get: <T = any>(url: string, params?: Record<string, any>) => getGlobalApiClientManager().get<T>(url, params),
  post: <T = any>(url: string, body?: any) => getGlobalApiClientManager().post<T>(url, body),
  put: <T = any>(url: string, body?: any) => getGlobalApiClientManager().put<T>(url, body),
  delete: <T = any>(url: string) => getGlobalApiClientManager().delete<T>(url),
  uploadFile: (url: string, file: File, onProgress?: (progress: number) => void) => 
    getGlobalApiClientManager().uploadFile(url, file, onProgress),
  downloadFile: (url: string, filename?: string) => getGlobalApiClientManager().downloadFile(url, filename),
  clearCache: () => getGlobalApiClientManager().clearCache(),
  getCacheStats: () => getGlobalApiClientManager().getCacheStats(),
  setAuthToken: (token: string) => getGlobalApiClientManager().setAuthToken(token),
  removeAuthToken: () => getGlobalApiClientManager().removeAuthToken(),
  isAuthenticated: () => getGlobalApiClientManager().isAuthenticated(),
  updateConfig: (newConfig: Partial<ApiClientConfig>) => getGlobalApiClientManager().updateConfig(newConfig),
  getConfig: () => getGlobalApiClientManager().getConfig()
}

/**
 * Хук для использования API клиента в Vue компонентах
 */
export function useApiClient() {
  const manager = getGlobalApiClientManager()
  
  return {
    apolloClient: manager.getApolloClient(),
    query: manager.query.bind(manager),
    mutate: manager.mutate.bind(manager),
    request: manager.request.bind(manager),
    get: manager.get.bind(manager),
    post: manager.post.bind(manager),
    put: manager.put.bind(manager),
    delete: manager.delete.bind(manager),
    uploadFile: manager.uploadFile.bind(manager),
    downloadFile: manager.downloadFile.bind(manager),
    clearCache: manager.clearCache.bind(manager),
    getCacheStats: manager.getCacheStats.bind(manager),
    setAuthToken: manager.setAuthToken.bind(manager),
    removeAuthToken: manager.removeAuthToken.bind(manager),
    isAuthenticated: manager.isAuthenticated.bind(manager),
    updateConfig: manager.updateConfig.bind(manager),
    getConfig: manager.getConfig.bind(manager)
  }
}
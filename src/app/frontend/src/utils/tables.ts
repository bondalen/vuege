// Утилиты для работы с таблицами и данными

import { ref, computed, Ref } from 'vue'

/**
 * Интерфейс для колонки таблицы
 */
export interface TableColumn<T = any> {
  key: string
  label: string
  field?: keyof T | ((item: T) => any)
  sortable?: boolean
  filterable?: boolean
  width?: string | number
  align?: 'left' | 'center' | 'right'
  format?: (value: any, item: T) => string
  render?: (value: any, item: T) => any
  hidden?: boolean
  fixed?: 'left' | 'right'
  resizable?: boolean
  minWidth?: number
  maxWidth?: number
}

/**
 * Интерфейс для сортировки
 */
export interface SortConfig {
  key: string
  direction: 'asc' | 'desc'
}

/**
 * Интерфейс для фильтра
 */
export interface FilterConfig {
  key: string
  value: any
  operator: 'equals' | 'contains' | 'startsWith' | 'endsWith' | 'greaterThan' | 'lessThan' | 'between' | 'in'
}

/**
 * Интерфейс для пагинации
 */
export interface PaginationConfig {
  page: number
  pageSize: number
  total: number
}

/**
 * Интерфейс для выбора строк
 */
export interface SelectionConfig {
  selectedKeys: Set<string | number>
  selectAll: boolean
  indeterminate: boolean
}

/**
 * Интерфейс для состояния таблицы
 */
export interface TableState<T = any> {
  data: T[]
  columns: TableColumn<T>[]
  sort: SortConfig | null
  filters: FilterConfig[]
  pagination: PaginationConfig
  selection: SelectionConfig
  loading: boolean
  error: any
  search: string
  expandedRows: Set<string | number>
}

/**
 * Класс для управления таблицами
 */
export class TableManager<T = any> {
  private state: Ref<TableState<T>>
  private originalData: T[]
  private rowKey: string | ((item: T) => string | number)

  constructor(
    data: T[],
    columns: TableColumn<T>[],
    rowKey: string | ((item: T) => string | number) = 'id'
  ) {
    this.originalData = [...data]
    this.rowKey = rowKey

    this.state = ref<TableState<T>>({
      data: [...data],
      columns,
      sort: null,
      filters: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: data.length
      },
      selection: {
        selectedKeys: new Set(),
        selectAll: false,
        indeterminate: false
      },
      loading: false,
      error: null,
      search: '',
      expandedRows: new Set()
    })
  }

  /**
   * Получает состояние таблицы
   */
  getState(): Ref<TableState<T>> {
    return this.state
  }

  /**
   * Получает обработанные данные
   */
  getProcessedData(): Ref<T[]> {
    return computed(() => {
      let data = [...this.originalData]

      // Применяем поиск
      if (this.state.value.search) {
        data = this.filterBySearch(data, this.state.value.search)
      }

      // Применяем фильтры
      if (this.state.value.filters.length > 0) {
        data = this.applyFilters(data, this.state.value.filters)
      }

      // Применяем сортировку
      if (this.state.value.sort) {
        data = this.sortData(data, this.state.value.sort)
      }

      // Обновляем общее количество
      this.state.value.pagination.total = data.length

      // Применяем пагинацию
      const { page, pageSize } = this.state.value.pagination
      const start = (page - 1) * pageSize
      const end = start + pageSize

      return data.slice(start, end)
    })
  }

  /**
   * Обновляет данные
   */
  updateData(data: T[]): void {
    this.originalData = [...data]
    this.state.value.data = [...data]
    this.state.value.pagination.total = data.length
    this.resetPagination()
  }

  /**
   * Добавляет данные
   */
  addData(data: T[]): void {
    this.originalData.push(...data)
    this.state.value.data.push(...data)
    this.state.value.pagination.total = this.originalData.length
  }

  /**
   * Удаляет данные
   */
  removeData(keys: (string | number)[]): void {
    const keySet = new Set(keys)
    this.originalData = this.originalData.filter(item => {
      const key = this.getRowKey(item)
      return !keySet.has(key)
    })
    this.state.value.data = this.originalData.filter(item => {
      const key = this.getRowKey(item)
      return !keySet.has(key)
    })
    this.state.value.pagination.total = this.originalData.length
  }

  /**
   * Обновляет одну запись
   */
  updateRow(key: string | number, updates: Partial<T>): void {
    const index = this.originalData.findIndex(item => this.getRowKey(item) === key)
    if (index !== -1) {
      this.originalData[index] = { ...this.originalData[index], ...updates }
      this.state.value.data[index] = { ...this.state.value.data[index], ...updates }
    }
  }

  /**
   * Устанавливает сортировку
   */
  setSort(key: string, direction: 'asc' | 'desc' = 'asc'): void {
    this.state.value.sort = { key, direction }
  }

  /**
   * Очищает сортировку
   */
  clearSort(): void {
    this.state.value.sort = null
  }

  /**
   * Добавляет фильтр
   */
  addFilter(filter: FilterConfig): void {
    this.state.value.filters.push(filter)
    this.resetPagination()
  }

  /**
   * Удаляет фильтр
   */
  removeFilter(key: string): void {
    this.state.value.filters = this.state.value.filters.filter(f => f.key !== key)
    this.resetPagination()
  }

  /**
   * Очищает все фильтры
   */
  clearFilters(): void {
    this.state.value.filters = []
    this.resetPagination()
  }

  /**
   * Устанавливает поиск
   */
  setSearch(search: string): void {
    this.state.value.search = search
    this.resetPagination()
  }

  /**
   * Очищает поиск
   */
  clearSearch(): void {
    this.state.value.search = ''
    this.resetPagination()
  }

  /**
   * Устанавливает страницу
   */
  setPage(page: number): void {
    this.state.value.pagination.page = Math.max(1, page)
  }

  /**
   * Устанавливает размер страницы
   */
  setPageSize(pageSize: number): void {
    this.state.value.pagination.pageSize = pageSize
    this.resetPagination()
  }

  /**
   * Сбрасывает пагинацию
   */
  resetPagination(): void {
    this.state.value.pagination.page = 1
  }

  /**
   * Выбирает строку
   */
  selectRow(key: string | number): void {
    this.state.value.selection.selectedKeys.add(key)
    this.updateSelectionState()
  }

  /**
   * Отменяет выбор строки
   */
  deselectRow(key: string | number): void {
    this.state.value.selection.selectedKeys.delete(key)
    this.updateSelectionState()
  }

  /**
   * Выбирает все строки
   */
  selectAll(): void {
    const processedData = this.getProcessedData().value
    processedData.forEach(item => {
      this.state.value.selection.selectedKeys.add(this.getRowKey(item))
    })
    this.state.value.selection.selectAll = true
    this.state.value.selection.indeterminate = false
  }

  /**
   * Отменяет выбор всех строк
   */
  deselectAll(): void {
    this.state.value.selection.selectedKeys.clear()
    this.state.value.selection.selectAll = false
    this.state.value.selection.indeterminate = false
  }

  /**
   * Переключает выбор строки
   */
  toggleRowSelection(key: string | number): void {
    if (this.state.value.selection.selectedKeys.has(key)) {
      this.deselectRow(key)
    } else {
      this.selectRow(key)
    }
  }

  /**
   * Получает выбранные строки
   */
  getSelectedRows(): T[] {
    const processedData = this.getProcessedData().value
    return processedData.filter(item => 
      this.state.value.selection.selectedKeys.has(this.getRowKey(item))
    )
  }

  /**
   * Получает ключи выбранных строк
   */
  getSelectedKeys(): (string | number)[] {
    return Array.from(this.state.value.selection.selectedKeys)
  }

  /**
   * Устанавливает состояние загрузки
   */
  setLoading(loading: boolean): void {
    this.state.value.loading = loading
  }

  /**
   * Устанавливает ошибку
   */
  setError(error: any): void {
    this.state.value.error = error
  }

  /**
   * Очищает ошибку
   */
  clearError(): void {
    this.state.value.error = null
  }

  /**
   * Разворачивает строку
   */
  expandRow(key: string | number): void {
    this.state.value.expandedRows.add(key)
  }

  /**
   * Сворачивает строку
   */
  collapseRow(key: string | number): void {
    this.state.value.expandedRows.delete(key)
  }

  /**
   * Переключает развертывание строки
   */
  toggleRowExpansion(key: string | number): void {
    if (this.state.value.expandedRows.has(key)) {
      this.collapseRow(key)
    } else {
      this.expandRow(key)
    }
  }

  /**
   * Получает развернутые строки
   */
  getExpandedRows(): (string | number)[] {
    return Array.from(this.state.value.expandedRows)
  }

  /**
   * Сворачивает все строки
   */
  collapseAll(): void {
    this.state.value.expandedRows.clear()
  }

  /**
   * Разворачивает все строки
   */
  expandAll(): void {
    const processedData = this.getProcessedData().value
    processedData.forEach(item => {
      this.state.value.expandedRows.add(this.getRowKey(item))
    })
  }

  /**
   * Сбрасывает состояние таблицы
   */
  reset(): void {
    this.state.value = {
      ...this.state.value,
      sort: null,
      filters: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: this.originalData.length
      },
      selection: {
        selectedKeys: new Set(),
        selectAll: false,
        indeterminate: false
      },
      loading: false,
      error: null,
      search: '',
      expandedRows: new Set()
    }
  }

  /**
   * Экспортирует данные
   */
  exportData(format: 'csv' | 'json' | 'excel' = 'csv'): string | Blob {
    const data = this.getProcessedData().value

    switch (format) {
      case 'csv':
        return this.exportToCSV(data)
      case 'json':
        return JSON.stringify(data, null, 2)
      case 'excel':
        return this.exportToExcel(data)
      default:
        throw new Error(`Unsupported export format: ${format}`)
    }
  }

  /**
   * Получает статистику таблицы
   */
  getStats(): Record<string, any> {
    const processedData = this.getProcessedData().value
    const totalData = this.originalData.length

    return {
      totalRows: totalData,
      visibleRows: processedData.length,
      selectedRows: this.state.value.selection.selectedKeys.size,
      expandedRows: this.state.value.expandedRows.size,
      currentPage: this.state.value.pagination.page,
      totalPages: Math.ceil(this.state.value.pagination.total / this.state.value.pagination.pageSize),
      hasFilters: this.state.value.filters.length > 0,
      hasSearch: !!this.state.value.search,
      hasSort: !!this.state.value.sort,
      isLoading: this.state.value.loading,
      hasError: !!this.state.value.error
    }
  }

  /**
   * Приватные методы
   */
  private getRowKey(item: T): string | number {
    if (typeof this.rowKey === 'function') {
      return this.rowKey(item)
    }
    return (item as any)[this.rowKey]
  }

  private filterBySearch(data: T[], search: string): T[] {
    const searchLower = search.toLowerCase()
    return data.filter(item => {
      return this.state.value.columns.some(column => {
        if (column.field) {
          const value = typeof column.field === 'function' 
            ? column.field(item) 
            : (item as any)[column.field]
          return String(value).toLowerCase().includes(searchLower)
        }
        return false
      })
    })
  }

  private applyFilters(data: T[], filters: FilterConfig[]): T[] {
    return data.filter(item => {
      return filters.every(filter => {
        const value = this.getValueByKey(item, filter.key)
        return this.matchesFilter(value, filter)
      })
    })
  }

  private getValueByKey(item: T, key: string): any {
    const column = this.state.value.columns.find(col => col.key === key)
    if (column?.field) {
      return typeof column.field === 'function' 
        ? column.field(item) 
        : (item as any)[column.field]
    }
    return (item as any)[key]
  }

  private matchesFilter(value: any, filter: FilterConfig): boolean {
    switch (filter.operator) {
      case 'equals':
        return value === filter.value
      case 'contains':
        return String(value).includes(String(filter.value))
      case 'startsWith':
        return String(value).startsWith(String(filter.value))
      case 'endsWith':
        return String(value).endsWith(String(filter.value))
      case 'greaterThan':
        return value > filter.value
      case 'lessThan':
        return value < filter.value
      case 'between':
        return value >= filter.value[0] && value <= filter.value[1]
      case 'in':
        return Array.isArray(filter.value) && filter.value.includes(value)
      default:
        return true
    }
  }

  private sortData(data: T[], sort: SortConfig): T[] {
    return [...data].sort((a, b) => {
      const aValue = this.getValueByKey(a, sort.key)
      const bValue = this.getValueByKey(b, sort.key)

      if (aValue < bValue) return sort.direction === 'asc' ? -1 : 1
      if (aValue > bValue) return sort.direction === 'asc' ? 1 : -1
      return 0
    })
  }

  private updateSelectionState(): void {
    const processedData = this.getProcessedData().value
    const selectedCount = this.state.value.selection.selectedKeys.size
    const totalCount = processedData.length

    if (selectedCount === 0) {
      this.state.value.selection.selectAll = false
      this.state.value.selection.indeterminate = false
    } else if (selectedCount === totalCount) {
      this.state.value.selection.selectAll = true
      this.state.value.selection.indeterminate = false
    } else {
      this.state.value.selection.selectAll = false
      this.state.value.selection.indeterminate = true
    }
  }

  private exportToCSV(data: T[]): string {
    const headers = this.state.value.columns
      .filter(col => !col.hidden)
      .map(col => col.label)
      .join(',')

    const rows = data.map(item => {
      return this.state.value.columns
        .filter(col => !col.hidden)
        .map(col => {
          const value = col.field 
            ? (typeof col.field === 'function' ? col.field(item) : (item as any)[col.field])
            : (item as any)[col.key]
          return `"${String(value).replace(/"/g, '""')}"`
        })
        .join(',')
    }).join('\n')

    return `${headers}\n${rows}`
  }

  private exportToExcel(data: T[]): Blob {
    // Простая реализация - в реальном проекте используйте библиотеку типа xlsx
    const csv = this.exportToCSV(data)
    return new Blob([csv], { type: 'text/csv' })
  }
}

/**
 * Хук для использования менеджера таблиц в Vue компонентах
 */
export function useTableManager<T = any>(
  data: T[],
  columns: TableColumn<T>[],
  rowKey?: string | ((item: T) => string | number)
) {
  const manager = new TableManager(data, columns, rowKey)

  return {
    state: manager.getState(),
    processedData: manager.getProcessedData(),
    updateData: manager.updateData.bind(manager),
    addData: manager.addData.bind(manager),
    removeData: manager.removeData.bind(manager),
    updateRow: manager.updateRow.bind(manager),
    setSort: manager.setSort.bind(manager),
    clearSort: manager.clearSort.bind(manager),
    addFilter: manager.addFilter.bind(manager),
    removeFilter: manager.removeFilter.bind(manager),
    clearFilters: manager.clearFilters.bind(manager),
    setSearch: manager.setSearch.bind(manager),
    clearSearch: manager.clearSearch.bind(manager),
    setPage: manager.setPage.bind(manager),
    setPageSize: manager.setPageSize.bind(manager),
    resetPagination: manager.resetPagination.bind(manager),
    selectRow: manager.selectRow.bind(manager),
    deselectRow: manager.deselectRow.bind(manager),
    selectAll: manager.selectAll.bind(manager),
    deselectAll: manager.deselectAll.bind(manager),
    toggleRowSelection: manager.toggleRowSelection.bind(manager),
    getSelectedRows: manager.getSelectedRows.bind(manager),
    getSelectedKeys: manager.getSelectedKeys.bind(manager),
    setLoading: manager.setLoading.bind(manager),
    setError: manager.setError.bind(manager),
    clearError: manager.clearError.bind(manager),
    expandRow: manager.expandRow.bind(manager),
    collapseRow: manager.collapseRow.bind(manager),
    toggleRowExpansion: manager.toggleRowExpansion.bind(manager),
    getExpandedRows: manager.getExpandedRows.bind(manager),
    collapseAll: manager.collapseAll.bind(manager),
    expandAll: manager.expandAll.bind(manager),
    reset: manager.reset.bind(manager),
    exportData: manager.exportData.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}
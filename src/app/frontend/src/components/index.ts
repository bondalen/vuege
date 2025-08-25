// Экспорт всех компонентов

export { default as VuegeLayout } from './VuegeLayout.vue'
export { default as VuegeMap } from './VuegeMap.vue'
export { default as VuegeTable } from './VuegeTable.vue'
export { default as VuegeForm } from './VuegeForm.vue'
export { default as VuegeModal } from './VuegeModal.vue'
export { default as VuegeCard } from './VuegeCard.vue'

// Типы для компонентов
export interface TableColumn {
  name: string
  label: string
  field: string
  sortable?: boolean
  filterable?: boolean
  align?: 'left' | 'center' | 'right'
  format?: (value: any) => string
  style?: Record<string, any>
  classes?: string
}

export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'checkbox' | 'radio' | 'date' | 'file'
  value?: any
  required?: boolean
  validation?: any[]
  options?: Array<{ label: string; value: any }>
  placeholder?: string
  help?: string
}

export interface ModalConfig {
  title?: string
  subtitle?: string
  persistent?: boolean
  maximized?: boolean
  fullHeight?: boolean
  fullWidth?: boolean
  showClose?: boolean
  showCancel?: boolean
  showConfirm?: boolean
  cancelLabel?: string
  confirmLabel?: string
  cancelColor?: string
  confirmColor?: string
}

export interface CardConfig {
  title?: string
  subtitle?: string
  image?: string
  imageAlt?: string
  flat?: boolean
  bordered?: boolean
  clickable?: boolean
  showMenu?: boolean
}
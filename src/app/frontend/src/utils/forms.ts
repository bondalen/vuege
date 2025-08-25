// Утилиты для работы с формами

import { ref, reactive, computed, watch, Ref } from 'vue'

/**
 * Интерфейс для поля формы
 */
export interface FormField<T = any> {
  value: T
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'checkbox' | 'radio' | 'date' | 'file' | 'custom'
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  placeholder?: string
  help?: string
  error?: string
  validation?: FormValidation[]
  options?: FormOption[]
  multiple?: boolean
  min?: number
  max?: number
  step?: number
  pattern?: string
  autocomplete?: string
  rows?: number
  cols?: number
  accept?: string
  maxSize?: number
  customComponent?: any
  customProps?: Record<string, any>
}

/**
 * Интерфейс для валидации
 */
export interface FormValidation {
  type: 'required' | 'min' | 'max' | 'minLength' | 'maxLength' | 'pattern' | 'email' | 'url' | 'custom'
  message: string
  value?: any
  validator?: (value: any) => boolean | string
}

/**
 * Интерфейс для опции
 */
export interface FormOption {
  value: any
  label: string
  disabled?: boolean
  group?: string
}

/**
 * Интерфейс для состояния формы
 */
export interface FormState<T = Record<string, any>> {
  values: T
  errors: Record<string, string>
  touched: Record<string, boolean>
  dirty: Record<string, boolean>
  loading: boolean
  submitted: boolean
  valid: boolean
}

/**
 * Класс для управления формами
 */
export class FormManager<T = Record<string, any>> {
  private fields: Map<string, FormField>
  private state: Ref<FormState<T>>
  private initialValues: T
  private validators: Map<string, FormValidation[]>

  constructor(initialValues: T, fields?: FormField[]) {
    this.fields = new Map()
    this.validators = new Map()
    this.initialValues = { ...initialValues }

    this.state = ref<FormState<T>>({
      values: { ...initialValues },
      errors: {},
      touched: {},
      dirty: {},
      loading: false,
      submitted: false,
      valid: true
    })

    if (fields) {
      fields.forEach(field => this.addField(field))
    }
  }

  /**
   * Добавляет поле в форму
   */
  addField(name: string, field: FormField): void {
    this.fields.set(name, field)
    
    if (field.validation) {
      this.validators.set(name, field.validation)
    }

    // Инициализируем значение
    if (!(name in this.state.value.values)) {
      (this.state.value.values as any)[name] = field.value
    }
  }

  /**
   * Получает поле формы
   */
  getField(name: string): FormField | undefined {
    return this.fields.get(name)
  }

  /**
   * Обновляет поле формы
   */
  updateField(name: string, updates: Partial<FormField>): void {
    const field = this.fields.get(name)
    if (field) {
      Object.assign(field, updates)
      
      if (updates.validation) {
        this.validators.set(name, updates.validation)
      }
    }
  }

  /**
   * Удаляет поле формы
   */
  removeField(name: string): boolean {
    this.validators.delete(name)
    return this.fields.delete(name)
  }

  /**
   * Получает состояние формы
   */
  getState(): Ref<FormState<T>> {
    return this.state
  }

  /**
   * Получает значения формы
   */
  getValues(): T {
    return { ...this.state.value.values }
  }

  /**
   * Устанавливает значения формы
   */
  setValues(values: Partial<T>): void {
    Object.assign(this.state.value.values, values)
    this.markAsDirty()
  }

  /**
   * Устанавливает значение поля
   */
  setValue(name: string, value: any): void {
    (this.state.value.values as any)[name] = value
    this.markFieldAsDirty(name)
    this.validateField(name)
  }

  /**
   * Получает значение поля
   */
  getValue(name: string): any {
    return (this.state.value.values as any)[name]
  }

  /**
   * Сбрасывает форму к начальным значениям
   */
  reset(): void {
    this.state.value.values = { ...this.initialValues }
    this.state.value.errors = {}
    this.state.value.touched = {}
    this.state.value.dirty = {}
    this.state.value.submitted = false
  }

  /**
   * Очищает форму
   */
  clear(): void {
    const emptyValues: any = {}
    this.fields.forEach((field, name) => {
      emptyValues[name] = this.getEmptyValue(field)
    })
    
    this.state.value.values = emptyValues
    this.state.value.errors = {}
    this.state.value.touched = {}
    this.state.value.dirty = {}
    this.state.value.submitted = false
  }

  /**
   * Отмечает поле как "тронутое"
   */
  markFieldAsTouched(name: string): void {
    this.state.value.touched[name] = true
  }

  /**
   * Отмечает поле как "грязное"
   */
  markFieldAsDirty(name: string): void {
    this.state.value.dirty[name] = true
  }

  /**
   * Отмечает форму как "грязную"
   */
  markAsDirty(): void {
    Object.keys(this.fields).forEach(name => {
      this.state.value.dirty[name] = true
    })
  }

  /**
   * Проверяет, тронуто ли поле
   */
  isFieldTouched(name: string): boolean {
    return !!this.state.value.touched[name]
  }

  /**
   * Проверяет, грязное ли поле
   */
  isFieldDirty(name: string): boolean {
    return !!this.state.value.dirty[name]
  }

  /**
   * Проверяет, грязная ли форма
   */
  isDirty(): boolean {
    return Object.values(this.state.value.dirty).some(Boolean)
  }

  /**
   * Валидирует поле
   */
  validateField(name: string): string | null {
    const field = this.fields.get(name)
    const value = this.getValue(name)
    const validations = this.validators.get(name) || []

    for (const validation of validations) {
      const error = this.validateValue(value, validation, field)
      if (error) {
        this.state.value.errors[name] = error
        return error
      }
    }

    delete this.state.value.errors[name]
    return null
  }

  /**
   * Валидирует всю форму
   */
  validate(): boolean {
    const errors: Record<string, string> = {}
    let isValid = true

    this.fields.forEach((field, name) => {
      const value = this.getValue(name)
      const validations = this.validators.get(name) || []

      for (const validation of validations) {
        const error = this.validateValue(value, validation, field)
        if (error) {
          errors[name] = error
          isValid = false
          break
        }
      }
    })

    this.state.value.errors = errors
    this.state.value.valid = isValid
    return isValid
  }

  /**
   * Получает ошибки формы
   */
  getErrors(): Record<string, string> {
    return { ...this.state.value.errors }
  }

  /**
   * Получает ошибку поля
   */
  getFieldError(name: string): string | undefined {
    return this.state.value.errors[name]
  }

  /**
   * Устанавливает ошибку поля
   */
  setFieldError(name: string, error: string): void {
    this.state.value.errors[name] = error
    this.state.value.valid = false
  }

  /**
   * Очищает ошибку поля
   */
  clearFieldError(name: string): void {
    delete this.state.value.errors[name]
    this.updateFormValidity()
  }

  /**
   * Очищает все ошибки
   */
  clearErrors(): void {
    this.state.value.errors = {}
    this.state.value.valid = true
  }

  /**
   * Устанавливает состояние загрузки
   */
  setLoading(loading: boolean): void {
    this.state.value.loading = loading
  }

  /**
   * Отмечает форму как отправленную
   */
  markAsSubmitted(): void {
    this.state.value.submitted = true
  }

  /**
   * Отправляет форму
   */
  async submit(onSubmit?: (values: T) => Promise<void> | void): Promise<boolean> {
    this.setLoading(true)
    this.clearErrors()

    try {
      // Валидируем форму
      if (!this.validate()) {
        return false
      }

      // Отмечаем все поля как тронутые
      this.fields.forEach((_, name) => {
        this.markFieldAsTouched(name)
      })

      // Вызываем обработчик отправки
      if (onSubmit) {
        await onSubmit(this.getValues())
      }

      this.markAsSubmitted()
      return true
    } catch (error) {
      console.error('Form submission error:', error)
      return false
    } finally {
      this.setLoading(false)
    }
  }

  /**
   * Получает данные формы для отправки
   */
  getFormData(): FormData {
    const formData = new FormData()
    
    this.fields.forEach((field, name) => {
      const value = this.getValue(name)
      
      if (field.type === 'file' && value instanceof File) {
        formData.append(name, value)
      } else if (field.multiple && Array.isArray(value)) {
        value.forEach(item => formData.append(name, String(item)))
      } else {
        formData.append(name, String(value))
      }
    })

    return formData
  }

  /**
   * Получает JSON данные формы
   */
  getJsonData(): string {
    return JSON.stringify(this.getValues())
  }

  /**
   * Клонирует форму
   */
  clone(): FormManager<T> {
    const cloned = new FormManager<T>(this.getValues())
    
    this.fields.forEach((field, name) => {
      cloned.addField(name, { ...field })
    })

    return cloned
  }

  /**
   * Экспортирует состояние формы
   */
  export(): Record<string, any> {
    return {
      values: this.getValues(),
      errors: this.getErrors(),
      touched: { ...this.state.value.touched },
      dirty: { ...this.state.value.dirty },
      submitted: this.state.value.submitted,
      valid: this.state.value.valid
    }
  }

  /**
   * Импортирует состояние формы
   */
  import(data: Record<string, any>): void {
    if (data.values) {
      this.setValues(data.values)
    }
    if (data.errors) {
      this.state.value.errors = { ...data.errors }
    }
    if (data.touched) {
      this.state.value.touched = { ...data.touched }
    }
    if (data.dirty) {
      this.state.value.dirty = { ...data.dirty }
    }
    if (data.submitted !== undefined) {
      this.state.value.submitted = data.submitted
    }
    if (data.valid !== undefined) {
      this.state.value.valid = data.valid
    }
  }

  /**
   * Получает статистику формы
   */
  getStats(): Record<string, any> {
    const totalFields = this.fields.size
    const errorFields = Object.keys(this.state.value.errors).length
    const touchedFields = Object.values(this.state.value.touched).filter(Boolean).length
    const dirtyFields = Object.values(this.state.value.dirty).filter(Boolean).length

    return {
      totalFields,
      errorFields,
      touchedFields,
      dirtyFields,
      validFields: totalFields - errorFields,
      untouchedFields: totalFields - touchedFields,
      cleanFields: totalFields - dirtyFields,
      isValid: this.state.value.valid,
      isDirty: this.isDirty(),
      isSubmitted: this.state.value.submitted,
      isLoading: this.state.value.loading
    }
  }

  /**
   * Приватные методы
   */
  private validateValue(value: any, validation: FormValidation, field?: FormField): string | null {
    switch (validation.type) {
      case 'required':
        if (!value || (typeof value === 'string' && value.trim() === '')) {
          return validation.message
        }
        break

      case 'min':
        if (typeof value === 'number' && value < validation.value) {
          return validation.message
        }
        break

      case 'max':
        if (typeof value === 'number' && value > validation.value) {
          return validation.message
        }
        break

      case 'minLength':
        if (typeof value === 'string' && value.length < validation.value) {
          return validation.message
        }
        break

      case 'maxLength':
        if (typeof value === 'string' && value.length > validation.value) {
          return validation.message
        }
        break

      case 'pattern':
        if (typeof value === 'string' && !new RegExp(validation.value).test(value)) {
          return validation.message
        }
        break

      case 'email':
        if (typeof value === 'string' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return validation.message
        }
        break

      case 'url':
        if (typeof value === 'string' && !/^https?:\/\/.+/.test(value)) {
          return validation.message
        }
        break

      case 'custom':
        if (validation.validator) {
          const result = validation.validator(value)
          if (result !== true) {
            return typeof result === 'string' ? result : validation.message
          }
        }
        break
    }

    return null
  }

  private getEmptyValue(field: FormField): any {
    switch (field.type) {
      case 'checkbox':
        return false
      case 'select':
        return field.multiple ? [] : ''
      case 'number':
        return 0
      case 'file':
        return null
      default:
        return ''
    }
  }

  private updateFormValidity(): void {
    this.state.value.valid = Object.keys(this.state.value.errors).length === 0
  }
}

/**
 * Хук для использования менеджера форм в Vue компонентах
 */
export function useFormManager<T = Record<string, any>>(
  initialValues: T,
  fields?: FormField[]
) {
  const manager = new FormManager(initialValues, fields)

  return {
    state: manager.getState(),
    getValues: manager.getValues.bind(manager),
    setValues: manager.setValues.bind(manager),
    setValue: manager.setValue.bind(manager),
    getValue: manager.getValue.bind(manager),
    reset: manager.reset.bind(manager),
    clear: manager.clear.bind(manager),
    markFieldAsTouched: manager.markFieldAsTouched.bind(manager),
    markFieldAsDirty: manager.markFieldAsDirty.bind(manager),
    markAsDirty: manager.markAsDirty.bind(manager),
    isFieldTouched: manager.isFieldTouched.bind(manager),
    isFieldDirty: manager.isFieldDirty.bind(manager),
    isDirty: manager.isDirty.bind(manager),
    validateField: manager.validateField.bind(manager),
    validate: manager.validate.bind(manager),
    getErrors: manager.getErrors.bind(manager),
    getFieldError: manager.getFieldError.bind(manager),
    setFieldError: manager.setFieldError.bind(manager),
    clearFieldError: manager.clearFieldError.bind(manager),
    clearErrors: manager.clearErrors.bind(manager),
    setLoading: manager.setLoading.bind(manager),
    markAsSubmitted: manager.markAsSubmitted.bind(manager),
    submit: manager.submit.bind(manager),
    getFormData: manager.getFormData.bind(manager),
    getJsonData: manager.getJsonData.bind(manager),
    clone: manager.clone.bind(manager),
    export: manager.export.bind(manager),
    import: manager.import.bind(manager),
    getStats: manager.getStats.bind(manager),
    addField: manager.addField.bind(manager),
    getField: manager.getField.bind(manager),
    updateField: manager.updateField.bind(manager),
    removeField: manager.removeField.bind(manager)
  }
}
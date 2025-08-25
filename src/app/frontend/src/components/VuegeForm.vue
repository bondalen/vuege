<template>
  <div class="vuege-form">
    <q-form @submit="onSubmit" @reset="onReset">
      <!-- Заголовок формы -->
      <div v-if="title || $slots.header" class="form-header q-mb-lg">
        <h5 v-if="title" class="text-h5 q-mb-xs">{{ title }}</h5>
        <p v-if="subtitle" class="text-body2 text-grey-7">{{ subtitle }}</p>
        <slot name="header" />
      </div>

      <!-- Поля формы -->
      <div class="form-fields">
        <slot />
      </div>

      <!-- Ошибки формы -->
      <div v-if="hasErrors" class="form-errors q-mt-md">
        <q-banner class="bg-negative text-white">
          <template v-slot:avatar>
            <q-icon name="error" />
          </template>
          <div class="text-body2">
            <div v-for="(error, field) in errors" :key="field" class="q-mb-xs">
              <strong>{{ getFieldLabel(field) }}:</strong> {{ error }}
            </div>
          </div>
        </q-banner>
      </div>

      <!-- Действия формы -->
      <div class="form-actions q-mt-lg">
        <div class="row justify-end q-gutter-md">
          <slot name="actions">
            <q-btn
              v-if="showReset"
              label="Сбросить"
              color="secondary"
              flat
              type="reset"
              :disable="loading"
            />
            <q-btn
              :label="submitLabel"
              :color="submitColor"
              :icon="submitIcon"
              :loading="loading"
              type="submit"
            />
          </slot>
        </div>
      </div>
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFormManager } from '@/utils'

// Пропсы
interface Props {
  title?: string
  subtitle?: string
  loading?: boolean
  errors?: Record<string, string>
  showReset?: boolean
  submitLabel?: string
  submitColor?: string
  submitIcon?: string
  validateOnSubmit?: boolean
  autoSave?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  errors: () => ({}),
  showReset: true,
  submitLabel: 'Сохранить',
  submitColor: 'primary',
  submitIcon: 'save',
  validateOnSubmit: true,
  autoSave: false
})

// Эмиты
const emit = defineEmits<{
  submit: [data: any]
  reset: []
  validation: [valid: boolean]
  fieldChange: [field: string, value: any]
}>()

// Вычисляемые свойства
const hasErrors = computed(() => {
  return Object.keys(props.errors).length > 0
})

// Методы
const onSubmit = (data: any) => {
  if (props.validateOnSubmit) {
    // Валидация формы
    const isValid = validateForm(data)
    emit('validation', isValid)
    
    if (!isValid) {
      return
    }
  }
  
  emit('submit', data)
}

const onReset = () => {
  emit('reset')
}

const validateForm = (data: any): boolean => {
  // Базовая валидация
  return true
}

const getFieldLabel = (field: string): string => {
  // Получение метки поля
  return field.charAt(0).toUpperCase() + field.slice(1)
}
</script>

<style scoped>
.vuege-form {
  width: 100%;
}

.form-header {
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-errors {
  border-radius: 8px;
  overflow: hidden;
}

.form-actions {
  border-top: 1px solid #e0e0e0;
  padding-top: 1rem;
}
</style>
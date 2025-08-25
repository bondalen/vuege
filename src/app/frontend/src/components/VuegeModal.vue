<template>
  <q-dialog
    v-model="isVisible"
    :persistent="persistent"
    :maximized="maximized"
    :full-height="fullHeight"
    :full-width="fullWidth"
    :position="position"
    :transition-show="transitionShow"
    :transition-hide="transitionHide"
    @hide="onHide"
  >
    <q-card :style="cardStyle" :class="cardClass">
      <!-- Заголовок -->
      <q-card-section v-if="title || $slots.header" class="modal-header">
        <div class="row items-center justify-between">
          <div class="col">
            <h5 v-if="title" class="text-h5 q-mb-xs">{{ title }}</h5>
            <p v-if="subtitle" class="text-body2 text-grey-7">{{ subtitle }}</p>
            <slot name="header" />
          </div>
          <div class="col-auto">
            <slot name="header-actions" />
            <q-btn
              v-if="showClose"
              flat
              round
              dense
              icon="close"
              @click="close"
            />
          </div>
        </div>
      </q-card-section>

      <!-- Содержимое -->
      <q-card-section class="modal-content">
        <slot />
      </q-card-section>

      <!-- Действия -->
      <q-card-actions v-if="$slots.actions || showDefaultActions" class="modal-actions">
        <slot name="actions">
          <q-btn
            v-if="showCancel"
            :label="cancelLabel"
            :color="cancelColor"
            :icon="cancelIcon"
            flat
            @click="cancel"
          />
          <q-btn
            v-if="showConfirm"
            :label="confirmLabel"
            :color="confirmColor"
            :icon="confirmIcon"
            :loading="loading"
            @click="confirm"
          />
        </slot>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useModalManager } from '@/utils'

// Пропсы
interface Props {
  modelValue: boolean
  title?: string
  subtitle?: string
  persistent?: boolean
  maximized?: boolean
  fullHeight?: boolean
  fullWidth?: boolean
  position?: string
  transitionShow?: string
  transitionHide?: string
  showClose?: boolean
  showCancel?: boolean
  showConfirm?: boolean
  cancelLabel?: string
  confirmLabel?: string
  cancelColor?: string
  confirmColor?: string
  cancelIcon?: string
  confirmIcon?: string
  loading?: boolean
  size?: string
  cardStyle?: Record<string, any>
  cardClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  persistent: false,
  maximized: false,
  fullHeight: false,
  fullWidth: false,
  position: 'standard',
  transitionShow: 'fade',
  transitionHide: 'fade',
  showClose: true,
  showCancel: true,
  showConfirm: true,
  cancelLabel: 'Отмена',
  confirmLabel: 'Подтвердить',
  cancelColor: 'grey',
  confirmColor: 'primary',
  cancelIcon: 'close',
  confirmIcon: 'check',
  loading: false,
  size: 'md',
  cardStyle: () => ({}),
  cardClass: ''
})

// Эмиты
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
  cancel: []
  hide: []
}>()

// Состояние
const isVisible = ref(props.modelValue)

// Вычисляемые свойства
const showDefaultActions = computed(() => {
  return props.showCancel || props.showConfirm
})

// Методы
const close = () => {
  isVisible.value = false
  emit('update:modelValue', false)
}

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
  close()
}

const onHide = () => {
  emit('hide')
}

// Наблюдатели
watch(() => props.modelValue, (value) => {
  isVisible.value = value
})

watch(isVisible, (value) => {
  emit('update:modelValue', value)
})
</script>

<style scoped>
.modal-header {
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.modal-content {
  max-height: 70vh;
  overflow-y: auto;
}

.modal-actions {
  border-top: 1px solid #e0e0e0;
  padding-top: 1rem;
  justify-content: flex-end;
}
</style>
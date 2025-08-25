<template>
  <q-card 
    :class="cardClass" 
    :style="cardStyle"
    :flat="flat"
    :bordered="bordered"
    :square="square"
    :clickable="clickable"
    @click="onClick"
  >
    <!-- Изображение -->
    <q-img
      v-if="image"
      :src="image"
      :alt="imageAlt"
      :ratio="imageRatio"
      :spinner-color="spinnerColor"
      :spinner-size="spinnerSize"
    >
      <template v-slot:loading>
        <q-skeleton type="rect" />
      </template>
    </q-img>

    <!-- Заголовок -->
    <q-card-section v-if="title || $slots.header" class="card-header">
      <div class="row items-center justify-between">
        <div class="col">
          <h6 v-if="title" class="text-h6 q-mb-xs">{{ title }}</h6>
          <p v-if="subtitle" class="text-body2 text-grey-7">{{ subtitle }}</p>
          <slot name="header" />
        </div>
        <div class="col-auto">
          <slot name="header-actions" />
          <q-btn
            v-if="showMenu"
            flat
            round
            dense
            icon="more_vert"
            @click="showMenuDialog = true"
          />
        </div>
      </div>
    </q-card-section>

    <!-- Содержимое -->
    <q-card-section v-if="$slots.default" class="card-content">
      <slot />
    </q-card-section>

    <!-- Действия -->
    <q-card-actions v-if="$slots.actions" class="card-actions">
      <slot name="actions" />
    </q-card-actions>

    <!-- Меню -->
    <q-menu v-if="showMenu" v-model="showMenuDialog">
      <q-list style="min-width: 150px">
        <slot name="menu" />
      </q-list>
    </q-menu>
  </q-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Пропсы
interface Props {
  title?: string
  subtitle?: string
  image?: string
  imageAlt?: string
  imageRatio?: number
  flat?: boolean
  bordered?: boolean
  square?: boolean
  clickable?: boolean
  showMenu?: boolean
  spinnerColor?: string
  spinnerSize?: string
  cardClass?: string
  cardStyle?: Record<string, any>
}

const props = withDefaults(defineProps<Props>(), {
  flat: false,
  bordered: true,
  square: false,
  clickable: false,
  showMenu: false,
  imageRatio: 16/9,
  spinnerColor: 'primary',
  spinnerSize: '50px',
  cardClass: '',
  cardStyle: () => ({})
})

// Эмиты
const emit = defineEmits<{
  click: [event: Event]
}>()

// Состояние
const showMenuDialog = ref(false)

// Методы
const onClick = (event: Event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.card-header {
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.card-content {
  padding: 1rem;
}

.card-actions {
  border-top: 1px solid #e0e0e0;
  padding-top: 1rem;
  justify-content: flex-end;
}
</style>
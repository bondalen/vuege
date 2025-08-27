<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Тест отключения виртуального скроллинга</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 1: Без виртуального скроллинга</h6>
        <q-select
          v-model="selected"
          :options="options"
          label="Выберите тип"
          outlined
          :virtual-scroll="false"
        />
        <p>Выбранное: {{ selected }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 2: С принудительным отключением</h6>
        <q-select
          v-model="selected2"
          :options="options"
          label="Выберите тип"
          outlined
          :virtual-scroll="false"
          :virtual-scroll-item-size="0"
        />
        <p>Выбранное: {{ selected2 }}</p>
      </div>
      
      <div class="col-12">
        <h6>Отладочная информация</h6>
        <pre>{{ debugInfo }}</pre>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const options = [
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
]

const selected = ref(null)
const selected2 = ref(null)

const debugInfo = computed(() => ({
  options,
  selected: selected.value,
  selected2: selected2.value
}))

console.log('VirtualScrollTestPage - options:', options)
</script>
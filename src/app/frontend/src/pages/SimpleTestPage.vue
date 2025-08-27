<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Простой тест q-select</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест q-select с объектами</h6>
        <q-select
          v-model="selectedValue"
          :options="options"
          label="Выберите тип"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          emit-value
          map-options
        />
        <p>Выбранное значение: {{ selectedValue }}</p>
        <p>Тип значения: {{ typeof selectedValue }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест q-select без emit-value</h6>
        <q-select
          v-model="selectedValue2"
          :options="options"
          label="Выберите тип (без emit-value)"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          map-options
        />
        <p>Выбранное значение: {{ selectedValue2 }}</p>
        <p>Тип значения: {{ typeof selectedValue2 }}</p>
      </div>
    </div>
    
    <div class="row q-mt-lg">
      <div class="col-12">
        <q-card>
          <q-card-section>
            <h6>Отладочная информация</h6>
            <pre>{{ debugInfo }}</pre>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const options = ref([
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
])

const selectedValue = ref('GOVERNMENT')
const selectedValue2 = ref('GOVERNMENT')

const debugInfo = computed(() => ({
  options: options.value,
  selectedValue: selectedValue.value,
  selectedValue2: selectedValue2.value,
  selectedValueType: typeof selectedValue.value,
  selectedValue2Type: typeof selectedValue2.value
}))

console.log('SimpleTestPage - options:', options.value)
console.log('SimpleTestPage - selectedValue:', selectedValue.value)
</script>
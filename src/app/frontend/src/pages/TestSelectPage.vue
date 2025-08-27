<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Тест q-select компонента</h4>
      </div>
      
      <!-- Тест 1: Простой q-select -->
      <div class="col-12 col-md-6">
        <h6>Тест 1: Простой q-select</h6>
        <q-select
          v-model="selectedValue1"
          :options="options1"
          label="Простой select"
          outlined
          class="q-mb-md"
        />
        <p>Выбранное значение: {{ selectedValue1 }}</p>
      </div>
      
      <!-- Тест 2: q-select с option-value и option-label -->
      <div class="col-12 col-md-6">
        <h6>Тест 2: С option-value и option-label</h6>
        <q-select
          v-model="selectedValue2"
          :options="options2"
          label="С option-value и option-label"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
        />
        <p>Выбранное значение: {{ selectedValue2 }}</p>
      </div>
      
      <!-- Тест 3: q-select с emit-value и map-options -->
      <div class="col-12 col-md-6">
        <h6>Тест 3: С emit-value и map-options</h6>
        <q-select
          v-model="selectedValue3"
          :options="options2"
          label="С emit-value и map-options"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          emit-value
          map-options
        />
        <p>Выбранное значение: {{ selectedValue3 }}</p>
      </div>
      
      <!-- Тест 4: q-select с use-value и fill-input -->
      <div class="col-12 col-md-6">
        <h6>Тест 4: С use-value и fill-input</h6>
        <q-select
          v-model="selectedValue4"
          :options="options2"
          label="С use-value и fill-input"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          use-value
          fill-input
        />
        <p>Выбранное значение: {{ selectedValue4 }}</p>
      </div>
      
      <!-- Тест 5: Реактивный массив -->
      <div class="col-12 col-md-6">
        <h6>Тест 5: Реактивный массив</h6>
        <q-select
          v-model="selectedValue5"
          :options="reactiveOptions"
          label="Реактивный массив"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
        />
        <p>Выбранное значение: {{ selectedValue5 }}</p>
      </div>
      
      <!-- Тест 6: Оригинальный stateTypes -->
      <div class="col-12 col-md-6">
        <h6>Тест 6: Оригинальный stateTypes</h6>
        <q-select
          v-model="selectedValue6"
          :options="stateTypes"
          label="Оригинальный stateTypes"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
        />
        <p>Выбранное значение: {{ selectedValue6 }}</p>
      </div>
    </div>
    
    <!-- Отладочная информация -->
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

// Простые опции
const options1 = ['Государство', 'Правительство', 'Коммерческая', 'Империя']

// Объектные опции
const options2 = [
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
]

// Реактивный массив
const reactiveOptions = ref([
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
])

// Оригинальный stateTypes
const stateTypes = [
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
]

// Выбранные значения
const selectedValue1 = ref('')
const selectedValue2 = ref('')
const selectedValue3 = ref('')
const selectedValue4 = ref('')
const selectedValue5 = ref('')
const selectedValue6 = ref('GOVERNMENT')

// Отладочная информация
const debugInfo = computed(() => ({
  options1: options1,
  options2: options2,
  reactiveOptions: reactiveOptions.value,
  stateTypes: stateTypes,
  selectedValues: {
    test1: selectedValue1.value,
    test2: selectedValue2.value,
    test3: selectedValue3.value,
    test4: selectedValue4.value,
    test5: selectedValue5.value,
    test6: selectedValue6.value
  }
}))

console.log('TestSelectPage - options1:', options1)
console.log('TestSelectPage - options2:', options2)
console.log('TestSelectPage - reactiveOptions:', reactiveOptions.value)
console.log('TestSelectPage - stateTypes:', stateTypes)
</script>
<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Тест q-select с простыми строками</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 1: Простые строки</h6>
        <q-select
          v-model="selectedValue1"
          :options="simpleOptions"
          label="Тип государства"
          outlined
          class="q-mb-md"
          clearable
        />
        <p>Выбранное значение: {{ selectedValue1 }}</p>
        <p>Тип: {{ typeof selectedValue1 }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 2: Объекты с label/value</h6>
        <q-select
          v-model="selectedValue2"
          :options="objectOptions"
          label="Тип государства"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          clearable
        />
        <p>Выбранное значение: {{ selectedValue2 }}</p>
        <p>Тип: {{ typeof selectedValue2 }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 3: Объекты без option-value/label</h6>
        <q-select
          v-model="selectedValue3"
          :options="objectOptions"
          label="Тип государства"
          outlined
          class="q-mb-md"
          clearable
        />
        <p>Выбранное значение: {{ selectedValue3 }}</p>
        <p>Тип: {{ typeof selectedValue3 }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 4: С emit-value и map-options</h6>
        <q-select
          v-model="selectedValue4"
          :options="objectOptions"
          label="Тип государства"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          emit-value
          map-options
          clearable
        />
        <p>Выбранное значение: {{ selectedValue4 }}</p>
        <p>Тип: {{ typeof selectedValue4 }}</p>
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

const simpleOptions = [
  'Государство',
  'Правительство',
  'Коммерческая',
  'Империя'
]

const objectOptions = [
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
]

const selectedValue1 = ref('')
const selectedValue2 = ref('')
const selectedValue3 = ref(null)
const selectedValue4 = ref('GOVERNMENT')

const debugInfo = computed(() => ({
  simpleOptions,
  objectOptions,
  selectedValue1: selectedValue1.value,
  selectedValue2: selectedValue2.value,
  selectedValue3: selectedValue3.value,
  selectedValue4: selectedValue4.value,
  types: {
    value1: typeof selectedValue1.value,
    value2: typeof selectedValue2.value,
    value3: typeof selectedValue3.value,
    value4: typeof selectedValue4.value
  }
}))

console.log('StringTestPage - simpleOptions:', simpleOptions)
console.log('StringTestPage - objectOptions:', objectOptions)
</script>
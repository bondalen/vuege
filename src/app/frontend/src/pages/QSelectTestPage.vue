<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Тест q-select - Проблема с отображением опций</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 1: Без emit-value и map-options</h6>
        <q-select
          v-model="selectedValue1"
          :options="options"
          label="Тип государства"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          clearable
        />
        <p>Выбранное значение: {{ selectedValue1 }}</p>
        <p>Тип: {{ typeof selectedValue1 }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 2: С emit-value и map-options</h6>
        <q-select
          v-model="selectedValue2"
          :options="options"
          label="Тип государства"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          emit-value
          map-options
          clearable
        />
        <p>Выбранное значение: {{ selectedValue2 }}</p>
        <p>Тип: {{ typeof selectedValue2 }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 3: С use-value и fill-input</h6>
        <q-select
          v-model="selectedValue3"
          :options="options"
          label="Тип государства"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
          use-value
          fill-input
          clearable
        />
        <p>Выбранное значение: {{ selectedValue3 }}</p>
        <p>Тип: {{ typeof selectedValue3 }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 4: Только option-value и option-label</h6>
        <q-select
          v-model="selectedValue4"
          :options="options"
          label="Тип государства"
          outlined
          class="q-mb-md"
          option-value="value"
          option-label="label"
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

const options = ref([
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
])

const selectedValue1 = ref(null)
const selectedValue2 = ref('GOVERNMENT')
const selectedValue3 = ref('GOVERNMENT')
const selectedValue4 = ref(null)

const debugInfo = computed(() => ({
  options: options.value,
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

console.log('QSelectTestPage - options:', options.value)
</script>
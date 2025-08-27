<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Минимальный тест q-select</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 1: Минимальная конфигурация</h6>
        <q-select
          v-model="selected"
          :options="options"
          label="Выберите тип"
          outlined
        />
        <p>Выбранное: {{ selected }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 2: С option-value и option-label</h6>
        <q-select
          v-model="selected2"
          :options="options"
          label="Выберите тип"
          outlined
          option-value="value"
          option-label="label"
        />
        <p>Выбранное: {{ selected2 }}</p>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const options = [
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
]

const selected = ref(null)
const selected2 = ref(null)

console.log('MinimalTestPage - options:', options)
</script>
<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Тест CSS и стилей q-select</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 1: Обычный q-select</h6>
        <q-select
          v-model="selected"
          :options="options"
          label="Выберите тип"
          outlined
          class="test-select"
        />
        <p>Выбранное: {{ selected }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 2: С принудительными стилями</h6>
        <q-select
          v-model="selected2"
          :options="options"
          label="Выберите тип"
          outlined
          class="test-select force-options"
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

console.log('CssTestPage - options:', options)
</script>

<style scoped>
.test-select {
  /* Принудительно показываем все опции */
}

.force-options :deep(.q-menu) {
  max-height: none !important;
}

.force-options :deep(.q-option) {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}
</style>
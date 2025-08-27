<template>
  <q-page class="q-pa-md">
    <div class="row q-gutter-md">
      <div class="col-12">
        <h4>Тест принудительного рендеринга q-select</h4>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 1: Принудительный рендеринг</h6>
        <q-select
          v-model="selected"
          :options="options"
          label="Выберите тип"
          outlined
          class="force-render"
        />
        <p>Выбранное: {{ selected }}</p>
      </div>
      
      <div class="col-12 col-md-6">
        <h6>Тест 2: С key для принудительного обновления</h6>
        <q-select
          :key="renderKey"
          v-model="selected2"
          :options="options"
          label="Выберите тип"
          outlined
        />
        <p>Выбранное: {{ selected2 }}</p>
        <q-btn @click="forceRerender" label="Принудительно обновить" />
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
const renderKey = ref(0)

const debugInfo = computed(() => ({
  options,
  selected: selected.value,
  selected2: selected2.value,
  renderKey: renderKey.value
}))

const forceRerender = () => {
  renderKey.value++
}

console.log('ForceRenderTestPage - options:', options)
</script>

<style scoped>
.force-render :deep(.q-menu) {
  max-height: none !important;
}

.force-render :deep(.q-option) {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  height: auto !important;
  min-height: 40px !important;
}

.force-render :deep(.q-virtual-scroll__content) {
  height: auto !important;
}
</style>
<template>
  <div id="app">
    <q-layout view="hHh lpR fFf">
      <q-header elevated class="bg-primary text-white" style="height: 32px; min-height: 32px;">
        <q-toolbar style="height: 32px; min-height: 32px;">
          <q-toolbar-title style="font-size: 0.9rem;">
            Vuege - Система учета организационных единиц
          </q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  console.log('VuegeApp mounted')
})
</script>

<style>
#app {
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  width: 100vw;
  padding: 2px !important;
  margin: 0 !important;
}

/* Уменьшение высоты верхнего фрейма */
.q-header {
  height: 32px !important;
  min-height: 32px !important;
}

/* Исправление отступов для q-layout */
.q-layout {
  padding: 2px !important;
  margin: 0 !important;
}

.q-toolbar {
  height: 32px !important;
  min-height: 32px !important;
  padding: 0 16px !important;
}

.q-toolbar-title {
  font-size: 0.9rem !important;
  line-height: 32px !important;
}
</style>

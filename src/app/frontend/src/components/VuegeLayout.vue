<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          Vuege
        </q-toolbar-title>

        <div>v0.1.0</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header>
          Навигация
        </q-item-label>

        <q-item clickable v-ripple :to="{ name: 'home' }" exact>
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>Главная</q-item-section>
        </q-item>

        <q-item clickable v-ripple :to="{ name: 'organizations' }">
          <q-item-section avatar>
            <q-icon name="business" />
          </q-item-section>
          <q-item-section>Организации</q-item-section>
        </q-item>

        <q-item clickable v-ripple :to="{ name: 'states' }">
          <q-item-section avatar>
            <q-icon name="public" />
          </q-item-section>
          <q-item-section>Государства</q-item-section>
        </q-item>

        <q-item clickable v-ripple :to="{ name: 'people' }">
          <q-item-section avatar>
            <q-icon name="people" />
          </q-item-section>
          <q-item-section>Люди</q-item-section>
        </q-item>

        <q-item clickable v-ripple :to="{ name: 'locations' }">
          <q-item-section avatar>
            <q-icon name="place" />
          </q-item-section>
          <q-item-section>Места</q-item-section>
        </q-item>

        <q-separator />

        <q-item-label header>
          Система
        </q-item-label>

        <q-item clickable v-ripple :to="{ name: 'reports' }">
          <q-item-section avatar>
            <q-icon name="assessment" />
          </q-item-section>
          <q-item-section>Отчеты</q-item-section>
        </q-item>

        <q-item clickable v-ripple :to="{ name: 'settings' }">
          <q-item-section avatar>
            <q-icon name="settings" />
          </q-item-section>
          <q-item-section>Настройки</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <slot />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const leftDrawerOpen = ref(false)

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
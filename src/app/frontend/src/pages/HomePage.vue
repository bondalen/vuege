<template>
  <div class="home-page">
    <q-page class="flex flex-center">
      <div class="text-center q-pa-lg">
        <div class="q-mb-xl">
          <h1 class="text-h1 text-primary q-mb-md">
            Vuege
          </h1>
          <p class="text-h5 text-grey-7 q-mb-lg">
            Система учета организационных единиц с исторической перспективой
          </p>
          <p class="text-body1 text-grey-6">
            Комплексная платформа для управления данными о государствах, организациях, людях и местах
          </p>
        </div>
        
        <div class="row q-gutter-lg justify-center q-mb-xl">
          <q-card class="col-12 col-sm-6 col-md-3 cursor-pointer" 
                  clickable 
                  @click="$router.push({ name: 'organizations' })"
                  :class="{ 'hover-card': true }">
            <q-card-section class="text-center">
              <q-icon name="business" size="3rem" color="primary" class="q-mb-md" />
              <div class="text-h6 q-mb-sm">Организации</div>
              <div class="text-subtitle2 text-grey-6">
                Управление государственными и коммерческими организациями
              </div>
            </q-card-section>
            <q-card-actions class="justify-center">
              <q-btn flat color="primary" label="Перейти" icon="arrow_forward" />
            </q-card-actions>
          </q-card>
          
          <q-card class="col-12 col-sm-6 col-md-3 cursor-pointer" 
                  clickable 
                  @click="$router.push({ name: 'states' })"
                  :class="{ 'hover-card': true }">
            <q-card-section class="text-center">
              <q-icon name="public" size="3rem" color="secondary" class="q-mb-md" />
              <div class="text-h6 q-mb-sm">Государства</div>
              <div class="text-subtitle2 text-grey-6">
                История государств от древности до наших дней
              </div>
            </q-card-section>
            <q-card-actions class="justify-center">
              <q-btn flat color="secondary" label="Перейти" icon="arrow_forward" />
            </q-card-actions>
          </q-card>
          
          <q-card class="col-12 col-sm-6 col-md-3 cursor-pointer" 
                  clickable 
                  @click="$router.push({ name: 'people' })"
                  :class="{ 'hover-card': true }">
            <q-card-section class="text-center">
              <q-icon name="people" size="3rem" color="accent" class="q-mb-md" />
              <div class="text-h6 q-mb-sm">Люди</div>
              <div class="text-subtitle2 text-grey-6">
                Биографии и должности исторических личностей
              </div>
            </q-card-section>
            <q-card-actions class="justify-center">
              <q-btn flat color="accent" label="Перейти" icon="arrow_forward" />
            </q-card-actions>
          </q-card>
          
          <q-card class="col-12 col-sm-6 col-md-3 cursor-pointer" 
                  clickable 
                  @click="$router.push({ name: 'locations' })"
                  :class="{ 'hover-card': true }">
            <q-card-section class="text-center">
              <q-icon name="place" size="3rem" color="positive" class="q-mb-md" />
              <div class="text-h6 q-mb-sm">Места</div>
              <div class="text-subtitle2 text-grey-6">
                Географические локации и их исторические изменения
              </div>
            </q-card-section>
            <q-card-actions class="justify-center">
              <q-btn flat color="positive" label="Перейти" icon="arrow_forward" />
            </q-card-actions>
          </q-card>
        </div>
        
        <div class="row q-gutter-md justify-center">
          <q-card class="col-12 col-md-8">
            <q-card-section>
              <div class="text-h6 q-mb-md">Быстрые действия</div>
              <div class="row q-gutter-sm">
                <q-btn color="primary" icon="add" label="Новая организация" 
                       @click="$router.push({ name: 'organizations' })" />
                <q-btn color="secondary" icon="add" label="Новое государство" 
                       @click="$router.push({ name: 'states' })" />
                <q-btn color="accent" icon="add" label="Новый человек" 
                       @click="$router.push({ name: 'people' })" />
                <q-btn color="positive" icon="add" label="Новое место" 
                       @click="$router.push({ name: 'locations' })" />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-page>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.cursor-pointer {
  cursor: pointer;
}
</style>
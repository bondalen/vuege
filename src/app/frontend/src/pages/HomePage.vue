<template>
  <div class="home-page">
    <q-page class="flex flex-center">
      <div class="text-center">
        <h1 class="text-h2 text-primary q-mb-md">
          Vuege
        </h1>
        <p class="text-h6 text-grey-7 q-mb-lg">
          Система учета организационных единиц с исторической перспективой
        </p>
        
        <div class="row q-gutter-md justify-center">
          <q-card class="col-12 col-sm-6 col-md-4">
            <q-card-section>
              <div class="text-h6">Организации</div>
              <div class="text-subtitle2">Управление государственными и коммерческими организациями</div>
            </q-card-section>
            <q-card-actions>
              <q-btn flat color="primary" label="Перейти" />
            </q-card-actions>
          </q-card>
          
          <q-card class="col-12 col-sm-6 col-md-4">
            <q-card-section>
              <div class="text-h6">Государства</div>
              <div class="text-subtitle2">История государств от древности до наших дней</div>
            </q-card-section>
            <q-card-actions>
              <q-btn flat color="primary" label="Перейти" />
            </q-card-actions>
          </q-card>
          
          <q-card class="col-12 col-sm-6 col-md-4">
            <q-card-section>
              <div class="text-h6">Люди</div>
              <div class="text-subtitle2">Биографии и должности исторических личностей</div>
            </q-card-section>
            <q-card-actions>
              <q-btn flat color="primary" label="Перейти" />
            </q-card-actions>
          </q-card>
        </div>
      </div>
    </q-page>
  </div>
</template>

<script setup lang="ts">
// HomePage component
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}
</style>
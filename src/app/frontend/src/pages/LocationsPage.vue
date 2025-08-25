<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Места</h4>
        <p class="text-body1 text-grey-7">
          Географические места и их историческое значение
        </p>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="Добавить место"
          @click="showCreateDialog = true"
        />
      </div>
    </div>

    <!-- Карта -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-center q-pa-lg">
          <q-icon name="map" size="100px" color="grey-4" />
          <div class="text-h6 q-mt-md">Интерактивная карта</div>
          <p class="text-grey-6">Интеграция с Leaflet для отображения мест</p>
        </div>
      </q-card-section>
    </q-card>

    <!-- Таблица мест -->
    <q-card>
      <q-table
        :rows="locations"
        :columns="columns"
        :loading="loading"
        row-key="id"
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-coordinates="props">
          <q-td :props="props">
            <div v-if="props.row.latitude && props.row.longitude">
              {{ props.row.latitude.toFixed(4) }}, {{ props.row.longitude.toFixed(4) }}
            </div>
            <div v-else class="text-grey-6">Не указано</div>
          </q-td>
        </template>
        
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              color="primary"
              icon="edit"
              size="sm"
              @click="editLocation(props.row)"
            />
            <q-btn
              flat
              round
              color="info"
              icon="map"
              size="sm"
              @click="showOnMap(props.row)"
            />
            <q-btn
              flat
              round
              color="negative"
              icon="delete"
              size="sm"
              @click="deleteLocation(props.row)"
            />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Диалог создания/редактирования -->
    <q-dialog v-model="showCreateDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">
            {{ editingLocation ? 'Редактировать' : 'Создать' }} место
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="form.name"
            label="Название"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-select
            v-model="form.type"
            :options="locationTypes"
            label="Тип места"
            outlined
            dense
            class="q-mb-md"
          />
          
          <div class="row q-gutter-md">
            <q-input
              v-model.number="form.latitude"
              label="Широта"
              type="number"
              step="0.0001"
              outlined
              dense
              class="col"
            />
            
            <q-input
              v-model.number="form.longitude"
              label="Долгота"
              type="number"
              step="0.0001"
              outlined
              dense
              class="col"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn
            :label="editingLocation ? 'Сохранить' : 'Создать'"
            color="primary"
            @click="saveLocation"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Location, LocationType } from '../types/graphql'

// Состояние
const loading = ref(false)
const locations = ref<Location[]>([])
const showCreateDialog = ref(false)
const editingLocation = ref<Location | null>(null)

// Форма
const form = reactive({
  name: '',
  type: LocationType.CITY,
  latitude: null as number | null,
  longitude: null as number | null
})

// Опции
const locationTypes = [
  { label: 'Страна', value: LocationType.COUNTRY },
  { label: 'Регион', value: LocationType.REGION },
  { label: 'Город', value: LocationType.CITY },
  { label: 'Район', value: LocationType.DISTRICT },
  { label: 'Адрес', value: LocationType.ADDRESS },
  { label: 'Координаты', value: LocationType.COORDINATES }
]

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true },
  { name: 'type', label: 'Тип', field: 'type', sortable: true },
  { name: 'coordinates', label: 'Координаты', field: 'coordinates', sortable: false },
  { name: 'parentLocation', label: 'Родительское место', field: row => row.parentLocation?.name || '-', sortable: false },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false }
]

// Методы
const loadLocations = async () => {
  loading.value = true
  try {
    // TODO: Загрузка через GraphQL
    locations.value = []
  } catch (error) {
    console.error('Ошибка загрузки мест:', error)
  } finally {
    loading.value = false
  }
}

const editLocation = (location: Location) => {
  editingLocation.value = location
  form.name = location.name
  form.type = location.type
  form.latitude = location.latitude || null
  form.longitude = location.longitude || null
  showCreateDialog.value = true
}

const showOnMap = (location: Location) => {
  // TODO: Показать на карте
  console.log('Показать на карте:', location)
}

const deleteLocation = async (location: Location) => {
  // TODO: Удаление через GraphQL
  console.log('Удаление места:', location.id)
}

const saveLocation = async () => {
  try {
    // TODO: Сохранение через GraphQL
    console.log('Сохранение места:', form)
    showCreateDialog.value = false
    await loadLocations()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  }
}

// Инициализация
onMounted(() => {
  loadLocations()
})
</script>
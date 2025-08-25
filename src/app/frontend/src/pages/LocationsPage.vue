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
          @click="openCreateDialog"
        />
      </div>
    </div>

    <!-- Карта -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div style="height: 400px;">
          <VuegeMap 
            :center="mapCenter"
            :zoom="mapZoom"
            :markers="mapMarkers"
            :polygons="mapPolygons"
          />
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
              @click="handleDeleteLocation(props.row)"
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
          <div class="row q-gutter-md">
            <q-input
              v-model="form.name"
              label="Название *"
              outlined
              dense
              class="col-12"
              :rules="[val => !!val || 'Название обязательно']"
            />
            
            <q-select
              v-model="form.type"
              :options="locationTypes"
              label="Тип места *"
              outlined
              dense
              class="col-12 col-sm-6"
              :rules="[val => !!val || 'Тип обязателен']"
            />
            
            <q-input
              v-model="form.parentLocationId"
              label="ID родительского места"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-input
              v-model.number="form.latitude"
              label="Широта"
              type="number"
              step="0.0001"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-input
              v-model.number="form.longitude"
              label="Долгота"
              type="number"
              step="0.0001"
              outlined
              dense
              class="col-12 col-sm-6"
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import type { Location, LocationType, SearchInput } from '../types/graphql'
import { GET_LOCATIONS } from '../graphql/queries'
import { CREATE_LOCATION, UPDATE_LOCATION, DELETE_LOCATION } from '../graphql/mutations'
import VuegeMap from '../components/VuegeMap.vue'

const $q = useQuasar()

// Состояние
const showCreateDialog = ref(false)
const editingLocation = ref<Location | null>(null)

// Форма
const form = reactive({
  name: '',
  type: LocationType.CITY,
  latitude: null as number | null,
  longitude: null as number | null,
  parentLocationId: ''
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

// Вычисляемые параметры поиска
const searchParams = computed<SearchInput>(() => ({
  query: '',
  filters: {},
  pagination: {
    page: 1,
    size: 100
  }
}))

// GraphQL запросы
const { result, loading, error, refetch } = useQuery(
  GET_LOCATIONS,
  { search: searchParams },
  { fetchPolicy: 'cache-and-network' }
)

// Мутации
const { mutate: createLocation, loading: creating } = useMutation(CREATE_LOCATION)
const { mutate: updateLocation, loading: updating } = useMutation(UPDATE_LOCATION)
const { mutate: deleteLocation, loading: deleting } = useMutation(DELETE_LOCATION)

// Вычисляемые данные
const locations = computed(() => result.value?.locations || [])

// Вычисляемые свойства для карты
const mapCenter = computed(() => {
  const locationsWithCoords = locations.value.filter(loc => loc.latitude && loc.longitude)
  if (locationsWithCoords.length === 0) {
    return [55.7558, 37.6176] as [number, number] // Москва по умолчанию
  }
  
  const avgLat = locationsWithCoords.reduce((sum, loc) => sum + loc.latitude!, 0) / locationsWithCoords.length
  const avgLng = locationsWithCoords.reduce((sum, loc) => sum + loc.longitude!, 0) / locationsWithCoords.length
  
  return [avgLat, avgLng] as [number, number]
})

const mapZoom = computed(() => {
  const locationsWithCoords = locations.value.filter(loc => loc.latitude && loc.longitude)
  if (locationsWithCoords.length === 0) return 10
  if (locationsWithCoords.length === 1) return 12
  return 6
})

const mapMarkers = computed(() => {
  return locations.value
    .filter(loc => loc.latitude && loc.longitude)
    .map(loc => ({
      position: [loc.latitude!, loc.longitude!] as [number, number],
      title: loc.name,
      description: getLocationTypeLabel(loc.type)
    }))
})

const mapPolygons = computed(() => {
  // Здесь можно добавить полигоны для регионов, если они есть в данных
  return []
})

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
  { name: 'type', label: 'Тип', field: 'type', sortable: true, align: 'left' },
  { name: 'coordinates', label: 'Координаты', field: 'coordinates', sortable: false, align: 'center' },
  { name: 'parentLocation', label: 'Родительское место', field: row => row.parentLocation?.name || '-', sortable: false, align: 'left' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Методы
const resetForm = () => {
  form.name = ''
  form.type = LocationType.CITY
  form.latitude = null
  form.longitude = null
  form.parentLocationId = ''
  editingLocation.value = null
}

const getLocationTypeLabel = (type: LocationType): string => {
  const typeOption = locationTypes.find(t => t.value === type)
  return typeOption ? typeOption.label : type
}

const editLocation = (location: Location) => {
  editingLocation.value = location
  form.name = location.name
  form.type = location.type
  form.latitude = location.latitude || null
  form.longitude = location.longitude || null
  form.parentLocationId = location.parentLocation?.id || ''
  showCreateDialog.value = true
}

const showOnMap = (location: Location) => {
  // Можно добавить центрирование карты на выбранном месте
  console.log('Показать на карте:', location)
}

const handleDeleteLocation = async (location: Location) => {
  try {
    await $q.dialog({
      title: 'Подтверждение удаления',
      message: `Вы уверены, что хотите удалить место "${location.name}"?`,
      cancel: true,
      persistent: true
    })

    await deleteLocation({ id: location.id })
    
    $q.notify({
      type: 'positive',
      message: 'Место успешно удалено'
    })
    
    await refetch()
  } catch (error) {
    console.error('Ошибка удаления места:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при удалении места'
    })
  }
}

const saveLocation = async () => {
  try {
    const input = {
      name: form.name,
      type: form.type,
      latitude: form.latitude,
      longitude: form.longitude,
      parentLocationId: form.parentLocationId || null
    }

    if (editingLocation.value) {
      await updateLocation({ 
        id: editingLocation.value.id, 
        input 
      })
      $q.notify({
        type: 'positive',
        message: 'Место успешно обновлено'
      })
    } else {
      await createLocation({ input })
      $q.notify({
        type: 'positive',
        message: 'Место успешно создано'
      })
    }

    showCreateDialog.value = false
    resetForm()
    await refetch()
  } catch (error) {
    console.error('Ошибка сохранения места:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении места'
    })
  }
}

const openCreateDialog = () => {
  resetForm()
  showCreateDialog.value = true
}

// Обработка ошибок
if (error.value) {
  console.error('Ошибка загрузки мест:', error.value)
  $q.notify({
    type: 'negative',
    message: 'Ошибка при загрузке мест'
  })
}
</script>
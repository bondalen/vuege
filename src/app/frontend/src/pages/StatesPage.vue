<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Государства</h4>
        <p class="text-body1 text-grey-7">
          История государств от древности до наших дней
        </p>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="Добавить государство"
          @click="openCreateDialog"
        />
      </div>
    </div>

    <!-- Фильтры -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-gutter-md">
          <q-input
            v-model="searchQuery"
            label="Поиск"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          
          <q-select
            v-model="selectedType"
            :options="stateTypes"
            label="Тип государства"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
            clearable
          />
          
          <q-input
            v-model="dateRange"
            label="Период существования"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
            placeholder="Например: 1000-1500"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Таблица государств -->
    <q-card>
      <q-table
        :rows="states"
        :columns="columns"
        :loading="loading"
        row-key="id"
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              color="primary"
              icon="edit"
              size="sm"
              @click="editState(props.row)"
            />
            <q-btn
              flat
              round
              color="info"
              icon="map"
              size="sm"
              @click="showMap(props.row)"
            />
            <q-btn
              flat
              round
              color="negative"
              icon="delete"
              size="sm"
              @click="handleDeleteState(props.row)"
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
            {{ editingState ? 'Редактировать' : 'Создать' }} государство
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
          
          <q-input
            v-model="form.code"
            label="Код"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-select
            v-model="form.type"
            :options="stateTypes"
            label="Тип государства"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-input
            v-model="form.description"
            label="Описание"
            type="textarea"
            outlined
            dense
            class="q-mb-md"
          />
          
          <div class="row q-gutter-md">
            <q-input
              v-model="form.foundedDate"
              label="Дата основания"
              type="date"
              outlined
              dense
              class="col"
            />
            
            <q-input
              v-model="form.dissolvedDate"
              label="Дата распада"
              type="date"
              outlined
              dense
              class="col"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn
            :label="editingState ? 'Сохранить' : 'Создать'"
            color="primary"
            @click="saveState"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Диалог карты -->
    <q-dialog v-model="showMapDialog" maximized>
      <q-card>
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Карта государства: {{ selectedState?.name }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        
        <q-card-section class="q-pa-none">
          <div style="height: 70vh;">
            <VuegeMap 
              :center="mapCenter"
              :zoom="mapZoom"
              :markers="mapMarkers"
              :polygons="mapPolygons"
            />
          </div>
        </q-card-section>
        
        <q-card-section>
          <div class="row q-gutter-md">
            <div class="col-12 col-md-6">
              <h6 class="q-mb-sm">Информация о государстве</h6>
              <div v-if="selectedState">
                <p><strong>Название:</strong> {{ selectedState.name }}</p>
                <p v-if="selectedState.code"><strong>Код:</strong> {{ selectedState.code }}</p>
                <p><strong>Тип:</strong> {{ getStateTypeLabel(selectedState.type) }}</p>
                <p v-if="selectedState.foundedDate"><strong>Основано:</strong> {{ selectedState.foundedDate }}</p>
                <p v-if="selectedState.dissolvedDate"><strong>Распалось:</strong> {{ selectedState.dissolvedDate }}</p>
                <p v-if="selectedState.capital"><strong>Столица:</strong> {{ selectedState.capital.name }}</p>
                <p v-if="selectedState.description"><strong>Описание:</strong> {{ selectedState.description }}</p>
              </div>
            </div>
            <div class="col-12 col-md-6">
              <h6 class="q-mb-sm">Территории</h6>
              <div v-if="selectedState?.territory?.length">
                <q-list>
                  <q-item v-for="territory in selectedState.territory" :key="territory.id">
                    <q-item-section>
                      <q-item-label>{{ territory.name }}</q-item-label>
                      <q-item-label caption>{{ getLocationTypeLabel(territory.type) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
              <div v-else class="text-grey-6">
                Территории не указаны
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import type { State, StateType, SearchInput, LocationType } from '../types/graphql'
import { GET_STATES } from '../graphql/queries'
import { CREATE_STATE, UPDATE_STATE, DELETE_STATE } from '../graphql/mutations'
import VuegeMap from '../components/VuegeMap.vue'

const $q = useQuasar()

// Состояние
const searchQuery = ref('')
const selectedType = ref<StateType | null>(null)
const dateRange = ref('')
const showCreateDialog = ref(false)
const showMapDialog = ref(false)
const editingState = ref<State | null>(null)
const selectedState = ref<State | null>(null)

// Форма
const form = reactive({
  name: '',
  code: '',
  type: StateType.REPUBLIC,
  description: '',
  foundedDate: '',
  dissolvedDate: '',
  capitalId: ''
})

// Опции
const stateTypes = [
  { label: 'Империя', value: StateType.EMPIRE },
  { label: 'Королевство', value: StateType.KINGDOM },
  { label: 'Республика', value: StateType.REPUBLIC },
  { label: 'Федерация', value: StateType.FEDERATION },
  { label: 'Конфедерация', value: StateType.CONFEDERATION },
  { label: 'Другое', value: StateType.OTHER }
]

// Вычисляемые параметры поиска
const searchParams = computed<SearchInput>(() => ({
  query: searchQuery.value,
  filters: {
    type: selectedType.value,
    dateRange: dateRange.value
  },
  pagination: {
    page: 1,
    size: 50
  }
}))

// GraphQL запросы
const { result, loading, error, refetch } = useQuery(
  GET_STATES,
  { search: searchParams },
  { fetchPolicy: 'cache-and-network' }
)

// Мутации
const { mutate: createState, loading: creating } = useMutation(CREATE_STATE)
const { mutate: updateState, loading: updating } = useMutation(UPDATE_STATE)
const { mutate: deleteState, loading: deleting } = useMutation(DELETE_STATE)

// Вычисляемые данные
const states = computed(() => result.value?.states || [])

// Вычисляемые свойства для карты
const mapCenter = computed(() => {
  if (selectedState.value?.capital?.latitude && selectedState.value?.capital?.longitude) {
    return [selectedState.value.capital.latitude, selectedState.value.capital.longitude] as [number, number]
  }
  return [55.7558, 37.6176] as [number, number] // Москва по умолчанию
})

const mapZoom = computed(() => {
  if (selectedState.value?.territory?.length) return 6
  return 10
})

const mapMarkers = computed(() => {
  if (!selectedState.value?.capital) return []
  
  return [{
    position: [selectedState.value.capital.latitude!, selectedState.value.capital.longitude!] as [number, number],
    title: selectedState.value.capital.name,
    description: 'Столица'
  }]
})

const mapPolygons = computed(() => {
  // Здесь можно добавить полигоны территорий, если они есть в данных
  return []
})

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
  { name: 'code', label: 'Код', field: 'code', sortable: true, align: 'center' },
  { name: 'type', label: 'Тип', field: 'type', sortable: true, align: 'left' },
  { name: 'foundedDate', label: 'Основано', field: 'foundedDate', sortable: true, align: 'center' },
  { name: 'dissolvedDate', label: 'Распалось', field: 'dissolvedDate', sortable: true, align: 'center' },
  { name: 'capital', label: 'Столица', field: row => row.capital?.name || '-', sortable: false, align: 'left' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Методы
const resetForm = () => {
  form.name = ''
  form.code = ''
  form.type = StateType.REPUBLIC
  form.description = ''
  form.foundedDate = ''
  form.dissolvedDate = ''
  form.capitalId = ''
  editingState.value = null
}

const editState = (state: State) => {
  editingState.value = state
  form.name = state.name
  form.code = state.code || ''
  form.type = state.type
  form.description = state.description || ''
  form.foundedDate = state.foundedDate || ''
  form.dissolvedDate = state.dissolvedDate || ''
  form.capitalId = state.capital?.id || ''
  showCreateDialog.value = true
}

const showMap = (state: State) => {
  selectedState.value = state
  showMapDialog.value = true
}

const handleDeleteState = async (state: State) => {
  try {
    await $q.dialog({
      title: 'Подтверждение удаления',
      message: `Вы уверены, что хотите удалить государство "${state.name}"?`,
      cancel: true,
      persistent: true
    })

    await deleteState({ id: state.id })
    
    $q.notify({
      type: 'positive',
      message: 'Государство успешно удалено'
    })
    
    await refetch()
  } catch (error) {
    console.error('Ошибка удаления государства:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при удалении государства'
    })
  }
}

const saveState = async () => {
  try {
    const input = {
      name: form.name,
      code: form.code || null,
      type: form.type,
      description: form.description || null,
      foundedDate: form.foundedDate || null,
      dissolvedDate: form.dissolvedDate || null,
      capitalId: form.capitalId || null
    }

    if (editingState.value) {
      await updateState({ 
        id: editingState.value.id, 
        input 
      })
      $q.notify({
        type: 'positive',
        message: 'Государство успешно обновлено'
      })
    } else {
      await createState({ input })
      $q.notify({
        type: 'positive',
        message: 'Государство успешно создано'
      })
    }

    showCreateDialog.value = false
    resetForm()
    await refetch()
  } catch (error) {
    console.error('Ошибка сохранения государства:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении государства'
    })
  }
}

const openCreateDialog = () => {
  resetForm()
  showCreateDialog.value = true
}

// Вспомогательные методы
const getStateTypeLabel = (type: StateType): string => {
  const typeOption = stateTypes.find(t => t.value === type)
  return typeOption ? typeOption.label : type
}

const getLocationTypeLabel = (type: LocationType): string => {
  const locationTypes = {
    [LocationType.COUNTRY]: 'Страна',
    [LocationType.REGION]: 'Регион',
    [LocationType.CITY]: 'Город',
    [LocationType.DISTRICT]: 'Район',
    [LocationType.ADDRESS]: 'Адрес',
    [LocationType.COORDINATES]: 'Координаты'
  }
  return locationTypes[type] || type
}

// Обработка ошибок
if (error.value) {
  console.error('Ошибка загрузки государств:', error.value)
  $q.notify({
    type: 'negative',
    message: 'Ошибка при загрузке государств'
  })
}
</script>
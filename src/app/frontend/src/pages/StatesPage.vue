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
          
          <!-- Временное решение: обычный HTML select -->
          <div class="q-field q-field--outlined q-field--dense col-12 col-sm-6 col-md-4">
            <div class="q-field__control">
              <div class="q-field__control-container">
                <select
                  v-model="selectedType"
                  class="q-field__native q-placeholder"
                  style="width: 100%; padding: 8px; border: none; outline: none; background: transparent;"
                >
                  <option value="">Все типы</option>
                  <option value="STATE">Государство</option>
                  <option value="GOVERNMENT">Правительство</option>
                  <option value="COMMERCIAL">Коммерческая</option>
                  <option value="EMPIRE">Империя</option>
                </select>
              </div>
            </div>
            <div class="q-field__label">Тип государства</div>
          </div>
          
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
          
          <!-- Временное решение: обычный HTML select -->
          <div class="q-field q-field--outlined q-field--dense q-mb-md">
            <div class="q-field__control">
              <div class="q-field__control-container">
                <select
                  v-model="form.type"
                  class="q-field__native q-placeholder"
                  style="width: 100%; padding: 8px; border: none; outline: none; background: transparent;"
                >
                  <option value="">Выберите тип государства</option>
                  <option value="STATE">Государство</option>
                  <option value="GOVERNMENT">Правительство</option>
                  <option value="COMMERCIAL">Коммерческая</option>
                  <option value="EMPIRE">Империя</option>
                </select>
              </div>
            </div>
            <div class="q-field__label">Тип государства</div>
          </div>
          
          <q-input
            v-model="form.foundedDate"
            label="Дата основания"
            type="date"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-input
            v-model="form.dissolvedDate"
            label="Дата распада"
            type="date"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-checkbox
            v-model="form.isFictional"
            label="Вымышленное государство"
            class="q-mb-md"
          />
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
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import type { Organization, SearchInput } from '../types/graphql'
import { OrganizationType } from '../types/graphql'
import { GET_ORGANIZATIONS } from '../graphql/queries'
import { CREATE_ORGANIZATION, UPDATE_ORGANIZATION, DELETE_ORGANIZATION } from '../graphql/mutations'
import VuegeMap from '../components/VuegeMap.vue'

const $q = useQuasar()

// Состояние
const searchQuery = ref('')
const selectedType = ref<OrganizationType | null>(null)
const dateRange = ref('')
const showCreateDialog = ref(false)
const showMapDialog = ref(false)
const editingState = ref<Organization | null>(null)
const selectedState = ref<Organization | null>(null)

// Форма
const form = reactive({
  name: '',
  type: 'GOVERNMENT',
  foundedDate: '',
  dissolvedDate: '',
  isFictional: false
})

// Опции - используем computed
const stateTypes = computed(() => [
  { label: 'Государство', value: 'STATE' },
  { label: 'Правительство', value: 'GOVERNMENT' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Империя', value: 'EMPIRE' }
])

console.log('stateTypes array:', stateTypes.value)
console.log('stateTypes length:', stateTypes.value.length)
stateTypes.value.forEach((type, index) => {
  console.log(`stateTypes[${index}]:`, type)
})

const historicalPeriods = [
  { label: 'Раннее Средневековье (476-1000)', value: '1' },
  { label: 'Высокое Средневековье (1000-1300)', value: '2' },
  { label: 'Позднее Средневековье (1300-1492)', value: '3' },
  { label: 'Новое время (1492-1789)', value: '4' },
  { label: 'Новейшее время (1789-2025)', value: '5' }
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
  GET_ORGANIZATIONS,
  {},
  { fetchPolicy: 'cache-and-network' }
)

// Отладочное логирование
console.log('StatesPage - result:', result.value)
console.log('StatesPage - loading:', loading.value)
console.log('StatesPage - error:', error.value)

// Мутации
const { mutate: createOrganization, loading: creating } = useMutation(CREATE_ORGANIZATION)
const { mutate: updateOrganization, loading: updating } = useMutation(UPDATE_ORGANIZATION)
const { mutate: deleteOrganization, loading: deleting } = useMutation(DELETE_ORGANIZATION)

// Вычисляемые данные
const states = computed(() => {
  const data = result.value?.organizationalUnits || []
  
  // Фильтрация по поиску
  let filtered = data
  if (searchQuery.value) {
    filtered = filtered.filter(state => 
      state.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      state.type.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  // Фильтрация по типу
  if (selectedType.value) {
    filtered = filtered.filter(state => state.type === selectedType.value)
  }
  
  return filtered
})

// Вычисляемые свойства для карты
const mapCenter = computed(() => {
  if (selectedState.value?.location?.latitude && selectedState.value?.location?.longitude) {
    return [selectedState.value.location.latitude, selectedState.value.location.longitude] as [number, number]
  }
  return [55.7558, 37.6176] as [number, number] // Москва по умолчанию
})

const mapZoom = computed(() => {
  return 10
})

const mapMarkers = computed(() => {
  if (!selectedState.value?.location) return []
  
  return [{
    position: [selectedState.value.location.latitude!, selectedState.value.location.longitude!] as [number, number],
    title: selectedState.value.location.name,
    description: 'Местоположение'
  }]
})

const mapPolygons = computed(() => {
  // Здесь можно добавить полигоны территорий, если они есть в данных
  return []
})

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' as const },
  { name: 'type', label: 'Тип', field: 'type', sortable: true, align: 'left' as const },
  { name: 'foundedDate', label: 'Основано', field: 'foundedDate', sortable: true, align: 'center' as const },
  { name: 'dissolvedDate', label: 'Распалось', field: 'dissolvedDate', sortable: true, align: 'center' as const },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' as const }
]

// Методы
const resetForm = () => {
  form.name = ''
  form.type = 'GOVERNMENT'
  form.foundedDate = ''
  form.dissolvedDate = ''
  form.isFictional = false
  editingState.value = null
}

const editState = (state: any) => {
  console.log('editState - incoming state:', state)
  console.log('editState - stateTypes:', stateTypes.value)
  editingState.value = state
  
  // Сбросим форму перед заполнением
  resetForm()
  
  // Заполним форму новыми значениями
  form.name = state.name
  form.type = state.type
  form.foundedDate = state.foundedDate || ''
  form.dissolvedDate = state.dissolvedDate || ''
  form.isFictional = state.isFictional || false
  
  console.log('editState - form after setting:', form)
  console.log('editState - form.type:', form.type)
  console.log('editState - stateTypes:', stateTypes.value)
  console.log('editState - matching option:', stateTypes.value.find(t => t.value === form.type))
  
  showCreateDialog.value = true
}

const showMap = (state: Organization) => {
  selectedState.value = state
  showMapDialog.value = true
}

const handleDeleteState = async (state: Organization) => {
  try {
    await $q.dialog({
      title: 'Подтверждение удаления',
      message: `Вы уверены, что хотите удалить организацию "${state.name}"?`,
      cancel: true,
      persistent: true
    })

    await deleteOrganization({ id: state.id })
    
    $q.notify({
      type: 'positive',
      message: 'Организация успешно удалена'
    })
    
    await refetch()
  } catch (error) {
    console.error('Ошибка удаления организации:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при удалении организации'
    })
  }
}

const saveState = async () => {
  try {
    const input = {
      name: form.name,
      type: form.type,
      foundedDate: form.foundedDate || null,
      dissolvedDate: form.dissolvedDate || null,
      isFictional: form.isFictional
    }

    if (editingState.value) {
      await updateOrganization({ 
        id: editingState.value.id, 
        input 
      })
      $q.notify({
        type: 'positive',
        message: 'Организация успешно обновлена'
      })
    } else {
      await createOrganization({ input })
      $q.notify({
        type: 'positive',
        message: 'Организация успешно создана'
      })
    }

    showCreateDialog.value = false
    resetForm()
    await refetch()
  } catch (error) {
    console.error('Ошибка сохранения организации:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении организации'
    })
  }
}

const openCreateDialog = () => {
  resetForm()
  showCreateDialog.value = true
}

// Вспомогательные методы
const getStateTypeLabel = (type: OrganizationType): string => {
  const typeOption = stateTypes.value.find(t => t.value === type)
  return typeOption ? typeOption.label : type
}

const getLocationTypeLabel = (type: string): string => {
  const locationTypes: Record<string, string> = {
    'COUNTRY': 'Страна',
    'REGION': 'Регион',
    'CITY': 'Город',
    'DISTRICT': 'Район',
    'ADDRESS': 'Адрес',
    'COORDINATES': 'Координаты'
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
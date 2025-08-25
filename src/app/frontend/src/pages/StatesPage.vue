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
          @click="showCreateDialog = true"
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
              @click="deleteState(props.row)"
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
        
        <q-card-section>
          <div class="text-center q-pa-lg">
            <q-icon name="map" size="100px" color="grey-4" />
            <div class="text-h6 q-mt-md">Карта будет добавлена позже</div>
            <p class="text-grey-6">Интеграция с Leaflet для отображения территорий</p>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { State, StateType } from '../types/graphql'

// Состояние
const loading = ref(false)
const states = ref<State[]>([])
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
  dissolvedDate: ''
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

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true },
  { name: 'code', label: 'Код', field: 'code', sortable: true },
  { name: 'type', label: 'Тип', field: 'type', sortable: true },
  { name: 'foundedDate', label: 'Основано', field: 'foundedDate', sortable: true },
  { name: 'dissolvedDate', label: 'Распалось', field: 'dissolvedDate', sortable: true },
  { name: 'capital', label: 'Столица', field: row => row.capital?.name || '-', sortable: false },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false }
]

// Методы
const loadStates = async () => {
  loading.value = true
  try {
    // TODO: Загрузка через GraphQL
    states.value = []
  } catch (error) {
    console.error('Ошибка загрузки государств:', error)
  } finally {
    loading.value = false
  }
}

const editState = (state: State) => {
  editingState.value = state
  form.name = state.name
  form.code = state.code || ''
  form.type = state.type
  form.description = state.description || ''
  form.foundedDate = state.foundedDate || ''
  form.dissolvedDate = state.dissolvedDate || ''
  showCreateDialog.value = true
}

const showMap = (state: State) => {
  selectedState.value = state
  showMapDialog.value = true
}

const deleteState = async (state: State) => {
  // TODO: Удаление через GraphQL
  console.log('Удаление государства:', state.id)
}

const saveState = async () => {
  try {
    // TODO: Сохранение через GraphQL
    console.log('Сохранение государства:', form)
    showCreateDialog.value = false
    await loadStates()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  }
}

// Инициализация
onMounted(() => {
  loadStates()
})
</script>
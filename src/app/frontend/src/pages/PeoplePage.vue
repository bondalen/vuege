<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Люди</h4>
        <p class="text-body1 text-grey-7">
          Биографии и должности исторических личностей
        </p>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="Добавить человека"
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
            label="Поиск по имени"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          
          <q-input
            v-model="birthYearRange"
            label="Год рождения"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
            placeholder="Например: 1800-1900"
          />
          
          <q-select
            v-model="selectedOrganization"
            :options="organizations"
            label="Организация"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
            clearable
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Таблица людей -->
    <q-card>
      <q-table
        :rows="people"
        :columns="columns"
        :loading="loading"
        row-key="id"
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-fullName="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ props.row.firstName }} {{ props.row.lastName }}</div>
            <div class="text-caption text-grey-6" v-if="props.row.middleName">
              {{ props.row.middleName }}
            </div>
          </q-td>
        </template>
        
        <template v-slot:body-cell-birthDeath="props">
          <q-td :props="props">
            <div v-if="props.row.birthDate || props.row.deathDate">
              {{ formatYear(props.row.birthDate) }} - {{ formatYear(props.row.deathDate) }}
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
              @click="editPerson(props.row)"
            />
            <q-btn
              flat
              round
              color="info"
              icon="work"
              size="sm"
              @click="showPositions(props.row)"
            />
            <q-btn
              flat
              round
              color="negative"
              icon="delete"
              size="sm"
              @click="deletePerson(props.row)"
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
            {{ editingPerson ? 'Редактировать' : 'Создать' }} человека
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="row q-gutter-md">
            <q-input
              v-model="form.firstName"
              label="Имя"
              outlined
              dense
              class="col"
            />
            
            <q-input
              v-model="form.lastName"
              label="Фамилия"
              outlined
              dense
              class="col"
            />
          </div>
          
          <q-input
            v-model="form.middleName"
            label="Отчество"
            outlined
            dense
            class="q-mt-md"
          />
          
          <div class="row q-gutter-md q-mt-md">
            <q-input
              v-model="form.birthDate"
              label="Дата рождения"
              type="date"
              outlined
              dense
              class="col"
            />
            
            <q-input
              v-model="form.deathDate"
              label="Дата смерти"
              type="date"
              outlined
              dense
              class="col"
            />
          </div>
          
          <q-input
            v-model="form.biography"
            label="Биография"
            type="textarea"
            outlined
            dense
            class="q-mt-md"
            rows="4"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn
            :label="editingPerson ? 'Сохранить' : 'Создать'"
            color="primary"
            @click="savePerson"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Диалог должностей -->
    <q-dialog v-model="showPositionsDialog" maximized>
      <q-card>
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">
            Должности: {{ selectedPerson?.firstName }} {{ selectedPerson?.lastName }}
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        
        <q-card-section>
          <div class="text-center q-pa-lg">
            <q-icon name="work" size="100px" color="grey-4" />
            <div class="text-h6 q-mt-md">Должности будут добавлены позже</div>
            <p class="text-grey-6">Интеграция с системой должностей</p>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Person, Organization } from '../types/graphql'

// Состояние
const loading = ref(false)
const people = ref<Person[]>([])
const organizations = ref<Organization[]>([])
const searchQuery = ref('')
const birthYearRange = ref('')
const selectedOrganization = ref<Organization | null>(null)
const showCreateDialog = ref(false)
const showPositionsDialog = ref(false)
const editingPerson = ref<Person | null>(null)
const selectedPerson = ref<Person | null>(null)

// Форма
const form = reactive({
  firstName: '',
  lastName: '',
  middleName: '',
  birthDate: '',
  deathDate: '',
  biography: ''
})

// Колонки таблицы
const columns = [
  { name: 'fullName', label: 'ФИО', field: 'fullName', sortable: false },
  { name: 'birthDeath', label: 'Годы жизни', field: 'birthDeath', sortable: false },
  { name: 'positions', label: 'Должности', field: row => row.positions?.length || 0, sortable: true },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false }
]

// Методы
const loadPeople = async () => {
  loading.value = true
  try {
    // TODO: Загрузка через GraphQL
    people.value = []
  } catch (error) {
    console.error('Ошибка загрузки людей:', error)
  } finally {
    loading.value = false
  }
}

const loadOrganizations = async () => {
  try {
    // TODO: Загрузка организаций для фильтра
    organizations.value = []
  } catch (error) {
    console.error('Ошибка загрузки организаций:', error)
  }
}

const formatYear = (date: string | undefined) => {
  if (!date) return '?'
  return new Date(date).getFullYear()
}

const editPerson = (person: Person) => {
  editingPerson.value = person
  form.firstName = person.firstName
  form.lastName = person.lastName
  form.middleName = person.middleName || ''
  form.birthDate = person.birthDate || ''
  form.deathDate = person.deathDate || ''
  form.biography = person.biography || ''
  showCreateDialog.value = true
}

const showPositions = (person: Person) => {
  selectedPerson.value = person
  showPositionsDialog.value = true
}

const deletePerson = async (person: Person) => {
  // TODO: Удаление через GraphQL
  console.log('Удаление человека:', person.id)
}

const savePerson = async () => {
  try {
    // TODO: Сохранение через GraphQL
    console.log('Сохранение человека:', form)
    showCreateDialog.value = false
    await loadPeople()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  }
}

// Инициализация
onMounted(() => {
  loadPeople()
  loadOrganizations()
})
</script>
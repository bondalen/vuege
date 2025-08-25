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
              @click="handleDeletePerson(props.row)"
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import type { Person, Organization, SearchInput } from '../types/graphql'
import { GET_PEOPLE, GET_ORGANIZATIONS } from '../graphql/queries'
import { CREATE_PERSON, UPDATE_PERSON, DELETE_PERSON } from '../graphql/mutations'

const $q = useQuasar()

// Состояние
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

// Вычисляемые параметры поиска
const searchParams = computed<SearchInput>(() => ({
  query: searchQuery.value,
  filters: {
    birthYearRange: birthYearRange.value,
    organizationId: selectedOrganization.value?.id
  },
  pagination: {
    page: 1,
    size: 50
  }
}))

// GraphQL запросы
const { result: peopleResult, loading, error, refetch } = useQuery(
  GET_PEOPLE,
  { search: searchParams },
  { fetchPolicy: 'cache-and-network' }
)

const { result: organizationsResult } = useQuery(
  GET_ORGANIZATIONS,
  { search: { query: '', pagination: { page: 1, size: 100 } } },
  { fetchPolicy: 'cache-and-network' }
)

// Мутации
const { mutate: createPerson, loading: creating } = useMutation(CREATE_PERSON)
const { mutate: updatePerson, loading: updating } = useMutation(UPDATE_PERSON)
const { mutate: deletePerson, loading: deleting } = useMutation(DELETE_PERSON)

// Вычисляемые данные
const people = computed(() => peopleResult.value?.people || [])
const organizations = computed(() => organizationsResult.value?.organizations || [])

// Колонки таблицы
const columns = [
  { name: 'fullName', label: 'ФИО', field: 'fullName', sortable: false, align: 'left' },
  { name: 'birthDeath', label: 'Годы жизни', field: 'birthDeath', sortable: false, align: 'center' },
  { name: 'positions', label: 'Должности', field: row => row.positions?.length || 0, sortable: true, align: 'center' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Методы
const resetForm = () => {
  form.firstName = ''
  form.lastName = ''
  form.middleName = ''
  form.birthDate = ''
  form.deathDate = ''
  form.biography = ''
  editingPerson.value = null
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

const handleDeletePerson = async (person: Person) => {
  try {
    await $q.dialog({
      title: 'Подтверждение удаления',
      message: `Вы уверены, что хотите удалить "${person.firstName} ${person.lastName}"?`,
      cancel: true,
      persistent: true
    })

    await deletePerson({ id: person.id })
    
    $q.notify({
      type: 'positive',
      message: 'Человек успешно удален'
    })
    
    await refetch()
  } catch (error) {
    console.error('Ошибка удаления человека:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при удалении человека'
    })
  }
}

const savePerson = async () => {
  try {
    const input = {
      firstName: form.firstName,
      lastName: form.lastName,
      middleName: form.middleName || null,
      birthDate: form.birthDate || null,
      deathDate: form.deathDate || null,
      biography: form.biography || null
    }

    if (editingPerson.value) {
      await updatePerson({ 
        id: editingPerson.value.id, 
        input 
      })
      $q.notify({
        type: 'positive',
        message: 'Человек успешно обновлен'
      })
    } else {
      await createPerson({ input })
      $q.notify({
        type: 'positive',
        message: 'Человек успешно создан'
      })
    }

    showCreateDialog.value = false
    resetForm()
    await refetch()
  } catch (error) {
    console.error('Ошибка сохранения человека:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении человека'
    })
  }
}

const openCreateDialog = () => {
  resetForm()
  showCreateDialog.value = true
}

// Обработка ошибок
if (error.value) {
  console.error('Ошибка загрузки людей:', error.value)
  $q.notify({
    type: 'negative',
    message: 'Ошибка при загрузке людей'
  })
}
</script>
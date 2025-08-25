<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Организации</h4>
        <p class="text-body1 text-grey-7">
          Управление государственными и коммерческими организациями
        </p>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="Добавить организацию"
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
            :options="organizationTypes"
            label="Тип организации"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
            clearable
          />
          
          <q-select
            v-model="selectedStatus"
            :options="statusOptions"
            label="Статус"
            outlined
            dense
            class="col-12 col-sm-6 col-md-4"
            clearable
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Таблица организаций -->
    <q-card>
      <q-table
        :rows="organizations"
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
              @click="editOrganization(props.row)"
            />
            <q-btn
              flat
              round
              color="negative"
              icon="delete"
              size="sm"
              @click="deleteOrganization(props.row)"
            />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Диалог создания/редактирования -->
    <q-dialog v-model="showCreateDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">
            {{ editingOrganization ? 'Редактировать' : 'Создать' }} организацию
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
            :options="organizationTypes"
            label="Тип организации"
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
          
          <q-input
            v-model="form.foundedDate"
            label="Дата основания"
            type="date"
            outlined
            dense
            class="q-mb-md"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn
            :label="editingOrganization ? 'Сохранить' : 'Создать'"
            color="primary"
            @click="saveOrganization"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Organization, OrganizationType } from '../types/graphql'

// Состояние
const loading = ref(false)
const organizations = ref<Organization[]>([])
const searchQuery = ref('')
const selectedType = ref<OrganizationType | null>(null)
const selectedStatus = ref<string | null>(null)
const showCreateDialog = ref(false)
const editingOrganization = ref<Organization | null>(null)

// Форма
const form = reactive({
  name: '',
  type: OrganizationType.COMMERCIAL,
  description: '',
  foundedDate: ''
})

// Опции
const organizationTypes = [
  { label: 'Правительственная', value: OrganizationType.GOVERNMENT },
  { label: 'Коммерческая', value: OrganizationType.COMMERCIAL },
  { label: 'Некоммерческая', value: OrganizationType.NON_PROFIT },
  { label: 'Образовательная', value: OrganizationType.EDUCATIONAL },
  { label: 'Военная', value: OrganizationType.MILITARY },
  { label: 'Религиозная', value: OrganizationType.RELIGIOUS },
  { label: 'Другая', value: OrganizationType.OTHER }
]

const statusOptions = [
  { label: 'Активная', value: 'active' },
  { label: 'Неактивная', value: 'inactive' },
  { label: 'Ликвидированная', value: 'dissolved' }
]

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true },
  { name: 'type', label: 'Тип', field: 'type', sortable: true },
  { name: 'foundedDate', label: 'Дата основания', field: 'foundedDate', sortable: true },
  { name: 'location', label: 'Местоположение', field: row => row.location?.name || '-', sortable: false },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false }
]

// Методы
const loadOrganizations = async () => {
  loading.value = true
  try {
    // TODO: Загрузка через GraphQL
    organizations.value = []
  } catch (error) {
    console.error('Ошибка загрузки организаций:', error)
  } finally {
    loading.value = false
  }
}

const editOrganization = (org: Organization) => {
  editingOrganization.value = org
  form.name = org.name
  form.type = org.type
  form.description = org.description || ''
  form.foundedDate = org.foundedDate || ''
  showCreateDialog.value = true
}

const deleteOrganization = async (org: Organization) => {
  // TODO: Удаление через GraphQL
  console.log('Удаление организации:', org.id)
}

const saveOrganization = async () => {
  try {
    // TODO: Сохранение через GraphQL
    console.log('Сохранение организации:', form)
    showCreateDialog.value = false
    await loadOrganizations()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  }
}

// Инициализация
onMounted(() => {
  loadOrganizations()
})
</script>
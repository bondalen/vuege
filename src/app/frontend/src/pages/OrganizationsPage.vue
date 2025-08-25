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
              @click="handleDeleteOrganization(props.row)"
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
              :options="organizationTypes"
              label="Тип организации *"
              outlined
              dense
              class="col-12 col-sm-6"
              :rules="[val => !!val || 'Тип обязателен']"
            />
            
            <q-input
              v-model="form.foundedDate"
              label="Дата основания"
              type="date"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-input
              v-model="form.dissolvedDate"
              label="Дата ликвидации"
              type="date"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-input
              v-model="form.locationId"
              label="ID местоположения"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-input
              v-model="form.parentOrganizationId"
              label="ID родительской организации"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-input
              v-model="form.description"
              label="Описание"
              type="textarea"
              outlined
              dense
              class="col-12"
              rows="3"
            />
          </div>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import type { Organization, OrganizationType, SearchInput } from '../types/graphql'
import { GET_ORGANIZATIONS } from '../graphql/queries'
import { CREATE_ORGANIZATION, UPDATE_ORGANIZATION, DELETE_ORGANIZATION } from '../graphql/mutations'

const $q = useQuasar()

// Состояние
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
  foundedDate: '',
  dissolvedDate: '',
  locationId: '',
  parentOrganizationId: ''
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

// Вычисляемые параметры поиска
const searchParams = computed<SearchInput>(() => ({
  query: searchQuery.value,
  filters: {
    type: selectedType.value,
    status: selectedStatus.value
  },
  pagination: {
    page: 1,
    size: 50
  }
}))

// GraphQL запросы
const { result, loading, error, refetch } = useQuery(
  GET_ORGANIZATIONS,
  { search: searchParams },
  { fetchPolicy: 'cache-and-network' }
)

// Мутации
const { mutate: createOrganization, loading: creating } = useMutation(CREATE_ORGANIZATION)
const { mutate: updateOrganization, loading: updating } = useMutation(UPDATE_ORGANIZATION)
const { mutate: deleteOrganization, loading: deleting } = useMutation(DELETE_ORGANIZATION)

// Вычисляемые данные
const organizations = computed(() => result.value?.organizations || [])

// Колонки таблицы
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
  { name: 'type', label: 'Тип', field: 'type', sortable: true, align: 'left' },
  { name: 'foundedDate', label: 'Дата основания', field: 'foundedDate', sortable: true, align: 'center' },
  { name: 'location', label: 'Местоположение', field: row => row.location?.name || '-', sortable: false, align: 'left' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Методы
const resetForm = () => {
  form.name = ''
  form.type = OrganizationType.COMMERCIAL
  form.description = ''
  form.foundedDate = ''
  form.dissolvedDate = ''
  form.locationId = ''
  form.parentOrganizationId = ''
  editingOrganization.value = null
}

const editOrganization = (org: Organization) => {
  editingOrganization.value = org
  form.name = org.name
  form.type = org.type
  form.description = org.description || ''
  form.foundedDate = org.foundedDate || ''
  form.dissolvedDate = org.dissolvedDate || ''
  form.locationId = org.location?.id || ''
  form.parentOrganizationId = org.parentOrganization?.id || ''
  showCreateDialog.value = true
}

const handleDeleteOrganization = async (org: Organization) => {
  try {
    await $q.dialog({
      title: 'Подтверждение удаления',
      message: `Вы уверены, что хотите удалить организацию "${org.name}"?`,
      cancel: true,
      persistent: true
    })

    await deleteOrganization({ id: org.id })
    
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

const saveOrganization = async () => {
  try {
    const input = {
      name: form.name,
      type: form.type,
      description: form.description || null,
      foundedDate: form.foundedDate || null,
      dissolvedDate: form.dissolvedDate || null,
      locationId: form.locationId || null,
      parentOrganizationId: form.parentOrganizationId || null
    }

    if (editingOrganization.value) {
      await updateOrganization({ 
        id: editingOrganization.value.id, 
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

// Обработка ошибок
if (error.value) {
  console.error('Ошибка загрузки организаций:', error.value)
  $q.notify({
    type: 'negative',
    message: 'Ошибка при загрузке организаций'
  })
}
</script>
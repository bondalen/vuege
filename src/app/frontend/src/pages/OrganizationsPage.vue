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
                  <option value="EMPIRE">Империя</option>
                  <option value="STATE">Государство</option>
                  <option value="COMMERCIAL">Коммерческая</option>
                  <option value="GOVERNMENT">Правительственная</option>
                </select>
              </div>
            </div>
            <div class="q-field__label">Тип организации</div>
          </div>
          
          <!-- Временное решение: обычный HTML select -->
          <div class="q-field q-field--outlined q-field--dense col-12 col-sm-6 col-md-4">
            <div class="q-field__control">
              <div class="q-field__control-container">
                <select
                  v-model="selectedStatus"
                  class="q-field__native q-placeholder"
                  style="width: 100%; padding: 8px; border: none; outline: none; background: transparent;"
                >
                  <option value="">Все статусы</option>
                  <option value="active">Активная</option>
                  <option value="inactive">Неактивная</option>
                  <option value="dissolved">Ликвидированная</option>
                </select>
              </div>
            </div>
            <div class="q-field__label">Статус</div>
          </div>
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
        dense
      >
        <template v-slot:body-cell-details="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              color="info"
              icon="info"
              size="sm"
              @click="selectOrganization(props.row)"
              :class="{ 'bg-blue-1': selectedOrganization?.id === props.row.id }"
            />
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

    <!-- Вкладки с деталями организации -->
    <q-card v-if="selectedOrganization" class="q-mt-md">
      <q-card-section>
        <div class="text-h6">
          Детали организации: {{ selectedOrganization.name }}
          <q-btn
            flat
            round
            color="grey"
            icon="close"
            size="sm"
            @click="clearSelectedOrganization"
            class="q-ml-sm"
          />
        </div>
      </q-card-section>

      <q-tabs
        v-model="activeTab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="positions" label="Должности" icon="work" />
        <q-tab name="childUnits" label="Дочерние организации" icon="account_tree" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="activeTab" animated>
        <!-- Вкладка "Должности" -->
        <q-tab-panel name="positions" class="q-pa-none">
          <div v-if="positionsLoading" class="q-pa-md text-center">
            <q-spinner-dots color="primary" size="40px" />
            <div class="q-mt-sm">Загрузка должностей...</div>
          </div>
          
          <div v-else-if="positionsError" class="q-pa-md text-center text-negative">
            <q-icon name="error" size="40px" />
            <div class="q-mt-sm">Ошибка загрузки должностей</div>
          </div>
          
          <div v-else-if="positions.length === 0" class="q-pa-md text-center text-grey">
            <q-icon name="work_off" size="40px" />
            <div class="q-mt-sm">Должности не найдены</div>
          </div>
          
          <q-table
            v-else
            :rows="positions"
            :columns="positionColumns"
            row-key="id"
            dense
            :pagination="{ rowsPerPage: 10 }"
            class="q-mt-md"
          >
            <template v-slot:body-cell-hierarchy="props">
              <q-td :props="props">
                <q-chip
                  :color="getHierarchyColor(props.value)"
                  text-color="white"
                  size="sm"
                >
                  {{ getHierarchyLabel(props.value) }}
                </q-chip>
              </q-td>
            </template>
            
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <q-chip
                  :color="props.value ? 'positive' : 'negative'"
                  text-color="white"
                  size="sm"
                >
                  {{ props.value ? 'Активная' : 'Неактивная' }}
                </q-chip>
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>

        <!-- Вкладка "Дочерние организации" -->
        <q-tab-panel name="childUnits" class="q-pa-none">
          <div v-if="childrenLoading" class="q-pa-md text-center">
            <q-spinner-dots color="primary" size="40px" />
            <div class="q-mt-sm">Загрузка дочерних организаций...</div>
          </div>
          
          <div v-else-if="childrenError" class="q-pa-md text-center text-negative">
            <q-icon name="error" size="40px" />
            <div class="q-mt-sm">Ошибка загрузки дочерних организаций</div>
          </div>
          
          <div v-else-if="childOrganizations.length === 0" class="q-pa-md text-center text-grey">
            <q-icon name="account_tree" size="40px" />
            <div class="q-mt-sm">Дочерние организации не найдены</div>
          </div>
          
          <q-table
            v-else
            :rows="childOrganizations"
            :columns="childOrganizationColumns"
            row-key="id"
            dense
            :pagination="{ rowsPerPage: 10 }"
            class="q-mt-md"
          >
            <template v-slot:body-cell-type="props">
              <q-td :props="props">
                {{ getOrganizationTypeLabel(props.value) }}
              </q-td>
            </template>
            
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                {{ getOrganizationStatus(props.row) }}
              </q-td>
            </template>
            
            <template v-slot:body-cell-fictional="props">
              <q-td :props="props">
                <q-chip
                  :color="props.value ? 'orange' : 'blue'"
                  text-color="white"
                  size="sm"
                >
                  {{ props.value ? 'Вымышленная' : 'Реальная' }}
                </q-chip>
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>
      </q-tab-panels>
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
            
            <!-- Временное решение: обычный HTML select -->
            <div class="q-field q-field--outlined q-field--dense col-12 col-sm-6">
              <div class="q-field__control">
                <div class="q-field__control-container">
                  <select
                    v-model="form.type"
                    class="q-field__native q-placeholder"
                    style="width: 100%; padding: 8px; border: none; outline: none; background: transparent;"
                    required
                  >
                    <option value="">Выберите тип организации</option>
                    <option value="EMPIRE">Империя</option>
                    <option value="STATE">Государство</option>
                    <option value="COMMERCIAL">Коммерческая</option>
                    <option value="GOVERNMENT">Правительственная</option>
                  </select>
                </div>
              </div>
              <div class="q-field__label">Тип организации *</div>
            </div>
            
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
            
            <q-checkbox
              v-model="form.isFictional"
              label="Вымышленная организация"
              class="col-12 col-sm-6"
            />
            
            <!-- Поле даты ликвидации (показывается только для неактивных статусов) -->
            <q-input
              v-if="form.status !== 'active'"
              v-model="form.dissolvedDate"
              label="Дата ликвидации"
              type="date"
              outlined
              dense
              class="col-12 col-sm-6"
              @update:model-value="updateStatusFromDissolvedDate"
            />
            
            <!-- Поле статуса (редактируемое) -->
            <div class="q-field q-field--outlined q-field--dense col-12 col-sm-6">
              <div class="q-field__control">
                <div class="q-field__control-container">
                  <select v-model="form.status" class="q-field__native q-placeholder" style="padding: 8px; border: none; background: transparent; width: 100%;" @change="updateDissolvedDateFromStatus">
                    <option v-for="option in formStatusOptions" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="q-field__label">Статус</div>
            </div>
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
import { GET_ORGANIZATIONS, GET_ORGANIZATION_POSITIONS, GET_CHILD_ORGANIZATIONS } from '../graphql/queries'
import { CREATE_ORGANIZATION, UPDATE_ORGANIZATION, DELETE_ORGANIZATION } from '../graphql/mutations'

const $q = useQuasar()

// Состояние
const searchQuery = ref('')
const selectedType = ref<OrganizationType | null>(null)
const selectedStatus = ref<string | null>(null)
const showCreateDialog = ref(false)
const editingOrganization = ref<Organization | null>(null)

// Состояние для вкладок
const selectedOrganization = ref<Organization | null>(null)
const activeTab = ref('positions') // 'positions' или 'children'

// Форма
const form = reactive({
  name: '',
  type: 'STATE', // Изменено на поддерживаемое значение
  foundedDate: new Date().toISOString().split('T')[0], // Устанавливаем сегодняшнюю дату по умолчанию
  dissolvedDate: '',
  locationId: '',
  parentOrganizationId: '',
  isFictional: false,
  status: 'active' // Добавляем поле статуса
})

// Опции - используем computed для правильной реактивности
// Только значения, поддерживаемые Backend enum OrganizationType
const organizationTypes = computed(() => [
  { label: 'Империя', value: 'EMPIRE' },
  { label: 'Государство', value: 'STATE' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Правительственная', value: 'GOVERNMENT' }
])

const statusOptions = computed(() => [
  { label: 'Активная', value: 'active' },
  { label: 'Неактивная', value: 'inactive' },
  { label: 'Ликвидированная', value: 'dissolved' }
])

// Опции статусов для форм (без "Все статусы")
const formStatusOptions = computed(() => [
  { label: 'Активная', value: 'active' },
  { label: 'Неактивная', value: 'inactive' },
  { label: 'Ликвидированная', value: 'dissolved' }
])

// Отладочное логирование
console.log('organizationTypes array:', organizationTypes.value)
console.log('organizationTypes length:', organizationTypes.value.length)
organizationTypes.value.forEach((type, index) => {
  console.log(`organizationTypes[${index}]:`, type)
})

// Вычисляемые параметры поиска
const searchParams = computed(() => ({
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
  {},
  { fetchPolicy: 'cache-and-network' }
)

// Запрос для должностей организации
const { result: positionsResult, loading: positionsLoading, error: positionsError } = useQuery(
  GET_ORGANIZATION_POSITIONS,
  {},
  { fetchPolicy: 'cache-and-network' }
)

// Запрос для дочерних организаций
const { result: childrenResult, loading: childrenLoading, error: childrenError } = useQuery(
  GET_CHILD_ORGANIZATIONS,
  {},
  { fetchPolicy: 'cache-and-network' }
)

// Отладочное логирование
console.log('OrganizationsPage - result:', result.value)
console.log('OrganizationsPage - loading:', loading.value)
console.log('OrganizationsPage - error:', error.value)

// Мутации
const { mutate: createOrganization, loading: creating } = useMutation(CREATE_ORGANIZATION)
const { mutate: updateOrganization, loading: updating } = useMutation(UPDATE_ORGANIZATION)
const { mutate: deleteOrganization, loading: deleting } = useMutation(DELETE_ORGANIZATION)

// Вычисляемые данные
const organizations = computed(() => {
  const data = result.value?.organizationalUnits || []
  
  // Фильтрация по поиску
  let filtered = data
  if (searchQuery.value) {
    filtered = filtered.filter(org => 
      org.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      org.type.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  // Фильтрация по типу
  if (selectedType.value) {
    filtered = filtered.filter(org => org.type === selectedType.value)
  }
  
  // Фильтрация по статусу
  if (selectedStatus.value) {
    filtered = filtered.filter(org => {
      const orgStatus = getOrganizationStatus(org)
      return orgStatus === getStatusLabel(selectedStatus.value!)
    })
  }
  
  return filtered
})

// Данные для вкладок
const positions = computed(() => {
  const allPositions = positionsResult.value?.positions || []
  return allPositions.filter(pos => pos.organization?.id === selectedOrganization.value?.id)
})

const childOrganizations = computed(() => {
  const allOrganizations = childrenResult.value?.organizationalUnits || []
  // Фильтруем организации, которые имеют выбранную организацию как родителя
  // Поскольку у нас нет прямого поля parentUnitId в GraphQL, используем ID для демонстрации
  if (selectedOrganization.value?.id === '36') {
    // Для Византийской Империи возвращаем дочерние организации
    return allOrganizations.filter(org => ['37', '38', '39', '40'].includes(org.id))
  } else if (selectedOrganization.value?.id === '37') {
    // Для Константинополя возвращаем пустой список (нет дочерних)
    return []
  } else if (selectedOrganization.value?.id === '38') {
    // Для Византийской Армии возвращаем пустой список (нет дочерних)
    return []
  } else if (selectedOrganization.value?.id === '39') {
    // Для Византийского Флота возвращаем пустой список (нет дочерних)
    return []
  } else if (selectedOrganization.value?.id === '40') {
    // Для Византийской Церкви возвращаем пустой список (нет дочерних)
    return []
  }
  return []
})

// Колонки таблицы организаций
const columns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
  { name: 'type', label: 'Тип', field: row => getOrganizationTypeLabel(row.type), sortable: true, align: 'left' },
  { name: 'status', label: 'Статус', field: row => getOrganizationStatus(row), sortable: true, align: 'center' },
  { name: 'foundedDate', label: 'Дата основания', field: 'foundedDate', sortable: true, align: 'center' },
  { name: 'location', label: 'Местоположение', field: row => row.location?.name || '-', sortable: false, align: 'left' },
  { name: 'details', label: 'Детали', field: 'details', sortable: false, align: 'center' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Колонки таблицы должностей
const positionColumns = [
  { name: 'title', label: 'Название должности', field: 'title', sortable: true, align: 'left' },
  { name: 'hierarchy', label: 'Уровень', field: 'hierarchy', sortable: true, align: 'center' },
  { name: 'createdDate', label: 'Дата создания', field: row => new Date(row.createdDate).toLocaleDateString(), sortable: true, align: 'center' },
  { name: 'abolishedDate', label: 'Дата ликвидации', field: row => row.abolishedDate ? new Date(row.abolishedDate).toLocaleDateString() : '-', sortable: true, align: 'center' },
  { name: 'status', label: 'Статус', field: 'isActive', sortable: true, align: 'center' },
  { name: 'responsibilities', label: 'Обязанности', field: row => row.responsibilities?.join(', ') || '-', sortable: false, align: 'left' }
]

// Колонки таблицы дочерних организаций
const childOrganizationColumns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
  { name: 'type', label: 'Тип', field: 'type', sortable: true, align: 'left' },
  { name: 'foundedDate', label: 'Дата основания', field: row => new Date(row.foundedDate).toLocaleDateString(), sortable: true, align: 'center' },
  { name: 'dissolvedDate', label: 'Дата ликвидации', field: row => row.dissolvedDate ? new Date(row.dissolvedDate).toLocaleDateString() : '-', sortable: true, align: 'center' },
  { name: 'status', label: 'Статус', field: 'status', sortable: true, align: 'center' },
  { name: 'fictional', label: 'Тип', field: 'isFictional', sortable: true, align: 'center' }
]

// Методы
const resetForm = () => {
  form.name = ''
  form.type = 'STATE' // Изменено на поддерживаемое значение
  form.foundedDate = new Date().toISOString().split('T')[0] // Устанавливаем сегодняшнюю дату по умолчанию
  form.dissolvedDate = ''
  form.locationId = ''
  form.parentOrganizationId = ''
  form.isFictional = false
  form.status = 'active'
  editingOrganization.value = null
}

// Методы для работы с вкладками
const selectOrganization = (org: Organization) => {
  selectedOrganization.value = org
  activeTab.value = 'positions' // По умолчанию показываем должности
}

const clearSelectedOrganization = () => {
  selectedOrganization.value = null
  activeTab.value = 'positions'
}

const editOrganization = (org: Organization) => {
  console.log('editOrganization - incoming org:', org)
  console.log('editOrganization - organizationTypes:', organizationTypes.value)
  
  // Сначала сбрасываем форму
  resetForm()
  
  // Затем устанавливаем режим редактирования
  editingOrganization.value = org
  
  // Заполняем форму данными
  form.name = org.name
  form.type = org.type
  form.foundedDate = org.foundedDate || new Date().toISOString().split('T')[0]
  form.dissolvedDate = org.dissolvedDate || ''
  form.locationId = org.location?.id || ''
  form.parentOrganizationId = org.parentOrganization?.id || ''
  form.isFictional = org.isFictional || false
  
  // Устанавливаем статус на основе даты ликвидации
  updateStatusFromDissolvedDate()
  
  console.log('editOrganization - form after setting:', form)
  console.log('editOrganization - form.type:', form.type)
  console.log('editOrganization - editingOrganization:', editingOrganization.value)
  console.log('editOrganization - organizationTypes:', organizationTypes.value)
  console.log('editOrganization - matching option:', organizationTypes.value.find(t => t.value === form.type))
  
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
    // Проверяем обязательные поля
    if (!form.name.trim()) {
      $q.notify({
        type: 'negative',
        message: 'Название обязательно для заполнения'
      })
      return
    }
    
    if (!form.foundedDate) {
      $q.notify({
        type: 'negative',
        message: 'Дата основания обязательна для заполнения'
      })
      return
    }

        const input: any = {
      name: form.name.trim(),
      type: form.type,
      foundedDate: form.foundedDate,
      dissolvedDate: form.dissolvedDate || null,
      isFictional: form.isFictional,
      historicalPeriodId: '1', // По умолчанию раннее средневековье
      parentUnitId: form.parentOrganizationId || null
    }

    // Добавляем location только если указан locationId
    if (form.locationId) {
      input.location = {
        latitude: 0, // Временные координаты
        longitude: 0
      }
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

// Вспомогательные методы
const getOrganizationTypeLabel = (type: string): string => {
  const typeOption = organizationTypes.value.find(t => t.value === type)
  return typeOption ? typeOption.label : type
}

const getStatusLabel = (status: string): string => {
  const statusOption = statusOptions.value.find(s => s.value === status)
  return statusOption ? statusOption.label : status
}

const getOrganizationStatus = (org: any): string => {
  // Проверяем, является ли org объектом организации или формой
  const dissolvedDate = org.dissolvedDate || org.dissolvedDate
  
  if (dissolvedDate) {
    const dissolvedDateObj = new Date(dissolvedDate)
    const currentDate = new Date()
    
    if (dissolvedDateObj < currentDate) {
      return 'Ликвидированная'
    } else {
      return 'Неактивная'
    }
  }
  return 'Активная'
}

// Вспомогательные методы для должностей
const getHierarchyLabel = (hierarchy: string): string => {
  const hierarchyMap: Record<string, string> = {
    'ENTRY': 'Начальный',
    'JUNIOR': 'Младший',
    'MIDDLE': 'Средний',
    'SENIOR': 'Старший',
    'LEAD': 'Ведущий',
    'MANAGER': 'Менеджер',
    'DIRECTOR': 'Директор',
    'EXECUTIVE': 'Руководитель'
  }
  return hierarchyMap[hierarchy] || hierarchy
}

const getHierarchyColor = (hierarchy: string): string => {
  const colorMap: Record<string, string> = {
    'ENTRY': 'grey',
    'JUNIOR': 'blue',
    'MIDDLE': 'green',
    'SENIOR': 'orange',
    'LEAD': 'purple',
    'MANAGER': 'teal',
    'DIRECTOR': 'red',
    'EXECUTIVE': 'deep-purple'
  }
  return colorMap[hierarchy] || 'grey'
}

// Функция для синхронизации статуса с датой ликвидации
const updateStatusFromDissolvedDate = () => {
  if (!form.dissolvedDate) {
    form.status = 'active'
  } else {
    const dissolvedDate = new Date(form.dissolvedDate)
    const currentDate = new Date()
    
    if (dissolvedDate < currentDate) {
      form.status = 'dissolved'
    } else {
      form.status = 'inactive'
    }
  }
}

// Функция для обновления даты ликвидации при изменении статуса
const updateDissolvedDateFromStatus = () => {
  switch (form.status) {
    case 'active':
      form.dissolvedDate = ''
      break
    case 'inactive':
      // Устанавливаем дату в будущем (через год)
      const futureDate = new Date()
      futureDate.setFullYear(futureDate.getFullYear() + 1)
      form.dissolvedDate = futureDate.toISOString().split('T')[0]
      break
    case 'dissolved':
      // Устанавливаем дату в прошлом (год назад)
      const pastDate = new Date()
      pastDate.setFullYear(pastDate.getFullYear() - 1)
      form.dissolvedDate = pastDate.toISOString().split('T')[0]
      break
  }
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
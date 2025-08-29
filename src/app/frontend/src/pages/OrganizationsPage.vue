<template>
  <q-page class="q-pa-sm-md q-pa-xs-sm organizations-page">
    <!-- Заголовки -->
    <div class="text-center page-titles">
      <h4 class="text-h4 q-ma-xs">Организации</h4>
      <p class="text-body1 text-grey-7 q-ma-xs">
        Управление государственными и коммерческими организациями
      </p>
    </div>

    <!-- Фильтры и кнопка добавления -->
    <q-card class="filter-card" style="width: 100%; max-width: 2880px; margin-bottom: 3px;">
      <q-card-section class="q-pa-sm">
        <!-- Верхняя строка: поиск и кнопка добавления -->
        <div class="row q-gutter-md q-mb-sm" style="display: flex; align-items: center;">
          <q-input
            v-model="searchQuery"
            label="Поиск"
            outlined
            dense
            style="flex: 2; margin-right: 8px;"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          
          <q-btn
            color="primary"
            icon="add"
            :label="buttonLabel"
            @click="openCreateDialog"
            style="flex: 1;"
            dense
            class="add-organization-btn"
          />
        </div>
        
        <!-- Нижняя строка: комбобоксы фильтров -->
        <div class="row q-gutter-md" style="display: flex; align-items: center;">
          <q-select
            v-model="selectedType"
            :options="organizationTypeOptions"
            label="Тип организации"
            outlined
            dense
            dark
            clearable
            option-value="value"
            option-label="label"
            emit-value
            map-options
            class="filter-select"
            style="flex: 2; margin-right: 8px; background-color: #f5f5f5;"
          />
          
          <q-select
            v-model="selectedStatus"
            :options="organizationStatusOptions"
            label="Статус"
            outlined
            dense
            dark
            clearable
            option-value="value"
            option-label="label"
            emit-value
            map-options
            class="filter-select"
            style="flex: 1; background-color: #f5f5f5;"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Таблица организаций -->
    <q-card class="table-card" style="width: 100%; max-width: 2880px; margin-bottom: 3px;">
      <q-table
        :rows="organizations"
        :columns="columns"
        :loading="loading"
        row-key="id"
        :pagination="{ rowsPerPage: 10 }"
        dense
        :class="{ 'selected-row-highlight': true }"
      >
        <template v-slot:body="props">
          <q-tr
            :props="props"
            :class="{ 'bg-blue-1': selectedOrganization?.id === props.row.id }"
            @click="selectOrganization(props.row)"
            style="cursor: pointer;"
          >
            <q-td key="name" :props="props">
              {{ props.row.name }}
            </q-td>
            <q-td key="type" :props="props">
              {{ getOrganizationTypeLabel(props.row.type) }}
            </q-td>
            <q-td key="status" :props="props">
              {{ getOrganizationStatus(props.row) }}
            </q-td>
            <q-td key="foundedDate" :props="props">
              {{ props.row.foundedDate }}
            </q-td>
            <q-td key="location" :props="props">
              {{ props.row.location?.name || '-' }}
            </q-td>
            <q-td key="details" :props="props">
              <q-btn
                flat
                round
                color="info"
                icon="info"
                size="sm"
                @click.stop="selectOrganization(props.row)"
                :class="{ 'bg-blue-1': selectedOrganization?.id === props.row.id }"
              />
            </q-td>
            <q-td key="actions" :props="props">
              <q-btn
                flat
                round
                color="primary"
                icon="edit"
                size="sm"
                @click.stop="editOrganization(props.row)"
              />
              <q-btn
                flat
                round
                color="negative"
                icon="delete"
                size="sm"
                @click.stop="handleDeleteOrganization(props.row)"
              />
            </q-td>
          </q-tr>
        </template>

      </q-table>
    </q-card>

    <!-- Вкладки с деталями организации -->
    <q-card v-if="selectedOrganization" class="tabs-card" style="width: 100%; max-width: 2880px;">
      <q-card-section style="padding: 8px 16px; background-color: #e3f2fd;">
        <div style="display: flex; justify-content: space-between; align-items: center; height: 40px; font-size: 14px; color: #1976d2;">
          <span>Детали организации: {{ selectedOrganization.name }}</span>
          <q-btn
            flat
            round
            color="grey-7"
            icon="close"
            size="sm"
            @click="clearSelectedOrganization"
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
          
          <div v-else>
            <div class="q-mb-md">
              <q-btn
                color="primary"
                icon="add"
                label="Добавить должность"
                @click="openCreatePositionDialog"
                dense
                size="sm"
              />
            </div>
            
            <q-table
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
              
                          <template v-slot:body-cell-actions="props">
              <q-td :props="props">
                <q-btn
                  flat
                  round
                  color="primary"
                  icon="edit"
                  size="sm"
                  @click="editPosition(props.row)"
                />
                <q-btn
                  flat
                  round
                  color="negative"
                  icon="delete"
                  size="sm"
                  @click="deletePosition(props.row)"
                />
              </q-td>
            </template>
            </q-table>
          </div>
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
          
          <div v-else>
            <div class="q-mb-md">
              <q-btn
                color="primary"
                icon="add"
                label="Добавить дочернюю организацию"
                @click="openCreateChildOrganizationDialog"
                dense
                size="sm"
              />
            </div>
            
            <q-table
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
            
            <template v-slot:body-cell-actions="props">
              <q-td :props="props">
                <q-btn
                  flat
                  round
                  color="primary"
                  icon="edit"
                  size="sm"
                  @click="editChildOrganization(props.row)"
                />
                <q-btn
                  flat
                  round
                  color="negative"
                  icon="delete"
                  size="sm"
                  @click="deleteChildOrganization(props.row)"
                />
              </q-td>
            </template>
          </q-table>
            </div>
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
            
            <q-select
              v-model="form.type"
              :options="organizationTypes"
              label="Тип организации *"
              outlined
              dense
              dark
              clearable
              option-value="value"
              option-label="label"
              emit-value
              map-options
              class="col-12 col-sm-6"
              style="background-color: #f5f5f5;"
              :rules="[val => !!val || 'Тип организации обязателен']"
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
            
            <!-- Поле статуса -->
            <q-select
              v-model="form.status"
              :options="formStatusOptions"
              label="Статус"
              outlined
              dense
              dark
              clearable
              option-value="value"
              option-label="label"
              emit-value
              map-options
              class="col-12 col-sm-6"
              style="background-color: #f5f5f5;"
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

    <!-- Диалог для создания/редактирования должности -->
    <q-dialog v-model="showPositionDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">
            {{ editingPosition ? 'Редактировать должность' : 'Создать должность' }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="positionForm.title"
            label="Название должности"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-select
            v-model="positionForm.hierarchy"
            :options="hierarchyOptions"
            label="Уровень иерархии"
            outlined
            dense
            dark
            clearable
            option-value="value"
            option-label="label"
            emit-value
            map-options
            class="q-mb-md"
            style="background-color: #f5f5f5;"
          />
          
          <q-input
            v-model="positionForm.responsibilities"
            label="Обязанности"
            type="textarea"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-toggle
            v-model="positionForm.isActive"
            label="Активная должность"
            color="primary"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" @click="showPositionDialog = false" />
          <q-btn
            :label="editingPosition ? 'Сохранить' : 'Создать'"
            color="primary"
            @click="savePosition"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Диалог для создания/редактирования дочерней организации -->
    <q-dialog v-model="showChildOrganizationDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">
            {{ editingChildOrganization ? 'Редактировать дочернюю организацию' : 'Создать дочернюю организацию' }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="row q-gutter-md">
            <q-input
              v-model="childOrganizationForm.name"
              label="Название организации *"
              outlined
              dense
              class="col-12"
              :rules="[val => !!val || 'Название обязательно']"
            />
            
            <q-select
              v-model="childOrganizationForm.type"
              :options="organizationTypes"
              label="Тип организации *"
              outlined
              dense
              dark
              clearable
              option-value="value"
              option-label="label"
              emit-value
              map-options
              class="col-12 col-sm-6"
              style="background-color: #f5f5f5;"
              :rules="[val => !!val || 'Тип организации обязателен']"
            />
            
            <q-input
              v-model="childOrganizationForm.foundedDate"
              label="Дата основания *"
              type="date"
              outlined
              dense
              class="col-12 col-sm-6"
              :rules="[val => !!val || 'Дата основания обязательна']"
            />
            
            <q-input
              v-model="childOrganizationForm.dissolvedDate"
              label="Дата ликвидации"
              type="date"
              outlined
              dense
              class="col-12 col-sm-6"
            />
            
            <q-checkbox
              v-model="childOrganizationForm.isFictional"
              label="Вымышленная организация"
              class="col-12 col-sm-6"
            />
            
            <q-select
              v-model="childOrganizationForm.status"
              :options="formStatusOptions"
              label="Статус"
              outlined
              dense
              dark
              clearable
              option-value="value"
              option-label="label"
              emit-value
              map-options
              class="col-12 col-sm-6"
              style="background-color: #f5f5f5;"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" @click="showChildOrganizationDialog = false" />
          <q-btn
            :label="editingChildOrganization ? 'Сохранить' : 'Создать'"
            color="primary"
            @click="saveChildOrganization"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import type { Organization, OrganizationType, SearchInput, PositionHierarchy, PositionInput } from '../types/graphql'
import { GET_ORGANIZATIONS, GET_ORGANIZATION_POSITIONS, GET_CHILD_ORGANIZATIONS } from '../graphql/queries'
import { CREATE_ORGANIZATION, UPDATE_ORGANIZATION, DELETE_ORGANIZATION, CREATE_POSITION, UPDATE_POSITION, DELETE_POSITION } from '../graphql/mutations'

const $q = useQuasar()

// Состояние
const searchQuery = ref('')
const selectedType = ref<OrganizationType | null>(null)
const selectedStatus = ref<string | null>(null)
const showCreateDialog = ref(false)
const editingOrganization = ref<Organization | null>(null)
const selectedOrganization = ref<Organization | null>(null)
const screenWidth = ref(window.innerWidth)

// Состояние для вкладок
const activeTab = ref('positions') // 'positions' или 'children'

// Состояние для диалогов должностей и дочерних организаций
const showPositionDialog = ref(false)
const showChildOrganizationDialog = ref(false)
const editingPosition = ref<any>(null)
const editingChildOrganization = ref<any>(null)

// Форма
const form = reactive({
  name: '',
  type: 'STATE', // Изменено на поддерживаемое значение
  foundedDate: new Date().toISOString().split('T')[0], // Устанавливаем сегодняшнюю дату по умолчанию
  dissolvedDate: '',
  parentOrganizationId: '',
  isFictional: false,
  status: 'active' // Добавляем поле статуса
})

// Форма для должности
const positionForm = reactive({
  title: '',
  hierarchy: 'ADMINISTRATIVE',
  responsibilities: '',
  isActive: true
})

// Форма для дочерней организации
const childOrganizationForm = reactive({
  name: '',
  type: 'STATE',
  foundedDate: new Date().toISOString().split('T')[0],
  dissolvedDate: '',
  isFictional: false,
  status: 'active'
})

// Опции для иерархии должностей
const hierarchyOptions = [
  { label: 'Исполнительная', value: 'EXECUTIVE' },
  { label: 'Законодательная', value: 'LEGISLATIVE' },
  { label: 'Судебная', value: 'JUDICIAL' },
  { label: 'Административная', value: 'ADMINISTRATIVE' },
  { label: 'Операционная', value: 'OPERATIONAL' }
]

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

// Опции для фильтров (с пустым значением "Все")
const organizationTypeOptions = computed(() => [
  { label: 'Все типы', value: null },
  { label: 'Империя', value: 'EMPIRE' },
  { label: 'Государство', value: 'STATE' },
  { label: 'Коммерческая', value: 'COMMERCIAL' },
  { label: 'Правительственная', value: 'GOVERNMENT' }
])

const organizationStatusOptions = computed(() => [
  { label: 'Все статусы', value: null },
  { label: 'Активная', value: 'active' },
  { label: 'Неактивная', value: 'inactive' },
  { label: 'Ликвидированная', value: 'dissolved' }
])

// Адаптивная кнопка
const buttonLabel = computed(() => {
  const isMobile = screenWidth.value <= 768
  return isMobile ? 'Добавить' : 'Добавить организацию'
})

// Обработчик изменения размера экрана
const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth
}

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('resize', updateScreenWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth)
})

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
const { result: positionsResult, loading: positionsLoading, error: positionsError, refetch: refetchPositions } = useQuery(
  GET_ORGANIZATION_POSITIONS,
  {},
  { fetchPolicy: 'cache-and-network' }
)

// Запрос для дочерних организаций
const { result: childrenResult, loading: childrenLoading, error: childrenError, refetch: refetchChildren } = useQuery(
  GET_CHILD_ORGANIZATIONS,
  {},
  { fetchPolicy: 'cache-and-network' }
)

// Отладочное логирование
console.log('OrganizationsPage - result:', result.value)
console.log('OrganizationsPage - loading:', loading.value)
console.log('OrganizationsPage - error:', error.value)

// Отладочная информация о данных организаций
if (result.value?.organizationalUnits) {
  console.log('Доступные организации:', result.value.organizationalUnits.length)
  result.value.organizationalUnits.forEach((org, index) => {
    console.log(`Организация ${index}:`, org.name, 'тип:', org.type)
  })
}

// Мутации
const { mutate: createOrganization, loading: creating } = useMutation(CREATE_ORGANIZATION)
const { mutate: updateOrganization, loading: updating } = useMutation(UPDATE_ORGANIZATION)
const { mutate: deleteOrganization, loading: deleting } = useMutation(DELETE_ORGANIZATION)

// Мутации для должностей
const { mutate: createPosition } = useMutation(CREATE_POSITION)
const { mutate: updatePosition } = useMutation(UPDATE_POSITION)
const { mutate: deletePositionMutation } = useMutation(DELETE_POSITION)

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
  if (selectedType.value !== null && selectedType.value !== undefined) {
    console.log('Фильтрация по типу:', selectedType.value, 'тип:', typeof selectedType.value)
    filtered = filtered.filter(org => {
      console.log('Сравниваем:', org.type, 'с', selectedType.value, 'результат:', org.type === selectedType.value)
      return org.type === selectedType.value
    })
    console.log('Организации после фильтрации по типу:', filtered.length)
  }
  
  // Фильтрация по статусу
  if (selectedStatus.value !== null && selectedStatus.value !== undefined) {
    console.log('Фильтрация по статусу:', selectedStatus.value)
    filtered = filtered.filter(org => {
      const orgStatus = getOrganizationStatus(org)
      return orgStatus === getStatusLabel(selectedStatus.value!)
    })
    console.log('Организации после фильтрации по статусу:', filtered.length)
  }
  
  return filtered
})

// Данные для вкладок
const positions = computed(() => {
  if (!selectedOrganization.value) return []
  
  const allPositions = positionsResult.value?.positions || []
  const filtered = allPositions.filter(pos => pos.organization?.id === selectedOrganization.value?.id)
  
  console.log('positions computed - selectedOrganization:', selectedOrganization.value?.id)
  console.log('positions computed - allPositions:', allPositions.length)
  console.log('positions computed - filtered:', filtered.length)
  
  return filtered
})

const childOrganizations = computed(() => {
  if (!selectedOrganization.value) return []
  
  const allOrganizations = childrenResult.value?.organizationalUnits || []
  // Фильтруем организации, которые имеют выбранную организацию как родителя
  const filtered = allOrganizations.filter(org => 
    org.parentUnit?.id === selectedOrganization.value?.id
  )
  
  console.log('childOrganizations computed - selectedOrganization:', selectedOrganization.value?.id)
  console.log('childOrganizations computed - allOrganizations:', allOrganizations.length)
  console.log('childOrganizations computed - filtered:', filtered.length)
  
  return filtered
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
  { name: 'responsibilities', label: 'Обязанности', field: row => row.responsibilities?.join(', ') || '-', sortable: false, align: 'left' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Колонки таблицы дочерних организаций
const childOrganizationColumns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true, align: 'left' },
  { name: 'type', label: 'Тип', field: 'type', sortable: true, align: 'left' },
  { name: 'foundedDate', label: 'Дата основания', field: row => new Date(row.foundedDate).toLocaleDateString(), sortable: true, align: 'center' },
  { name: 'dissolvedDate', label: 'Дата ликвидации', field: row => row.dissolvedDate ? new Date(row.dissolvedDate).toLocaleDateString() : '-', sortable: true, align: 'center' },
  { name: 'status', label: 'Статус', field: 'status', sortable: true, align: 'center' },
  { name: 'fictional', label: 'Тип', field: 'isFictional', sortable: true, align: 'center' },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false, align: 'center' }
]

// Методы
const resetForm = () => {
  form.name = ''
  form.type = 'STATE' // Изменено на поддерживаемое значение
  form.foundedDate = new Date().toISOString().split('T')[0] // Устанавливаем сегодняшнюю дату по умолчанию
  form.dissolvedDate = ''
  form.parentOrganizationId = ''
  form.isFictional = false
  form.status = 'active'
  editingOrganization.value = null
}

// Методы для работы с вкладками
const selectOrganization = (org: Organization) => {
  // Если нажимаем на ту же организацию - скрываем вкладки
  if (selectedOrganization.value?.id === org.id) {
    selectedOrganization.value = null
    activeTab.value = 'positions'
  } else {
    // Если нажимаем на другую организацию - показываем её данные
    selectedOrganization.value = org
    activeTab.value = 'positions' // По умолчанию показываем должности
    
    // Принудительно обновляем данные для новой организации
    console.log('Выбрана новая организация:', org.name, 'ID:', org.id)
    console.log('positionsResult.value:', positionsResult.value)
    console.log('childrenResult.value:', childrenResult.value)
  }
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
  form.parentOrganizationId = org.parentOrganization?.id || ''
  form.isFictional = org.isFictional || false
  

  
  console.log('editOrganization - form after setting:', form)
  console.log('editOrganization - form.type:', form.type)
  console.log('editOrganization - editingOrganization:', editingOrganization.value)
  console.log('editOrganization - organizationTypes:', organizationTypes.value)
  console.log('editOrganization - matching option:', organizationTypes.value.find(t => t.value === form.type))
  
  showCreateDialog.value = true
}

const handleDeleteOrganization = async (org: Organization) => {
  console.log('=== НАЧАЛО handleDeleteOrganization ===')
  console.log('Организация:', org.name, 'ID:', org.id)
  console.log('$q доступен:', !!$q)
  console.log('$q.dialog доступен:', !!$q?.dialog)
  
  try {
    console.log('Показываем диалог подтверждения...')
    
    // Показываем диалог подтверждения с обработчиками
    const confirmed = await new Promise((resolve) => {
      $q.dialog({
        title: 'Подтверждение удаления',
        message: `Вы уверены, что хотите удалить организацию "${org.name}"?`,
        ok: {
          label: 'Удалить',
          color: 'negative'
        },
        cancel: {
          label: 'Отмена',
          color: 'primary'
        },
        persistent: true
      }).onOk(() => {
        console.log('Пользователь нажал OK')
        resolve(true)
      }).onCancel(() => {
        console.log('Пользователь нажал Отмена')
        resolve(false)
      }).onDismiss(() => {
        console.log('Диалог закрыт')
        resolve(false)
      })
    })

    console.log('Результат диалога:', confirmed)
    
    if (confirmed) {
      console.log('Пользователь подтвердил удаление, выполняем удаление...')
      await deleteOrganization({ id: org.id })
    } else {
      console.log('Пользователь отменил удаление')
      return
    }
    
    console.log('Удаление выполнено успешно')
    
    $q.notify({
      type: 'positive',
      message: 'Организация успешно удалена'
    })
    
    // Обновляем все данные
    await refetch() // Обновляем основной список организаций
    await refetchChildren() // Обновляем данные дочерних организаций
    await refetchPositions() // Обновляем данные должностей
  } catch (error) {
    console.log('=== ОШИБКА В handleDeleteOrganization ===')
    console.log('Тип ошибки:', typeof error)
    console.log('Название ошибки:', error.name)
    console.log('Сообщение ошибки:', error.message)
    console.log('Полная ошибка:', error)
    
    console.error('Ошибка удаления организации:', error)
    
    // Проверяем тип ошибки
    let errorMessage = 'Ошибка при удалении организации'
    if (error.message?.includes('not found') || error.message?.includes('не найдена')) {
      errorMessage = 'Организация уже удалена или не найдена'
    } else if (error.message?.includes('permission') || error.message?.includes('доступ')) {
      errorMessage = 'Нет прав для удаления организации'
    }
    
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  }
  
  console.log('=== КОНЕЦ handleDeleteOrganization ===')
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

    // Извлекаем значение type, если это объект
    const typeValue = typeof form.type === 'object' 
      ? form.type.value 
      : form.type

    // Извлекаем значение status, если это объект (для логики фронтенда)
    const statusValue = typeof form.status === 'object' 
      ? form.status.value 
      : form.status

    console.log('Данные формы для отправки:', {
      name: form.name.trim(),
      type: typeValue,
      status: statusValue,
      foundedDate: form.foundedDate,
      dissolvedDate: form.dissolvedDate || null,
      isFictional: form.isFictional,
      historicalPeriodId: '1',
      parentUnitId: form.parentOrganizationId || null
    })

    const input: any = {
      name: form.name.trim(),
      type: typeValue,
      foundedDate: form.foundedDate,
      dissolvedDate: form.dissolvedDate || null,
      isFictional: form.isFictional,
      historicalPeriodId: '1', // По умолчанию раннее средневековье
      parentUnitId: form.parentOrganizationId || null
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
    // Обновляем все данные
    await refetch() // Обновляем основной список организаций
    await refetchChildren() // Обновляем данные дочерних организаций
    await refetchPositions() // Обновляем данные должностей
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
    'EXECUTIVE': 'Исполнительная',
    'LEGISLATIVE': 'Законодательная',
    'JUDICIAL': 'Судебная',
    'ADMINISTRATIVE': 'Административная',
    'OPERATIONAL': 'Операционная'
  }
  return hierarchyMap[hierarchy] || hierarchy
}

const getHierarchyColor = (hierarchy: string): string => {
  const colorMap: Record<string, string> = {
    'EXECUTIVE': 'deep-purple',
    'LEGISLATIVE': 'blue',
    'JUDICIAL': 'red',
    'ADMINISTRATIVE': 'green',
    'OPERATIONAL': 'orange'
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



// Методы для работы с должностями
const openCreatePositionDialog = () => {
  editingPosition.value = null
  // Сбрасываем форму
  positionForm.title = ''
  positionForm.hierarchy = 'ADMINISTRATIVE'
  positionForm.responsibilities = ''
  positionForm.isActive = true
  showPositionDialog.value = true
}

const editPosition = (position: any) => {
  editingPosition.value = position
  // Заполняем форму данными из выбранной должности
  positionForm.title = position.title
  positionForm.hierarchy = position.hierarchy
  // Обрабатываем responsibilities - они могут быть JSON строками или обычными строками
  let responsibilities = ''
  if (Array.isArray(position.responsibilities)) {
    responsibilities = position.responsibilities.map((resp: string) => {
      // Если это JSON строка, извлекаем значение
      if (resp.startsWith('"') && resp.endsWith('"')) {
        try {
          return JSON.parse(resp)
        } catch {
          return resp
        }
      }
      return resp
    }).join(', ')
  } else if (position.responsibilities) {
    responsibilities = position.responsibilities
  }
  positionForm.responsibilities = responsibilities
  positionForm.isActive = position.isActive
  showPositionDialog.value = true
}

const deletePosition = async (position: any) => {
  console.log('=== НАЧАЛО deletePosition ===')
  console.log('Должность:', position.title, 'ID:', position.id)
  
  try {
    // Показываем диалог подтверждения с обработчиками
    const confirmed = await new Promise((resolve) => {
      $q.dialog({
        title: 'Подтверждение удаления',
        message: `Вы уверены, что хотите удалить должность "${position.title}"?`,
        ok: {
          label: 'Удалить',
          color: 'negative'
        },
        cancel: {
          label: 'Отмена',
          color: 'primary'
        },
        persistent: true
      }).onOk(() => {
        console.log('Пользователь нажал OK для должности')
        resolve(true)
      }).onCancel(() => {
        console.log('Пользователь нажал Отмена для должности')
        resolve(false)
      }).onDismiss(() => {
        console.log('Диалог должности закрыт')
        resolve(false)
      })
    })

    console.log('Результат диалога должности:', confirmed)
    
    if (confirmed) {
      console.log('Пользователь подтвердил удаление должности, выполняем удаление...')
      await deletePositionMutation({ id: position.id })
      console.log('Удаление должности выполнено успешно')
      
      // Обновляем все данные
      await refetch() // Обновляем основной список организаций
      await refetchChildren() // Обновляем данные дочерних организаций
      await refetchPositions() // Обновляем данные должностей
      
      $q.notify({
        type: 'positive',
        message: 'Должность успешно удалена'
      })
    } else {
      console.log('Пользователь отменил удаление должности')
      return
    }
  } catch (error) {
    console.error('Ошибка удаления должности:', error)
    
    // Проверяем тип ошибки
    let errorMessage = 'Ошибка при удалении должности'
    if (error.message?.includes('not found') || error.message?.includes('не найдена')) {
      errorMessage = 'Должность уже удалена или не найдена'
    } else if (error.message?.includes('permission') || error.message?.includes('доступ')) {
      errorMessage = 'Нет прав для удаления должности'
    }
    
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  }
  
  console.log('=== КОНЕЦ deletePosition ===')
}

// Методы для работы с дочерними организациями
const openCreateChildOrganizationDialog = () => {
  editingChildOrganization.value = null
  // Сбрасываем форму
  childOrganizationForm.name = ''
  childOrganizationForm.type = 'STATE'
  childOrganizationForm.foundedDate = new Date().toISOString().split('T')[0]
  childOrganizationForm.dissolvedDate = ''
  childOrganizationForm.isFictional = false
  childOrganizationForm.status = 'active'
  showChildOrganizationDialog.value = true
}

const editChildOrganization = (organization: any) => {
  editingChildOrganization.value = organization
  // Заполняем форму данными из выбранной организации
  childOrganizationForm.name = organization.name
  childOrganizationForm.type = organization.type
  childOrganizationForm.foundedDate = organization.foundedDate || new Date().toISOString().split('T')[0]
  childOrganizationForm.dissolvedDate = organization.dissolvedDate || ''
  childOrganizationForm.isFictional = organization.isFictional || false
  childOrganizationForm.status = organization.status || 'active'
  showChildOrganizationDialog.value = true
}

const deleteChildOrganization = async (organization: any) => {
  console.log('=== НАЧАЛО deleteChildOrganization ===')
  console.log('Дочерняя организация:', organization.name, 'ID:', organization.id)
  
  try {
    // Показываем диалог подтверждения с обработчиками
    const confirmed = await new Promise((resolve) => {
      $q.dialog({
        title: 'Подтверждение удаления',
        message: `Вы уверены, что хотите удалить дочернюю организацию "${organization.name}"?`,
        ok: {
          label: 'Удалить',
          color: 'negative'
        },
        cancel: {
          label: 'Отмена',
          color: 'primary'
        },
        persistent: true
      }).onOk(() => {
        console.log('Пользователь нажал OK для дочерней организации')
        resolve(true)
      }).onCancel(() => {
        console.log('Пользователь нажал Отмена для дочерней организации')
        resolve(false)
      }).onDismiss(() => {
        console.log('Диалог дочерней организации закрыт')
        resolve(false)
      })
    })

    console.log('Результат диалога дочерней организации:', confirmed)
    
    if (confirmed) {
      console.log('Пользователь подтвердил удаление дочерней организации, выполняем удаление...')
      await deleteOrganization({ id: organization.id })
      console.log('Удаление дочерней организации выполнено успешно')
      
      $q.notify({
        type: 'positive',
        message: 'Дочерняя организация успешно удалена'
      })
      
      // Обновляем все данные
      await refetch() // Обновляем основной список организаций
      await refetchChildren() // Обновляем данные дочерних организаций
      await refetchPositions() // Обновляем данные должностей
    } else {
      console.log('Пользователь отменил удаление дочерней организации')
      return
    }
  } catch (error) {
    console.error('Ошибка удаления дочерней организации:', error)
    
    // Проверяем тип ошибки
    let errorMessage = 'Ошибка при удалении дочерней организации'
    if (error.message?.includes('not found') || error.message?.includes('не найдена')) {
      errorMessage = 'Организация уже удалена или не найдена'
    } else if (error.message?.includes('permission') || error.message?.includes('доступ')) {
      errorMessage = 'Нет прав для удаления организации'
    }
    
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  }
  
  console.log('=== КОНЕЦ deleteChildOrganization ===')
}

// Методы сохранения
const savePosition = async () => {
  try {
    const input: PositionInput = {
      title: positionForm.title,
      hierarchy: positionForm.hierarchy,
      responsibilities: [positionForm.responsibilities], // Преобразуем в массив
      isActive: positionForm.isActive,
      organizationId: selectedOrganization.value?.id,
      createdDate: new Date().toISOString().split('T')[0] // Добавляем текущую дату
    }
    
    if (editingPosition.value) {
      // При обновлении используем существующую дату создания
      const updateInput = {
        ...input,
        createdDate: editingPosition.value.createdDate || new Date().toISOString().split('T')[0]
      }
      await updatePosition({ id: editingPosition.value.id, input: updateInput })
    } else {
      await createPosition({ input })
    }
    
    console.log('Сохранение должности:', positionForm)
    
    showPositionDialog.value = false
    
    // Обновляем все данные
    await refetch() // Обновляем основной список организаций
    await refetchChildren() // Обновляем данные дочерних организаций
    await refetchPositions() // Обновляем данные должностей
    
    $q.notify({
      type: 'positive',
      message: editingPosition.value ? 'Должность успешно обновлена' : 'Должность успешно создана'
    })
    
    // Сброс формы
    positionForm.title = ''
    positionForm.hierarchy = 'ADMINISTRATIVE'
    positionForm.responsibilities = ''
    positionForm.isActive = true
    editingPosition.value = null
  } catch (error) {
    console.error('Ошибка сохранения должности:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении должности'
    })
  }
}

const saveChildOrganization = async () => {
  try {
    // Извлекаем значение type, если это объект
    const typeValue = typeof childOrganizationForm.type === 'object' 
      ? childOrganizationForm.type.value 
      : childOrganizationForm.type

    // Извлекаем значение status, если это объект (для логики фронтенда)
    const statusValue = typeof childOrganizationForm.status === 'object' 
      ? childOrganizationForm.status.value 
      : childOrganizationForm.status

    console.log('=== СОЗДАНИЕ ДОЧЕРНЕЙ ОРГАНИЗАЦИИ ===')
    console.log('selectedOrganization.value:', selectedOrganization.value)
    console.log('selectedOrganization.value?.id:', selectedOrganization.value?.id)
    console.log('childOrganizationForm:', childOrganizationForm)

    const input = {
      name: childOrganizationForm.name,
      type: typeValue,
      foundedDate: childOrganizationForm.foundedDate,
      dissolvedDate: childOrganizationForm.dissolvedDate || null,
      parentUnitId: selectedOrganization.value?.id,
      isFictional: childOrganizationForm.isFictional,
      historicalPeriodId: '1' // По умолчанию раннее средневековье
    }
    
    console.log('GraphQL input:', input)
    
    if (editingChildOrganization.value) {
      await updateOrganization({ id: editingChildOrganization.value.id, input })
    } else {
      await createOrganization({ input })
    }
    
    console.log('Сохранение дочерней организации:', childOrganizationForm)
    
    showChildOrganizationDialog.value = false
    // Обновляем все данные
    await refetch() // Обновляем основной список организаций
    await refetchChildren() // Обновляем данные дочерних организаций
    await refetchPositions() // Обновляем данные должностей
    $q.notify({
      type: 'positive',
      message: editingChildOrganization.value ? 'Дочерняя организация успешно обновлена' : 'Дочерняя организация успешно создана'
    })
    
    // Сброс формы
    childOrganizationForm.name = ''
    childOrganizationForm.type = 'STATE'
    childOrganizationForm.foundedDate = new Date().toISOString().split('T')[0]
    childOrganizationForm.dissolvedDate = ''
    childOrganizationForm.isFictional = false
    childOrganizationForm.status = 'active'
    editingChildOrganization.value = null
  } catch (error) {
    console.error('Ошибка сохранения дочерней организации:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении дочерней организации'
    })
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

<style scoped>
.selected-row-highlight .q-tr.bg-blue-1 {
  background-color: #e3f2fd !important;
}

.selected-row-highlight .q-tr.bg-blue-1:hover {
  background-color: #bbdefb !important;
}

/* Стили для заголовков страницы */
.page-titles {
  margin-top: 5px !important;
  margin-bottom: 3px !important;
}

/* Унификация отступов между элементами страницы */
.organizations-page > * {
  margin-bottom: 3px !important;
}

.organizations-page > *:last-child {
  margin-bottom: 0 !important;
}

/* Адаптивные стили для кнопки добавления организации */
.add-organization-btn {
  min-width: auto !important;
  white-space: nowrap !important;
}

@media (max-width: 768px) {
  .add-organization-btn {
    min-width: 80px !important;
    font-size: 0.9rem !important;
  }
}

/* Унификация ширины всех карточек */
.filter-card,
.table-card,
.tabs-card {
  width: 100% !important;
  max-width: 2880px !important;
  margin: 0 auto !important;
  margin-bottom: 3px !important;
}

/* Убираем нижний отступ у последней карточки */
.tabs-card {
  margin-bottom: 0 !important;
}

/* Стили для вкладок (если открыты) */
.q-card .q-tabs {
  width: 100% !important;
  max-width: 2880px !important;
}

/* Дополнительные стили для q-page-container */
.q-page-container {
  width: 100% !important;
  max-width: 2880px !important;
  margin: 0 auto !important;
}



/* Адаптивные стили для мобильных устройств */
@media (max-width: 768px) {
  .organizations-page {
    padding: 2px !important;
  }
  
  .filter-card,
  .table-card {
    margin-left: 2px !important;
    margin-right: 2px !important;
  }
  
  .page-titles {
    margin-top: 3px !important;
    margin-bottom: 3px !important;
  }
  
  /* Уменьшение размера шрифта для мобильных */
  .page-titles h4 {
    font-size: 1.2rem !important;
  }
  
  .page-titles p {
    font-size: 0.9rem !important;
  }
}

/* Стили для очень маленьких экранов */
@media (max-width: 480px) {
  .organizations-page {
    padding: 1px !important;
  }
  
  .filter-card,
  .table-card {
    margin-left: 1px !important;
    margin-right: 1px !important;
  }
  
  .page-titles h4 {
    font-size: 1rem !important;
  }
  
  .page-titles p {
    font-size: 0.8rem !important;
  }
}

/* Стили для q-select фильтров - базовая видимость */
.filter-select :deep(.q-field__label) {
  color: #1976d2 !important;
  font-weight: 500 !important;
}

.filter-select :deep(.q-field__native) {
  color: #2c3e50 !important;
  font-weight: 500 !important;
}

.filter-select :deep(.q-field__control) {
  background-color: #ffffff !important;
  border: 1px solid #e0e0e0 !important;
}

.filter-select :deep(.q-field--focused .q-field__control) {
  border-color: #1976d2 !important;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2) !important;
}

.filter-select :deep(.q-field--outlined .q-field__control:before) {
  border-color: #e0e0e0 !important;
}

.filter-select :deep(.q-field--outlined .q-field__control:hover:before) {
  border-color: #1976d2 !important;
}

.filter-select :deep(.q-select__dropdown) {
  background-color: #ffffff !important;
  color: #2c3e50 !important;
}

.filter-select :deep(.q-item) {
  color: #2c3e50 !important;
  background-color: #ffffff !important;
}

.filter-select :deep(.q-item:hover) {
  background-color: #f5f5f5 !important;
}

.filter-select :deep(.q-item--active) {
  background-color: #e3f2fd !important;
  color: #1976d2 !important;
}

/* Стили для q-select в диалогах - улучшенная видимость полей */
.q-dialog .q-select :deep(.q-field__label) {
  color: #1976d2 !important;
  font-weight: 500 !important;
}

.q-dialog .q-select :deep(.q-field__native) {
  color: #2c3e50 !important;
  font-weight: 500 !important;
}

.q-dialog .q-select :deep(.q-field__control) {
  background-color: #ffffff !important;
  border: 1px solid #e0e0e0 !important;
}

.q-dialog .q-select :deep(.q-field--focused .q-field__control) {
  border-color: #1976d2 !important;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2) !important;
}

.q-dialog .q-select :deep(.q-field--outlined .q-field__control:before) {
  border-color: #e0e0e0 !important;
}

.q-dialog .q-select :deep(.q-field--outlined .q-field__control:hover:before) {
  border-color: #1976d2 !important;
}

.q-dialog .q-select :deep(.q-select__dropdown) {
  background-color: #ffffff !important;
  color: #2c3e50 !important;
}

.q-dialog .q-select :deep(.q-item) {
  color: #2c3e50 !important;
  background-color: #ffffff !important;
}

.q-dialog .q-select :deep(.q-item:hover) {
  background-color: #f5f5f5 !important;
}

.q-dialog .q-select :deep(.q-item--active) {
  background-color: #e3f2fd !important;
  color: #1976d2 !important;
}
</style>
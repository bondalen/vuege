<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Отчеты</h4>
        <p class="text-body1 text-grey-7">
          Генерация отчетов в различных форматах
        </p>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="row q-mb-md">
      <div class="col-12 col-md-4">
        <q-select
          v-model="selectedReportType"
          :options="reportTypes"
          label="Фильтр по типу"
          outlined
          dense
          clearable
        />
      </div>
      <div class="col-12 col-md-4">
        <q-select
          v-model="selectedFormat"
          :options="reportFormats"
          label="Фильтр по формату"
          outlined
          dense
          clearable
        />
      </div>
      <div class="col-12 col-md-4">
        <q-btn
          color="primary"
          label="Создать пользовательский отчет"
          icon="add"
          @click="showCustomReportDialog = true"
        />
      </div>
    </div>

    <!-- Типы отчетов -->
    <div class="row q-gutter-md">
      <q-card 
        v-for="reportType in reportTypes.filter(t => t.value !== 'custom')" 
        :key="reportType.value"
        class="col-12 col-sm-6 col-md-4"
      >
        <q-card-section>
          <div class="text-h6">
            <q-icon :name="reportType.icon" class="q-mr-sm" />
            {{ reportType.label }}
          </div>
          <div class="text-subtitle2">Список всех {{ reportType.label.toLowerCase() }}</div>
        </q-card-section>
        <q-card-actions>
          <q-btn 
            v-for="format in reportFormats" 
            :key="format.value"
            flat 
            color="primary" 
            :label="format.label"
            :icon="format.icon"
            @click="generateReport(reportType.value, format.value)" 
          />
        </q-card-actions>
      </q-card>
      
      <q-card class="col-12 col-sm-6 col-md-4">
        <q-card-section>
          <div class="text-h6">Государства</div>
          <div class="text-subtitle2">История государств</div>
        </q-card-section>
        <q-card-actions>
          <q-btn flat color="primary" label="PDF" @click="generateReport('states', 'pdf')" />
          <q-btn flat color="primary" label="Excel" @click="generateReport('states', 'excel')" />
          <q-btn flat color="primary" label="JSON" @click="generateReport('states', 'json')" />
        </q-card-actions>
      </q-card>
      
      <q-card class="col-12 col-sm-6 col-md-4">
        <q-card-section>
          <div class="text-h6">Люди</div>
          <div class="text-subtitle2">Биографии и должности</div>
        </q-card-section>
        <q-card-actions>
          <q-btn flat color="primary" label="PDF" @click="generateReport('people', 'pdf')" />
          <q-btn flat color="primary" label="Excel" @click="generateReport('people', 'excel')" />
          <q-btn flat color="primary" label="JSON" @click="generateReport('people', 'json')" />
        </q-card-actions>
      </q-card>
      
      <q-card class="col-12 col-sm-6 col-md-4">
        <q-card-section>
          <div class="text-h6">Места</div>
          <div class="text-subtitle2">Географические данные</div>
        </q-card-section>
        <q-card-actions>
          <q-btn flat color="primary" label="PDF" @click="generateReport('locations', 'pdf')" />
          <q-btn flat color="primary" label="Excel" @click="generateReport('locations', 'excel')" />
          <q-btn flat color="primary" label="JSON" @click="generateReport('locations', 'json')" />
        </q-card-actions>
      </q-card>
      
      <q-card class="col-12 col-sm-6 col-md-4">
        <q-card-section>
          <div class="text-h6">Статистика</div>
          <div class="text-subtitle2">Общая статистика системы</div>
        </q-card-section>
        <q-card-actions>
          <q-btn flat color="primary" label="PDF" @click="generateReport('statistics', 'pdf')" />
          <q-btn flat color="primary" label="Excel" @click="generateReport('statistics', 'excel')" />
          <q-btn flat color="primary" label="JSON" @click="generateReport('statistics', 'json')" />
        </q-card-actions>
      </q-card>
      
      <q-card class="col-12 col-sm-6 col-md-4">
        <q-card-section>
          <div class="text-h6">Пользовательский</div>
          <div class="text-subtitle2">Настраиваемый отчет</div>
        </q-card-section>
        <q-card-actions>
          <q-btn flat color="primary" label="Настроить" @click="showCustomReportDialog = true" />
        </q-card-actions>
      </q-card>
    </div>

    <!-- История отчетов -->
    <q-card class="q-mt-lg">
      <q-card-section>
        <div class="text-h6">История отчетов</div>
      </q-card-section>
      
      <q-table
        :rows="filteredHistory"
        :columns="historyColumns"
        :loading="loading"
        row-key="id"
        :pagination="{ rowsPerPage: 10 }"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-chip
              :color="getStatusColor(props.value)"
              :icon="getStatusIcon(props.value)"
              :label="props.value"
              size="sm"
            />
          </q-td>
        </template>
        
        <template v-slot:body-cell-createdAt="props">
          <q-td :props="props">
            {{ formatDate(props.value, 'DD.MM.YYYY HH:mm') }}
          </q-td>
        </template>
        
        <template v-slot:body-cell-size="props">
          <q-td :props="props">
            {{ props.value || '-' }}
          </q-td>
        </template>
        
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              color="primary"
              icon="download"
              size="sm"
              :disable="!props.row.downloadUrl"
              @click="downloadReport(props.row)"
            />
            <q-btn
              flat
              round
              color="negative"
              icon="delete"
              size="sm"
              @click="deleteReport(props.row)"
            />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Диалог пользовательского отчета -->
    <q-dialog v-model="showCustomReportDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">Настройка пользовательского отчета</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="customReport.name"
            label="Название отчета *"
            outlined
            dense
            class="q-mb-md"
            :rules="[val => !!val || 'Название обязательно']"
          />
          
          <q-select
            v-model="customReport.type"
            :options="reportTypes.filter(t => t.value !== 'custom')"
            label="Тип данных *"
            outlined
            dense
            class="q-mb-md"
            :rules="[val => !!val || 'Тип данных обязателен']"
          />
          
          <q-select
            v-model="customReport.format"
            :options="reportFormats"
            label="Формат"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-input
            v-model.number="customReport.limit"
            label="Лимит записей"
            type="number"
            outlined
            dense
            class="q-mb-md"
            min="1"
            max="10000"
          />
          
          <q-select
            v-model="customReport.sortBy"
            :options="columnOptions"
            label="Сортировка по"
            outlined
            dense
            class="q-mb-md"
            clearable
          />
          
          <q-input
            v-model="customReport.filters"
            label="Фильтры (JSON)"
            type="textarea"
            outlined
            dense
            class="q-mb-md"
            placeholder='{"type": "GOVERNMENT", "active": true}'
            rows="3"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn
            label="Создать отчет"
            color="primary"
            :loading="loading"
            @click="generateCustomReport"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { 
  useNotificationManager, 
  useLoadingManager, 
  useTableManager,
  useFormManager,
  useModalManager,
  useApiClient,
  formatDate,
  formatYear,
  formatFileSize
} from '@/utils'
import { GET_ORGANIZATIONS, GET_STATES, GET_PEOPLE, GET_LOCATIONS } from '@/graphql/queries'

// Quasar
const $q = useQuasar()

// Менеджеры
const { 
  success: showSuccess, 
  error: showError, 
  warning: showWarning,
  info: showInfo
} = useNotificationManager()

const { show: showLoading, hide: hideLoading } = useLoadingManager()

const { query } = useApiClient()

const { show: showModal, confirm: showConfirm } = useModalManager()

// Состояние
const loading = ref(false)
const showCustomReportDialog = ref(false)
const selectedReportType = ref('')
const selectedFormat = ref('pdf')
const reportProgress = ref(0)

// Пользовательский отчет
const customReport = reactive({
  name: '',
  type: '',
  format: 'pdf',
  filters: {},
  columns: [],
  dateRange: {
    from: null,
    to: null
  },
  groupBy: '',
  sortBy: '',
  limit: 1000
})

// История отчетов
const reportHistory = ref([
  {
    id: 1,
    name: 'Отчет по организациям',
    type: 'organizations',
    format: 'pdf',
    createdAt: new Date('2024-01-15'),
    status: 'completed',
    size: '2.5 MB',
    downloadUrl: '/reports/1.pdf'
  },
  {
    id: 2,
    name: 'Статистика государств',
    type: 'states',
    format: 'excel',
    createdAt: new Date('2024-01-14'),
    status: 'completed',
    size: '1.8 MB',
    downloadUrl: '/reports/2.xlsx'
  },
  {
    id: 3,
    name: 'Список людей',
    type: 'people',
    format: 'csv',
    createdAt: new Date('2024-01-13'),
    status: 'processing',
    size: null,
    downloadUrl: null
  }
])

// Опции
const reportTypes = [
  { label: 'Организации', value: 'organizations', icon: 'business' },
  { label: 'Государства', value: 'states', icon: 'flag' },
  { label: 'Люди', value: 'people', icon: 'people' },
  { label: 'Местоположения', value: 'locations', icon: 'location_on' },
  { label: 'Статистика', value: 'statistics', icon: 'analytics' },
  { label: 'Пользовательский', value: 'custom', icon: 'edit' }
]

const reportFormats = [
  { label: 'PDF', value: 'pdf', icon: 'picture_as_pdf' },
  { label: 'Excel', value: 'excel', icon: 'table_chart' },
  { label: 'JSON', value: 'json', icon: 'code' },
  { label: 'CSV', value: 'csv', icon: 'table_view' },
  { label: 'XML', value: 'xml', icon: 'data_object' }
]

const columnOptions = [
  { label: 'ID', value: 'id' },
  { label: 'Название', value: 'name' },
  { label: 'Описание', value: 'description' },
  { label: 'Тип', value: 'type' },
  { label: 'Дата создания', value: 'createdAt' },
  { label: 'Дата обновления', value: 'updatedAt' }
]

// Колонки истории
const historyColumns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true },
  { name: 'type', label: 'Тип', field: 'type', sortable: true },
  { name: 'format', label: 'Формат', field: 'format', sortable: true },
  { name: 'createdAt', label: 'Создан', field: 'createdAt', sortable: true },
  { name: 'status', label: 'Статус', field: 'status', sortable: true },
  { name: 'size', label: 'Размер', field: 'size', sortable: true },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false }
]

// Вычисляемые свойства
const filteredHistory = computed(() => {
  return reportHistory.value.filter(report => {
    if (selectedReportType.value && report.type !== selectedReportType.value) {
      return false
    }
    if (selectedFormat.value && report.format !== selectedFormat.value) {
      return false
    }
    return true
  })
})

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'positive'
    case 'processing': return 'warning'
    case 'failed': return 'negative'
    default: return 'grey'
  }
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'completed': return 'check_circle'
    case 'processing': return 'hourglass_empty'
    case 'failed': return 'error'
    default: return 'help'
  }
}

// Методы
const loadReportHistory = async () => {
  loading.value = true
  showLoading({ message: 'Загрузка истории отчетов...' })
  
  try {
    // TODO: Загрузка истории отчетов через GraphQL
    // const { data } = await query(GET_REPORT_HISTORY)
    // reportHistory.value = data.reportHistory
    
    // Пока используем моковые данные
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showSuccess('История отчетов загружена')
  } catch (error) {
    console.error('Ошибка загрузки истории отчетов:', error)
    showError('Ошибка загрузки истории отчетов')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const generateReport = async (type: string, format: string) => {
  if (type === 'custom') {
    showCustomReportDialog.value = true
    return
  }

  loading.value = true
  showLoading({ message: 'Генерация отчета...' })
  
  try {
    // Получаем данные в зависимости от типа отчета
    let data = []
    
    switch (type) {
      case 'organizations':
        const { data: orgData } = await query(GET_ORGANIZATIONS, { limit: 1000 })
        data = orgData.organizations
        break
      case 'states':
        const { data: statesData } = await query(GET_STATES, { limit: 1000 })
        data = statesData.states
        break
      case 'people':
        const { data: peopleData } = await query(GET_PEOPLE, { limit: 1000 })
        data = peopleData.people
        break
      case 'locations':
        const { data: locationsData } = await query(GET_LOCATIONS, { limit: 1000 })
        data = locationsData.locations
        break
      case 'statistics':
        data = await generateStatistics()
        break
    }

    // Генерируем отчет
    const report = await generateReportFile(data, type, format)
    
    // Добавляем в историю
    reportHistory.value.unshift({
      id: Date.now(),
      name: `Отчет: ${type}`,
      type,
      format,
      createdAt: new Date(),
      status: 'completed',
      size: formatFileSize(report.size),
      downloadUrl: report.url
    })
    
    showSuccess(`Отчет "${type}" успешно сгенерирован`)
  } catch (error) {
    console.error('Ошибка генерации отчета:', error)
    showError('Ошибка генерации отчета')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const generateCustomReport = async () => {
  if (!customReport.name || !customReport.type) {
    showError('Заполните обязательные поля')
    return
  }

  loading.value = true
  showLoading({ message: 'Создание пользовательского отчета...' })
  
  try {
    // Получаем данные
    let data = []
    
    switch (customReport.type) {
      case 'organizations':
        const { data: orgData } = await query(GET_ORGANIZATIONS, { 
          limit: customReport.limit,
          filters: customReport.filters 
        })
        data = orgData.organizations
        break
      // Добавить другие типы...
    }

    // Применяем фильтры и сортировку
    data = applyFilters(data, customReport.filters)
    if (customReport.sortBy) {
      data = sortData(data, customReport.sortBy)
    }

    // Генерируем отчет
    const report = await generateReportFile(data, customReport.type, customReport.format)
    
    // Добавляем в историю
    reportHistory.value.unshift({
      id: Date.now(),
      name: customReport.name,
      type: customReport.type,
      format: customReport.format,
      createdAt: new Date(),
      status: 'completed',
      size: formatFileSize(report.size),
      downloadUrl: report.url
    })
    
    showCustomReportDialog.value = false
    showSuccess('Пользовательский отчет создан')
  } catch (error) {
    console.error('Ошибка создания отчета:', error)
    showError('Ошибка создания отчета')
  } finally {
    loading.value = false
    hideLoading()
  }
}

const downloadReport = async (report: any) => {
  if (!report.downloadUrl) {
    showWarning('Отчет еще не готов')
    return
  }

  try {
    showLoading({ message: 'Подготовка к скачиванию...' })
    
    // Создаем ссылку для скачивания
    const link = document.createElement('a')
    link.href = report.downloadUrl
    link.download = `${report.name}.${report.format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    showSuccess('Отчет скачан')
  } catch (error) {
    console.error('Ошибка скачивания отчета:', error)
    showError('Ошибка скачивания отчета')
  } finally {
    hideLoading()
  }
}

const deleteReport = async (report: any) => {
  try {
    const confirmed = await showConfirm({
      title: 'Подтверждение',
      message: `Удалить отчет "${report.name}"?`,
      okLabel: 'Удалить',
      cancelLabel: 'Отмена'
    })
    
    if (confirmed) {
      // TODO: Удаление отчета через GraphQL
      const index = reportHistory.value.findIndex(r => r.id === report.id)
      if (index !== -1) {
        reportHistory.value.splice(index, 1)
      }
      
      showSuccess('Отчет удален')
    }
  } catch (error) {
    console.error('Ошибка удаления отчета:', error)
    showError('Ошибка удаления отчета')
  }
}

// Вспомогательные методы
const generateStatistics = async () => {
  // Генерируем статистику
  const stats = {
    totalOrganizations: 0,
    totalStates: 0,
    totalPeople: 0,
    totalLocations: 0,
    activeOrganizations: 0,
    dissolvedOrganizations: 0
  }
  
  // Получаем данные для статистики
  const [orgData, statesData, peopleData, locationsData] = await Promise.all([
    query(GET_ORGANIZATIONS, { limit: 1 }),
    query(GET_STATES, { limit: 1 }),
    query(GET_PEOPLE, { limit: 1 }),
    query(GET_LOCATIONS, { limit: 1 })
  ])
  
  return stats
}

const generateReportFile = async (data: any[], type: string, format: string) => {
  // Имитация генерации файла
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  const size = Math.random() * 5000000 + 100000 // 100KB - 5MB
  const url = `/api/reports/${Date.now()}.${format}`
  
  return { size, url }
}

const applyFilters = (data: any[], filters: any) => {
  // Применяем фильтры к данным
  return data.filter(item => {
    // Логика фильтрации
    return true
  })
}

const sortData = (data: any[], sortBy: string) => {
  // Сортируем данные
  return data.sort((a, b) => {
    if (a[sortBy] < b[sortBy]) return -1
    if (a[sortBy] > b[sortBy]) return 1
    return 0
  })
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Инициализация
onMounted(() => {
  loadReportHistory()
})
</script>
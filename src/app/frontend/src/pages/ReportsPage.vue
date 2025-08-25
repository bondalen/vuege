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

    <!-- Типы отчетов -->
    <div class="row q-gutter-md">
      <q-card class="col-12 col-sm-6 col-md-4">
        <q-card-section>
          <div class="text-h6">Организации</div>
          <div class="text-subtitle2">Список всех организаций</div>
        </q-card-section>
        <q-card-actions>
          <q-btn flat color="primary" label="PDF" @click="generateReport('organizations', 'pdf')" />
          <q-btn flat color="primary" label="Excel" @click="generateReport('organizations', 'excel')" />
          <q-btn flat color="primary" label="JSON" @click="generateReport('organizations', 'json')" />
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
        :rows="reportHistory"
        :columns="historyColumns"
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
              icon="download"
              size="sm"
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
            label="Название отчета"
            outlined
            dense
            class="q-mb-md"
          />
          
          <q-select
            v-model="customReport.type"
            :options="reportTypes"
            label="Тип данных"
            outlined
            dense
            class="q-mb-md"
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
            v-model="customReport.filters"
            label="Фильтры (JSON)"
            type="textarea"
            outlined
            dense
            class="q-mb-md"
            placeholder='{"type": "GOVERNMENT", "active": true}'
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn
            label="Создать отчет"
            color="primary"
            @click="createCustomReport"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

// Состояние
const loading = ref(false)
const reportHistory = ref([])
const showCustomReportDialog = ref(false)

// Пользовательский отчет
const customReport = reactive({
  name: '',
  type: '',
  format: '',
  filters: ''
})

// Опции
const reportTypes = [
  { label: 'Организации', value: 'organizations' },
  { label: 'Государства', value: 'states' },
  { label: 'Люди', value: 'people' },
  { label: 'Места', value: 'locations' },
  { label: 'Статистика', value: 'statistics' }
]

const reportFormats = [
  { label: 'PDF', value: 'pdf' },
  { label: 'Excel', value: 'excel' },
  { label: 'JSON', value: 'json' },
  { label: 'CSV', value: 'csv' },
  { label: 'XML', value: 'xml' }
]

// Колонки истории
const historyColumns = [
  { name: 'name', label: 'Название', field: 'name', sortable: true },
  { name: 'type', label: 'Тип', field: 'type', sortable: true },
  { name: 'format', label: 'Формат', field: 'format', sortable: true },
  { name: 'createdAt', label: 'Создан', field: 'createdAt', sortable: true },
  { name: 'status', label: 'Статус', field: 'status', sortable: true },
  { name: 'actions', label: 'Действия', field: 'actions', sortable: false }
]

// Методы
const loadReportHistory = async () => {
  loading.value = true
  try {
    // TODO: Загрузка истории отчетов
    reportHistory.value = []
  } catch (error) {
    console.error('Ошибка загрузки истории отчетов:', error)
  } finally {
    loading.value = false
  }
}

const generateReport = async (type: string, format: string) => {
  try {
    // TODO: Генерация отчета через GraphQL
    console.log('Генерация отчета:', { type, format })
  } catch (error) {
    console.error('Ошибка генерации отчета:', error)
  }
}

const createCustomReport = async () => {
  try {
    // TODO: Создание пользовательского отчета
    console.log('Создание пользовательского отчета:', customReport)
    showCustomReportDialog.value = false
  } catch (error) {
    console.error('Ошибка создания отчета:', error)
  }
}

const downloadReport = (report: any) => {
  // TODO: Скачивание отчета
  console.log('Скачивание отчета:', report.id)
}

const deleteReport = (report: any) => {
  // TODO: Удаление отчета
  console.log('Удаление отчета:', report.id)
}

// Инициализация
onMounted(() => {
  loadReportHistory()
})
</script>
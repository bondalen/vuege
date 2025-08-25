<template>
  <div class="vuege-table">
    <!-- Заголовок таблицы -->
    <div v-if="title || $slots.header" class="table-header q-mb-md">
      <div class="row items-center justify-between">
        <div class="col">
          <h5 v-if="title" class="text-h5 q-mb-xs">{{ title }}</h5>
          <p v-if="subtitle" class="text-body2 text-grey-7">{{ subtitle }}</p>
          <slot name="header" />
        </div>
        <div class="col-auto">
          <slot name="actions" />
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div v-if="showFilters && $slots.filters" class="table-filters q-mb-md">
      <q-card flat bordered>
        <q-card-section>
          <slot name="filters" />
        </q-card-section>
      </q-card>
    </div>

    <!-- Поиск -->
    <div v-if="showSearch" class="table-search q-mb-md">
      <q-input
        v-model="searchQuery"
        :placeholder="searchPlaceholder"
        outlined
        dense
        clearable
        @update:model-value="onSearch"
      >
        <template v-slot:prepend>
          <q-icon name="search" />
        </template>
      </q-input>
    </div>

    <!-- Таблица -->
    <q-table
      :rows="processedData"
      :columns="columns"
      :loading="loading"
      :pagination="pagination"
      :row-key="rowKey"
      :selection="selection"
      :selected="selectedRows"
      @request="onRequest"
      @selection="onSelection"
    >
      <!-- Слоты для кастомных ячеек -->
      <template v-for="(_, name) in $slots" :key="name" v-slot:[name]="props">
        <slot :name="name" v-bind="props" />
      </template>
    </q-table>

    <!-- Пагинация -->
    <div v-if="showPagination" class="table-pagination q-mt-md">
      <div class="row items-center justify-between">
        <div class="col">
          <span class="text-caption">
            Показано {{ pagination.rowsPerPage * (pagination.page - 1) + 1 }} - 
            {{ Math.min(pagination.rowsPerPage * pagination.page, pagination.rowsNumber) }} 
            из {{ pagination.rowsNumber }} записей
          </span>
        </div>
        <div class="col-auto">
          <q-pagination
            v-model="pagination.page"
            :max="Math.ceil(pagination.rowsNumber / pagination.rowsPerPage)"
            :max-pages="6"
            boundary-numbers
            @update:model-value="onPageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useTableManager } from '@/utils'

// Пропсы
interface Props {
  data: any[]
  columns: any[]
  title?: string
  subtitle?: string
  loading?: boolean
  rowKey?: string
  selection?: 'single' | 'multiple' | false
  showFilters?: boolean
  showSearch?: boolean
  showPagination?: boolean
  searchPlaceholder?: string
  pageSize?: number
  sortable?: boolean
  filterable?: boolean
  selectable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  rowKey: 'id',
  selection: false,
  showFilters: true,
  showSearch: true,
  showPagination: true,
  searchPlaceholder: 'Поиск...',
  pageSize: 10,
  sortable: true,
  filterable: true,
  selectable: true
})

// Эмиты
const emit = defineEmits<{
  selection: [rows: any[]]
  search: [query: string]
  sort: [sort: any]
  filter: [filters: any]
  pageChange: [page: number]
  rowClick: [row: any]
}>()

// Состояние
const searchQuery = ref('')
const selectedRows = ref<any[]>([])

// Пагинация
const pagination = ref({
  page: 1,
  rowsPerPage: props.pageSize,
  rowsNumber: props.data.length,
  sortBy: null as string | null,
  descending: false
})

// Менеджер таблицы
const {
  processedData,
  setSearch,
  setPage,
  setPageSize,
  setSort,
  addFilter,
  clearFilters,
  getSelectedRows,
  selectAll,
  deselectAll
} = useTableManager(props.data, props.columns, props.rowKey)

// Вычисляемые свойства
const columns = computed(() => {
  return props.columns.map(col => ({
    ...col,
    sortable: props.sortable && col.sortable !== false,
    filterable: props.filterable && col.filterable !== false
  }))
})

// Методы
const onSearch = (query: string) => {
  setSearch(query)
  emit('search', query)
}

const onRequest = (request: any) => {
  if (request.pagination) {
    pagination.value = request.pagination
    setPage(request.pagination.page)
    setPageSize(request.pagination.rowsPerPage)
  }
  
  if (request.sortBy) {
    setSort(request.sortBy, request.descending ? 'desc' : 'asc')
    emit('sort', { key: request.sortBy, direction: request.descending ? 'desc' : 'asc' })
  }
}

const onSelection = (selection: any) => {
  selectedRows.value = selection.selected
  emit('selection', selection.selected)
}

const onPageChange = (page: number) => {
  setPage(page)
  emit('pageChange', page)
}

// Наблюдатели
watch(() => props.data, (newData) => {
  pagination.value.rowsNumber = newData.length
}, { deep: true })

// Инициализация
onMounted(() => {
  // Инициализация менеджера таблицы
})
</script>

<style scoped>
.vuege-table {
  width: 100%;
}

.table-header {
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.table-filters {
  background-color: #f5f5f5;
  border-radius: 8px;
}

.table-search {
  max-width: 400px;
}

.table-pagination {
  border-top: 1px solid #e0e0e0;
  padding-top: 1rem;
}
</style>
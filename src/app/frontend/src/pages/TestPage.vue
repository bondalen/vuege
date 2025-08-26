<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <h4 class="text-h4 q-mb-sm">Тест интеграции GraphQL</h4>
        <p class="text-body1 text-grey-7">
          Проверка работы GraphQL API и Frontend
        </p>
      </div>
    </div>

    <!-- Статус подключения -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">Статус подключения</div>
        <div class="row q-gutter-md">
          <q-chip :color="backendStatus ? 'positive' : 'negative'" text-color="white">
            Backend: {{ backendStatus ? 'Подключен' : 'Не подключен' }}
          </q-chip>
          <q-chip :color="graphqlStatus ? 'positive' : 'negative'" text-color="white">
            GraphQL: {{ graphqlStatus ? 'Работает' : 'Ошибка' }}
          </q-chip>
        </div>
      </q-card-section>
    </q-card>

    <!-- Тест GraphQL -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">Тест GraphQL запросов</div>
        <q-btn color="primary" label="Загрузить людей" @click="loadPeople" :loading="loading" />
        <q-btn color="secondary" label="Загрузить организации" @click="loadOrganizations" :loading="loading" class="q-ml-md" />
      </q-card-section>
    </q-card>

    <!-- Результаты -->
    <q-card v-if="people.length > 0">
      <q-card-section>
        <div class="text-h6 q-mb-md">Люди ({{ people.length }})</div>
        <div class="row q-gutter-md">
          <q-card v-for="person in people" :key="person.id" class="col-12 col-sm-6 col-md-4">
            <q-card-section>
              <div class="text-h6">{{ person.name }}</div>
              <div class="text-subtitle2" v-if="person.nationality">
                {{ person.nationality }}
              </div>
              <div class="text-caption" v-if="person.birthDate">
                {{ formatDate(person.birthDate) }}
              </div>
            </q-card-section>
          </q-card>
        </div>
      </q-card-section>
    </q-card>

    <q-card v-if="organizations.length > 0">
      <q-card-section>
        <div class="text-h6 q-mb-md">Организации ({{ organizations.length }})</div>
        <div class="row q-gutter-md">
          <q-card v-for="org in organizations" :key="org.id" class="col-12 col-sm-6 col-md-4">
            <q-card-section>
              <div class="text-h6">{{ org.name }}</div>
              <div class="text-subtitle2">{{ org.type }}</div>
              <div class="text-caption" v-if="org.foundedDate">
                Основана: {{ formatDate(org.foundedDate) }}
              </div>
            </q-card-section>
          </q-card>
        </div>
      </q-card-section>
    </q-card>

    <!-- Ошибки -->
    <q-card v-if="error" class="q-mt-md">
      <q-card-section>
        <div class="text-h6 text-negative q-mb-md">Ошибка</div>
        <pre class="text-caption">{{ error }}</pre>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { useQuasar } from 'quasar'
import { GET_PEOPLE, GET_ORGANIZATIONS } from '../graphql/queries'
import type { Person, Organization } from '../types/graphql'

const $q = useQuasar()

// Состояние
const loading = ref(false)
const error = ref('')
const backendStatus = ref(false)
const graphqlStatus = ref(false)
const people = ref<Person[]>([])
const organizations = ref<Organization[]>([])

// GraphQL запросы
const { result: peopleResult, loading: peopleLoading, error: peopleError } = useQuery(
  GET_PEOPLE,
  { search: { query: '', pagination: { page: 1, size: 10 } } },
  { fetchPolicy: 'cache-and-network' }
)

const { result: organizationsResult, loading: orgsLoading, error: orgsError } = useQuery(
  GET_ORGANIZATIONS,
  { search: { query: '', pagination: { page: 1, size: 10 } } },
  { fetchPolicy: 'cache-and-network' }
)

// Методы
const checkBackendStatus = async () => {
  try {
    const response = await fetch('/api/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: '{ __schema { types { name } } }' })
    })
    backendStatus.value = response.ok
    graphqlStatus.value = response.ok
  } catch (err) {
    backendStatus.value = false
    graphqlStatus.value = false
    error.value = `Ошибка подключения к Backend: ${err}`
  }
}

const loadPeople = async () => {
  try {
    loading.value = true
    error.value = ''
    
    if (peopleResult.value?.people) {
      people.value = peopleResult.value.people
      $q.notify({
        type: 'positive',
        message: `Загружено ${people.value.length} человек`
      })
    }
  } catch (err) {
    error.value = `Ошибка загрузки людей: ${err}`
    $q.notify({
      type: 'negative',
      message: 'Ошибка при загрузке людей'
    })
  } finally {
    loading.value = false
  }
}

const loadOrganizations = async () => {
  try {
    loading.value = true
    error.value = ''
    
    if (organizationsResult.value?.organizations) {
      organizations.value = organizationsResult.value.organizations
      $q.notify({
        type: 'positive',
        message: `Загружено ${organizations.value.length} организаций`
      })
    }
  } catch (err) {
    error.value = `Ошибка загрузки организаций: ${err}`
    $q.notify({
      type: 'negative',
      message: 'Ошибка при загрузке организаций'
    })
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('ru-RU')
}

// Инициализация
onMounted(() => {
  checkBackendStatus()
})
</script>
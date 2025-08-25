import { createApp } from 'vue'
import { Quasar, Notify, Dialog, Loading } from 'quasar'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './router/routes'
import { createApolloClient } from './utils/apollo'
import { DefaultApolloClient } from '@vue/apollo-composable'

// Import Quasar css
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/dist/quasar.css'

// Import app css
import './style.css'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create Apollo client
const apolloClient = createApolloClient()

// Create app
const app = createApp({
  name: 'VuegeApp'
})

// Use plugins
app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Loading
  },
  config: {
    brand: {
      primary: '#1976D2',
      secondary: '#26A69A',
      accent: '#9C27B0',
      dark: '#1D1D1D',
      darkPage: '#121212',
      positive: '#21BA45',
      negative: '#C10015',
      info: '#31CCEC',
      warning: '#F2C037'
    }
  }
})

// Use router
app.use(router)

// Provide Apollo client
app.provide(DefaultApolloClient, apolloClient)

// Mount app
app.mount('#app')
import { RouteRecordRaw } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import OrganizationsPage from '../pages/OrganizationsPage.vue'
import StatesPage from '../pages/StatesPage.vue'
import PeoplePage from '../pages/PeoplePage.vue'
import LocationsPage from '../pages/LocationsPage.vue'
import ReportsPage from '../pages/ReportsPage.vue'
import SettingsPage from '../pages/SettingsPage.vue'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/organizations',
    name: 'organizations',
    component: OrganizationsPage
  },
  {
    path: '/states',
    name: 'states',
    component: StatesPage
  },
  {
    path: '/people',
    name: 'people',
    component: PeoplePage
  },
  {
    path: '/locations',
    name: 'locations',
    component: LocationsPage
  },
  {
    path: '/reports',
    name: 'reports',
    component: ReportsPage
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsPage
  }
]
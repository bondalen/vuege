import { RouteRecordRaw } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import OrganizationsPage from '../pages/OrganizationsPage.vue'
import StatesPage from '../pages/StatesPage.vue'
import PeoplePage from '../pages/PeoplePage.vue'
import LocationsPage from '../pages/LocationsPage.vue'
import ReportsPage from '../pages/ReportsPage.vue'
import SettingsPage from '../pages/SettingsPage.vue'
import TestPage from '../pages/TestPage.vue'
import TestSelectPage from '../pages/TestSelectPage.vue'
import SimpleTestPage from '../pages/SimpleTestPage.vue'
import QSelectTestPage from '../pages/QSelectTestPage.vue'
import StringTestPage from '../pages/StringTestPage.vue'
import MinimalTestPage from '../pages/MinimalTestPage.vue'
import CssTestPage from '../pages/CssTestPage.vue'
import ForceRenderTestPage from '../pages/ForceRenderTestPage.vue'
import VirtualScrollTestPage from '../pages/VirtualScrollTestPage.vue'

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
  },
  {
    path: '/test',
    name: 'test',
    component: TestPage
  },
  {
    path: '/test-select',
    name: 'test-select',
    component: TestSelectPage
  },
  {
    path: '/simple-test',
    name: 'simple-test',
    component: SimpleTestPage
  },
  {
    path: '/qselect-test',
    name: 'qselect-test',
    component: QSelectTestPage
  },
  {
    path: '/string-test',
    name: 'string-test',
    component: StringTestPage
  },
  {
    path: '/minimal-test',
    name: 'minimal-test',
    component: MinimalTestPage
  },
  {
    path: '/css-test',
    name: 'css-test',
    component: CssTestPage
  },
  {
    path: '/force-render-test',
    name: 'force-render-test',
    component: ForceRenderTestPage
  },
  {
    path: '/virtual-scroll-test',
    name: 'virtual-scroll-test',
    component: VirtualScrollTestPage
  }
]
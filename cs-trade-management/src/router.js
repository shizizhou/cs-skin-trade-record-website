import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/login.vue'
import Register from './components/register.vue'
import Index from './components/index.vue'
import addTrade from './components/addTrade.vue'
import profit from './components/profit.vue'
import loss from './components/loss.vue'
import Search from './components/search.vue'
import importCSV from './components/importCSV.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/', component: Index },
  { path: '/add_trade', component: addTrade },
  { path: '/profit', component: profit },
  { path: '/loss', component: loss },
  { path: '/search', component: Search },
  { path: '/import_csv', component: importCSV }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
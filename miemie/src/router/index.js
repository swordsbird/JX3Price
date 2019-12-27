import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'text',
    component: () => import('../components/TextView.vue')
  },
  {
    path: '/text',
    name: 'text',
    component: () => import('../components/TextView.vue')
  },
  {
    path: '/customize',
    name: 'customize',
    component: () => import('../components/CustomizeView.vue')
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('../components/HistoryView.vue')
  },
  {
    path: '/analysis',
    name: 'analysis',
    component: () => import('../components/AnalysisView.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../components/SettingView.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  routes
})

export default router

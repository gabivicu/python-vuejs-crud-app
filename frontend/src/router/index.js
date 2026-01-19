import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../pages/Landing.vue'
import Home from '../pages/Home.vue'
import About from '../pages/About.vue'
import Settings from '../pages/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Landing,
  },
  {
    path: '/app',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

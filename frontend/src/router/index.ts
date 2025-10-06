import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/clientes',
    name: 'Clientes',
    component: () => import('../views/Clientes.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/agenda',
    name: 'Agenda',
    component: () => import('../views/Agenda.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/funcionarios',
    name: 'Funcionarios',
    component: () => import('../views/Funcionarios.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/procedimentos',
    name: 'Procedimentos',
    component: () => import('../views/Procedimentos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/pagamentos',
    name: 'Pagamentos',
    component: () => import('../views/Pagamentos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mensagens',
    name: 'Mensagens',
    component: () => import('../views/Mensagens.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Garantir que o token seja inicializado
  authStore.initializeAuth()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
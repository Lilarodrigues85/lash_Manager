import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref('')
  const user = ref(null)
  
  // Inicializar token imediatamente
  if (typeof window !== 'undefined') {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      token.value = savedToken
    }
  }

  // Inicializar token do localStorage
  const initializeAuth = () => {
    const savedToken = localStorage.getItem('token')
    console.log('Inicializando auth, token do localStorage:', savedToken)
    if (savedToken) {
      token.value = savedToken
      console.log('Token carregado:', !!token.value)
    }
  }

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username: string, password: string) => {
    const log = (msg: string) => {
      console.log(msg)
      const logs = JSON.parse(localStorage.getItem('debug_logs') || '[]')
      logs.push(`${new Date().toISOString()}: ${msg}`)
      localStorage.setItem('debug_logs', JSON.stringify(logs.slice(-20)))
    }
    
    try {
      log('Fazendo requisição de login...')
      const response = await api.post('/auth/login', { username, password })
      log(`Resposta recebida: status ${response.status}`)
      log(`Dados: ${JSON.stringify(response.data)}`)
      
      if (response.data && response.data.access_token) {
        token.value = response.data.access_token
        user.value = response.data.usuario
        localStorage.setItem('token', token.value)
        log(`Token salvo: ${token.value.substring(0, 20)}...`)
        log(`isAuthenticated: ${!!token.value}`)
        return true
      } else {
        log('ERRO: Token não encontrado na resposta')
        return false
      }
    } catch (error: any) {
      log(`ERRO no login: ${error.message}`)
      log(`Status do erro: ${error.response?.status}`)
      return false
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  const getCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  // Inicializar ao criar a store
  initializeAuth()

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    getCurrentUser,
    initializeAuth
  }
})
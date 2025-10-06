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
    try {
      console.log('Fazendo requisição de login...')
      const response = await api.post('/auth/login', { username, password })
      console.log('Resposta completa:', response)
      console.log('Dados da resposta:', response.data)
      
      if (response.data && response.data.access_token) {
        token.value = response.data.access_token
        user.value = response.data.usuario
        localStorage.setItem('token', token.value)
        console.log('Token definido na store:', token.value)
        console.log('Token salvo no localStorage:', localStorage.getItem('token'))
        console.log('isAuthenticated após login:', !!token.value)
        return true
      } else {
        console.error('Token não encontrado na resposta')
        return false
      }
    } catch (error) {
      console.error('Erro completo no login:', error)
      console.error('Resposta do erro:', error.response?.data)
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
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { username, password })
      token.value = response.data.access_token
      user.value = response.data.usuario
      localStorage.setItem('token', token.value)
      return true
    } catch (error) {
      console.error('Erro no login:', error)
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

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    getCurrentUser
  }
})
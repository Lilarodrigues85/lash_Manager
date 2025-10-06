import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  console.log('Interceptor - Token encontrado:', !!token)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('Header Authorization adicionado')
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Remover interceptor que limpa token automaticamente
    return Promise.reject(error)
  }
)

export default api
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  console.log('🔍 INTERCEPTOR REQUEST:')
  console.log('  URL:', config.url)
  console.log('  Token existe?', !!token)
  console.log('  Token (primeiros 50):', token?.substring(0, 50))
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('  ✅ Header Authorization definido')
  } else {
    console.log('  ❌ SEM TOKEN!')
  }
  
  console.log('  Headers:', config.headers)
  return config
}, (error) => {
  console.error('❌ ERRO NO INTERCEPTOR REQUEST:', error)
  return Promise.reject(error)
})

api.interceptors.response.use(
  (response) => {
    console.log('✅ RESPONSE:', response.config.url, response.status)
    return response
  },
  (error) => {
    console.log('❌ RESPONSE ERROR:')
    console.log('  URL:', error.config?.url)
    console.log('  Status:', error.response?.status)
    console.log('  Data:', error.response?.data)
    console.log('  Headers enviados:', error.config?.headers)
    return Promise.reject(error)
  }
)

export default api
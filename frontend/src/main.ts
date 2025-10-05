import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import './style.css'

import App from './App.vue'
import router from './router'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#F8BBD9',
          secondary: '#FFF0F5',
          accent: '#FFB6C1',
          background: '#FAFAFA',
          surface: '#FFFFFF',
          error: '#FF6B6B',
          warning: '#FFB74D',
          info: '#E1BEE7',
          success: '#C8E6C9',
          'on-primary': '#000000',
          'on-secondary': '#000000'
        }
      },
      dark: {
        colors: {
          primary: '#F8BBD9',
          secondary: '#2D2D2D',
          accent: '#FFB6C1',
          background: '#121212',
          surface: '#1E1E1E',
          error: '#FF6B6B',
          warning: '#FFB74D',
          info: '#E1BEE7',
          success: '#C8E6C9',
          'on-primary': '#000000',
          'on-secondary': '#FFFFFF'
        }
      }
    }
  }
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(vuetify)

app.mount('#app')
<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      app
      dark
      width="280"
      v-if="isAuthenticated"
      class="elegant-shadow"
    >
      <div class="pa-6 text-center">
        <img src="/images/Logo_reto-removebg-preview.png" alt="LashManager" class="sidebar-logo mb-2" @error="handleSidebarLogoError" />
        <div class="text-caption" style="color: rgba(255,255,255,0.8);">
          Sistema de Gestão Premium
        </div>
      </div>

      <v-divider class="mx-4" style="border-color: rgba(255,255,255,0.2);"></v-divider>

      <v-list nav class="pa-4">
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
          link
          class="mb-2 rounded-lg"
        >
          <template v-slot:prepend>
            <v-icon size="20">{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title class="font-weight-medium">{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app dark v-if="isAuthenticated" class="elegant-shadow" height="70">
      <v-app-bar-nav-icon @click="drawer = !drawer" class="ml-2"></v-app-bar-nav-icon>
      <img src="/images/Logo_reto-removebg-preview.png" alt="LashManager" class="appbar-logo ml-4" @error="handleAppbarLogoError" />
      <v-spacer></v-spacer>
      <v-btn icon size="large" @click="toggleTheme" class="mr-2">
        <v-icon>{{ themeStore.isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
      <v-btn icon size="large" @click="logout" class="mr-4">
        <v-icon>mdi-logout-variant</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <div class="global-background" v-if="isAuthenticated"></div>
      <div class="pa-6">
        <router-view />
      </div>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'

const drawer = ref(true)
const router = useRouter()
const theme = useTheme()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

const menuItems = [
  { title: 'Dashboard', icon: 'mdi-view-dashboard-outline', to: '/' },
  { title: 'Clientes', icon: 'mdi-account-heart-outline', to: '/clientes' },
  { title: 'Agenda', icon: 'mdi-calendar-heart', to: '/agenda' },
  { title: 'Funcionários', icon: 'mdi-account-star-outline', to: '/funcionarios' },
  { title: 'Procedimentos', icon: 'mdi-eye-plus-outline', to: '/procedimentos' },
  { title: 'Pagamentos', icon: 'mdi-credit-card-outline', to: '/pagamentos' },
  { title: 'Mensagens', icon: 'mdi-whatsapp', to: '/mensagens' }
]

const toggleTheme = () => {
  themeStore.toggleTheme()
  theme.global.name.value = themeStore.isDark ? 'dark' : 'light'
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

const handleSidebarLogoError = (event) => {
  event.target.outerHTML = '<div class="text-h5 font-weight-bold mb-2" style="color: white; letter-spacing: 2px;">✨ LashManager</div>'
}

const handleAppbarLogoError = (event) => {
  event.target.outerHTML = '<v-toolbar-title class="ml-4">💅 LashManager</v-toolbar-title>'
}

// Aplicar tema salvo
watch(() => themeStore.isDark, (isDark) => {
  theme.global.name.value = isDark ? 'dark' : 'light'
}, { immediate: true })
</script>

<style scoped>
.sidebar-logo {
  max-width: 180px;
  height: auto;
  filter: brightness(0) invert(1);
}

.appbar-logo {
  max-width: 120px;
  height: auto;
  filter: brightness(0) invert(1);
}
</style>
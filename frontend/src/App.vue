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
        <div class="text-h5 font-weight-bold mb-2" style="color: white; letter-spacing: 2px;">
          ✨ LashManager
        </div>
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
      <v-toolbar-title class="ml-4">💅 LashManager</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon size="large" @click="logout" class="mr-4">
        <v-icon>mdi-logout-variant</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <div class="pa-6">
        <router-view />
      </div>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const drawer = ref(true)
const router = useRouter()
const authStore = useAuthStore()

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

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
<template>
  <v-container fluid class="fill-height login-container">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="5" lg="4">
        <div class="text-center mb-8">
          <div class="text-h3 font-weight-bold text-gradient mb-2">
            ✨ LashManager
          </div>
          <div class="text-h6 text-grey-darken-1">
            Sistema Premium de Gestão
          </div>
        </div>
        
        <v-card class="glass-effect elegant-shadow pa-8">
          <v-form @submit.prevent="handleLogin">
            <v-text-field
              v-model="username"
              label="Usuário"
              prepend-inner-icon="mdi-account-outline"
              variant="outlined"
              class="mb-4"
              required
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Senha"
              prepend-inner-icon="mdi-lock-outline"
              type="password"
              variant="outlined"
              class="mb-6"
              required
            ></v-text-field>
            
            <v-btn
              color="primary"
              @click="handleLogin"
              :loading="loading"
              size="large"
              block
              class="pink-gradient elegant-shadow"
            >
              <v-icon left>mdi-login</v-icon>
              Entrar
            </v-btn>
          </v-form>
        </v-card>
        
        <div class="text-center mt-6 text-caption text-grey">
          Login: admin | Senha: admin123
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('admin')
const password = ref('admin123')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  const success = await authStore.login(username.value, password.value)
  
  if (success) {
    router.push('/')
  } else {
    alert('Credenciais inválidas')
  }
  
  loading.value = false
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #ffeef8 0%, #f8d7da 100%);
  min-height: 100vh;
}
</style>
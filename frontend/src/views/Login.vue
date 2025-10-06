<template>
  <v-container fluid class="fill-height login-container">
    <v-row align="center" justify="center" class="fill-height">
      <!-- Lado Esquerdo - Imagem -->
      <v-col cols="12" md="7" class="d-none d-md-flex align-center justify-center">
        <div class="image-container">
          <div class="floating-image">
            <img src="/images/lari_02.jpg" alt="Lash Designer" class="profile-image" @error="handleImageError" />
          </div>
          <div class="floating-elements">
            <div class="floating-icon icon-1">💅</div>
            <div class="floating-icon icon-2">✨</div>
            <div class="floating-icon icon-3">💕</div>
            <div class="floating-icon icon-4">🌸</div>
          </div>
        </div>
      </v-col>
      
      <!-- Lado Direito - Login -->
      <v-col cols="12" md="5" class="d-flex align-center justify-center">
        <div class="login-form-container">
          <div class="text-center mb-8 fade-in-up">
            <img src="/images/Logo_reto-removebg-preview.png" alt="LashManager" class="logo-image mb-4" @error="handleLogoError" />
            <div class="text-h6 text-grey-darken-1">
              Sistema Premium de Gestão
            </div>
          </div>
          
          <v-card class="glass-effect elegant-shadow pa-8 slide-in-right">
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Usuário"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                class="mb-4 input-animation"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Senha"
                prepend-inner-icon="mdi-lock-outline"
                type="password"
                variant="outlined"
                class="mb-6 input-animation"
                required
              ></v-text-field>
              
              <v-btn
                color="primary"
                @click="handleLogin"
                :loading="loading"
                size="large"
                block
                class="pink-gradient elegant-shadow button-hover"
              >
                <v-icon left>mdi-login</v-icon>
                Entrar
              </v-btn>
            </v-form>
          </v-card>
          

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
  
  try {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    
    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('token', data.access_token)
      window.location.href = '/'
    } else {
      alert('Credenciais inválidas')
    }
  } catch (error) {
    alert('Erro de conexão')
  }
  
  loading.value = false
}

const handleImageError = (event) => {
  event.target.src = '/images/placeholder.jpg'
}

const handleLogoError = (event) => {
  event.target.outerHTML = '<div class="text-h3 font-weight-bold text-gradient">✨ LashManager</div>'
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #ffeef8 0%, #f8d7da 100%);
  min-height: 100vh;
  overflow: hidden;
}

.image-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-image {
  animation: float 6s ease-in-out infinite;
  z-index: 2;
}

.profile-image {
  width: 350px;
  height: 350px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 20px 60px rgba(248, 187, 217, 0.4);
  border: 5px solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.profile-image:hover {
  transform: scale(1.05);
  box-shadow: 0 25px 80px rgba(248, 187, 217, 0.6);
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.floating-icon {
  position: absolute;
  font-size: 2rem;
  animation: floatIcon 4s ease-in-out infinite;
}

.icon-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.icon-2 {
  top: 30%;
  right: 15%;
  animation-delay: 1s;
}

.icon-3 {
  bottom: 25%;
  left: 15%;
  animation-delay: 2s;
}

.icon-4 {
  bottom: 35%;
  right: 10%;
  animation-delay: 3s;
}

.login-form-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}

.fade-in-up {
  animation: fadeInUp 1s ease-out;
}

.slide-in-right {
  animation: slideInRight 1.2s ease-out;
}

.fade-in {
  animation: fadeIn 1.5s ease-out;
}

.input-animation {
  transition: all 0.3s ease;
}

.input-animation:hover {
  transform: translateY(-2px);
}

.button-hover {
  transition: all 0.3s ease;
}

.button-hover:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(248, 187, 217, 0.4);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes floatIcon {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-15px) rotate(5deg);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.logo-image {
  max-width: 280px;
  height: auto;
  filter: drop-shadow(0 4px 8px rgba(248, 187, 217, 0.3));
  animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
}

@media (max-width: 960px) {
  .profile-image {
    width: 250px;
    height: 250px;
  }
  
  .floating-icon {
    font-size: 1.5rem;
  }
  
  .logo-image {
    max-width: 220px;
  }
}
</style>
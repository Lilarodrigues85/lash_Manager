<template>
  <div>
    <div class="mb-8">
      <div class="d-flex align-center mb-2">
        <img src="/images/Logo_redondo-removebg-preview.png" alt="Logo" class="dashboard-logo-small mr-3" @error="handleLogoError" />
        <h1 class="text-h3 font-weight-bold text-gradient">
        Dashboard
        </h1>
      </div>
      <p class="text-h6 text-grey-darken-1">Visão geral do seu salão</p>
    </div>

    <!-- Cards de Resumo -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="4">
        <v-card class="dashboard-card elegant-shadow pa-4 text-center">
          <v-icon size="32" class="mb-2" color="primary">
            mdi-calendar-today
          </v-icon>
          <div class="text-h5 font-weight-bold text-primary mb-1">
            {{ resumo.agendamentos_hoje }}
          </div>
          <div class="text-caption text-grey-darken-1">
            Agendamentos Hoje
          </div>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="4">
        <v-card class="dashboard-card elegant-shadow pa-4 text-center">
          <v-icon size="32" class="mb-2" color="success">
            mdi-cash
          </v-icon>
          <div class="text-h5 font-weight-bold text-success mb-1">
            R$ {{ formatCurrency(resumo.receita_dia) }}
          </div>
          <div class="text-caption text-grey-darken-1">
            Receita do Dia
          </div>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="4">
        <v-card class="dashboard-card elegant-shadow pa-4 text-center">
          <v-icon size="32" class="mb-2" color="success">
            mdi-currency-usd
          </v-icon>
          <div class="text-h5 font-weight-bold text-success mb-1">
            R$ {{ formatCurrency(resumo.receita_mes) }}
          </div>
          <div class="text-caption text-grey-darken-1">
            Receita do Mês
          </div>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="6">
        <v-card class="dashboard-card elegant-shadow pa-4 text-center">
          <v-icon size="32" class="mb-2" color="info">
            mdi-account-group
          </v-icon>
          <div class="text-h5 font-weight-bold text-info mb-1">
            {{ resumo.total_clientes }}
          </div>
          <div class="text-caption text-grey-darken-1">
            Total Clientes
          </div>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="6">
        <v-card class="dashboard-card elegant-shadow pa-4 text-center">
          <v-icon size="32" class="mb-2" color="warning">
            mdi-clock-outline
          </v-icon>
          <div class="text-h5 font-weight-bold text-warning mb-1">
            {{ resumo.agendamentos_pendentes }}
          </div>
          <div class="text-caption text-grey-darken-1">
            Agendamentos Pendentes
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Agenda de Hoje -->
    <v-row>
      <v-col cols="12" md="8">
        <v-card class="elegant-shadow">
          <v-card-title class="pa-6 pb-4">
            <v-icon left color="primary">mdi-calendar-today</v-icon>
            <span class="text-h5 font-weight-bold">Agenda de Hoje</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-0">
            <v-list v-if="agendaHoje.length" class="py-0">
              <v-list-item
                v-for="(agendamento, index) in agendaHoje"
                :key="agendamento.id"
                class="py-4 px-6"
                :class="{ 'border-b': index < agendaHoje.length - 1 }"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" class="mr-4">
                    <v-icon color="white">mdi-account</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium mb-1">
                  {{ agendamento.cliente_nome }}
                </v-list-item-title>
                <v-list-item-subtitle class="mb-2">
                  <v-icon size="16" class="mr-1">mdi-clock-outline</v-icon>
                  {{ formatTime(agendamento.data_hora) }} - {{ agendamento.funcionario_nome }}
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  <v-icon size="16" class="mr-1">mdi-eye-outline</v-icon>
                  {{ agendamento.procedimento_nome }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="getStatusColor(agendamento.status)" size="small">
                    {{ agendamento.status }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center py-12">
              <v-icon size="64" color="grey-lighten-2" class="mb-4">
                mdi-calendar-blank
              </v-icon>
              <div class="text-h6 text-grey">Nenhum agendamento para hoje</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Clientes Recentes -->
      <v-col cols="12" md="4">
        <v-card class="elegant-shadow">
          <v-card-title class="pa-6 pb-4">
            <v-icon left color="info">mdi-account-plus</v-icon>
            <span class="text-h5 font-weight-bold">Clientes Recentes</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-0">
            <v-list v-if="clientesRecentes.length" class="py-0">
              <v-list-item
                v-for="(cliente, index) in clientesRecentes"
                :key="cliente.id"
                class="py-4 px-6"
                :class="{ 'border-b': index < clientesRecentes.length - 1 }"
              >
                <template v-slot:prepend>
                  <v-avatar color="info" size="40" class="mr-4">
                    <span class="text-white font-weight-bold">
                      {{ cliente.nome.charAt(0) }}
                    </span>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium">
                  {{ cliente.nome }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  <v-icon size="16" class="mr-1">mdi-phone</v-icon>
                  {{ cliente.telefone }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { format } from 'date-fns'

const resumo = ref({
  agendamentos_hoje: 0,
  receita_dia: 0,
  receita_mes: 0,
  total_clientes: 0,
  agendamentos_pendentes: 0
})

const agendaHoje = ref([])
const clientesRecentes = ref([])

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

const formatTime = (dateTime: string) => {
  return format(new Date(dateTime), 'HH:mm')
}

const getStatusColor = (status: string) => {
  const colors = {
    'agendado': 'primary',
    'realizado': 'success',
    'cancelado': 'error'
  }
  return colors[status] || 'grey'
}

const loadDashboard = async () => {
  try {
    const [resumoRes, agendaRes, clientesRes] = await Promise.all([
      api.get('/dashboard/resumo'),
      api.get('/dashboard/agenda-hoje'),
      api.get('/dashboard/clientes-recentes')
    ])
    
    resumo.value = resumoRes.data
    agendaHoje.value = agendaRes.data
    clientesRecentes.value = clientesRes.data
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  }
}

const handleLogoError = (event) => {
  event.target.style.display = 'none'
}

onMounted(() => {
  // Aguardar um pouco para garantir que o token esteja carregado
  setTimeout(() => {
    const token = localStorage.getItem('token')
    console.log('Dashboard - Token no localStorage:', !!token)
    if (token) {
      loadDashboard()
    } else {
      console.log('Dashboard - Sem token, redirecionando para login')
      window.location.href = '/login'
    }
  }, 100)
})
</script>

<style scoped>


.dashboard-logo-small {
  width: 50px;
  height: 50px;
  filter: drop-shadow(0 2px 4px rgba(248, 187, 217, 0.3));
}

@media (max-width: 600px) {
  .dashboard-logo-small {
    width: 40px;
    height: 40px;
  }
}
</style>
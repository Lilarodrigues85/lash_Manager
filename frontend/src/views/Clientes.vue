<template>
  <v-container>
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-8">
          <div>
            <h1 class="text-h3 font-weight-bold text-gradient mb-2">
              👥 Clientes
            </h1>
            <p class="text-h6 text-grey-darken-1">Gerencie seus clientes</p>
          </div>
          <v-btn color="primary" size="large" @click="openDialog()" class="pink-gradient elegant-shadow">
            <v-icon left>mdi-plus</v-icon>
            Novo Cliente
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Alertas -->
    <v-row v-if="alert.show">
      <v-col cols="12">
        <v-alert
          :type="alert.type"
          :text="alert.message"
          closable
          @click:close="alert.show = false"
        ></v-alert>
      </v-col>
    </v-row>

    <!-- Filtros -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="search"
          label="Buscar por nome, telefone ou email"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          :loading="loading"
          @input="debouncedSearch"
          placeholder="Digite pelo menos 2 caracteres..."
          hint="Busca em tempo real"
          persistent-hint
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center">
        <v-chip v-if="clientes.length > 0" color="primary" variant="outlined">
          {{ clientes.length }} cliente(s) encontrado(s)
        </v-chip>
        <v-chip v-else-if="search && !loading" color="warning" variant="outlined">
          Nenhum cliente encontrado
        </v-chip>
      </v-col>
    </v-row>

    <!-- Lista de Clientes -->
    <v-row>
      <v-col cols="12">
        <v-card class="elegant-shadow">
          <v-data-table
            :headers="headers"
            :items="clientes"
            :loading="loading"
          >
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="viewClient(item)">
                mdi-eye
              </v-icon>
              <v-icon small class="mr-2" @click="editClient(item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="deleteClient(item)">
                mdi-delete
              </v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog Novo/Editar Cliente -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card class="elegant-shadow">
        <v-card-title class="pa-6 pb-4">
          <v-icon left color="primary">{{ editingClient ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          <span class="text-h5 font-weight-bold">
            {{ editingClient ? 'Editar Cliente' : 'Novo Cliente' }}
          </span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-6">
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="clientForm.nome"
              label="Nome Completo *"
              variant="outlined"
              prepend-inner-icon="mdi-account-outline"
              :rules="nameRules"
              :error-messages="errors.nome"
              required
              class="mb-4"
              @input="clearError('nome')"
            ></v-text-field>
            
            <v-text-field
              v-model="clientForm.telefone"
              label="Telefone *"
              variant="outlined"
              prepend-inner-icon="mdi-phone-outline"
              :rules="phoneRules"
              :error-messages="errors.telefone"
              required
              class="mb-4"
              @input="clearError('telefone')"
              placeholder="(11) 99999-9999"
            ></v-text-field>
            
            <v-text-field
              v-model="clientForm.email"
              label="Email"
              variant="outlined"
              prepend-inner-icon="mdi-email-outline"
              type="email"
              :rules="emailRules"
              :error-messages="errors.email"
              class="mb-4"
              @input="clearError('email')"
              placeholder="cliente@email.com"
            ></v-text-field>
            
            <v-textarea
              v-model="clientForm.observacoes"
              label="Observações"
              variant="outlined"
              prepend-inner-icon="mdi-note-text-outline"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" @click="closeDialog" class="mr-4">
            Cancelar
          </v-btn>
          <v-btn 
            color="primary" 
            @click="saveClient" 
            :disabled="!valid || saving" 
            :loading="saving"
            class="pink-gradient"
          >
            <v-icon left>mdi-content-save</v-icon>
            {{ saving ? 'Salvando...' : 'Salvar' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog Histórico -->
    <v-dialog v-model="historyDialog" max-width="900px">
      <v-card>
        <v-card-title class="pa-6 pb-4">
          <v-icon left color="primary">mdi-history</v-icon>
          <span class="text-h5 font-weight-bold">Histórico do Cliente</span>
        </v-card-title>
        <v-divider></v-divider>
        
        <v-card-text class="pa-6" v-if="selectedClient">
          <!-- Dados do Cliente -->
          <v-card class="mb-4" variant="outlined">
            <v-card-text>
              <h3 class="mb-2">{{ selectedClient.cliente.nome }}</h3>
              <p class="mb-1"><v-icon small>mdi-phone</v-icon> {{ selectedClient.cliente.telefone }}</p>
              <p class="mb-1" v-if="selectedClient.cliente.email"><v-icon small>mdi-email</v-icon> {{ selectedClient.cliente.email }}</p>
              <p class="mb-0" v-if="selectedClient.cliente.observacoes">
                <v-icon small>mdi-note</v-icon> {{ selectedClient.cliente.observacoes }}
              </p>
            </v-card-text>
          </v-card>

          <!-- Estatísticas -->
          <v-row class="mb-4">
            <v-col cols="4">
              <v-card color="primary" variant="tonal">
                <v-card-text class="text-center">
                  <div class="text-h4">{{ selectedClient.total_agendamentos }}</div>
                  <div class="text-caption">Agendamentos</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card color="success" variant="tonal">
                <v-card-text class="text-center">
                  <div class="text-h4">R$ {{ selectedClient.total_pago.toFixed(2) }}</div>
                  <div class="text-caption">Total Pago</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="4">
              <v-card color="warning" variant="tonal">
                <v-card-text class="text-center">
                  <div class="text-h4">R$ {{ selectedClient.total_pendente.toFixed(2) }}</div>
                  <div class="text-caption">Pendente</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Agendamentos -->
          <h3 class="mb-3">Agendamentos</h3>
          <v-timeline side="end" density="compact" v-if="selectedClient.agendamentos.length > 0">
            <v-timeline-item
              v-for="agendamento in selectedClient.agendamentos"
              :key="agendamento.id"
              dot-color="primary"
              size="small"
            >
              <v-card>
                <v-card-text>
                  <div class="d-flex justify-space-between align-center">
                    <div>
                      <strong>{{ new Date(agendamento.data_hora).toLocaleDateString('pt-BR') }}</strong>
                      <span class="ml-2">{{ new Date(agendamento.data_hora).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'}) }}</span>
                    </div>
                    <v-chip :color="getStatusColor(agendamento.status)" size="small">
                      {{ agendamento.status }}
                    </v-chip>
                  </div>
                  <p class="mb-0 mt-2" v-if="agendamento.observacoes">{{ agendamento.observacoes }}</p>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </v-timeline>
          <v-alert v-else type="info" variant="tonal">Nenhum agendamento encontrado</v-alert>
        </v-card-text>
        
        <v-divider></v-divider>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" @click="historyDialog = false">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const search = ref('')
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const valid = ref(false)
const editingClient = ref(null)
let searchTimeout = null

const clientes = ref([])
const selectedClient = ref(null)
const historyDialog = ref(false)

// Sistema de alertas
const alert = ref({
  show: false,
  type: 'success',
  message: ''
})

// Erros de validação
const errors = ref({
  nome: [],
  telefone: [],
  email: []
})

const headers = [
  { title: 'Nome', key: 'nome' },
  { title: 'Telefone', key: 'telefone' },
  { title: 'Email', key: 'email' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const clientForm = ref({
  nome: '',
  telefone: '',
  email: '',
  observacoes: ''
})

// Regras de validação
const nameRules = [
  v => !!v || 'Nome é obrigatório',
  v => (v && v.length >= 2) || 'Nome deve ter pelo menos 2 caracteres'
]

const phoneRules = [
  v => !!v || 'Telefone é obrigatório',
  v => (v && v.replace(/\D/g, '').length >= 10) || 'Telefone deve ter pelo menos 10 dígitos'
]

const emailRules = [
  v => !v || /.+@.+\..+/.test(v) || 'Email deve ser válido'
]

// Funções auxiliares
const showAlert = (type, message) => {
  alert.value = { show: true, type, message }
  setTimeout(() => {
    alert.value.show = false
  }, 5000)
}

const clearError = (field) => {
  errors.value[field] = []
}

const clearAllErrors = () => {
  Object.keys(errors.value).forEach(key => {
    errors.value[key] = []
  })
}

const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadClientes()
  }, 300)
}

const loadClientes = async () => {
  const searchTerm = search.value?.trim()
  
  if (searchTerm && searchTerm.length < 2) {
    return
  }
  
  loading.value = true
  try {
    const response = await api.get('/clientes', {
      params: { search: searchTerm }
    })
    
    if (response.data.success) {
      clientes.value = response.data.clientes
    } else {
      showAlert('error', response.data.error || 'Erro ao carregar clientes')
    }
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
    showAlert('error', 'Erro ao carregar clientes')
  }
  loading.value = false
}

const openDialog = (client = null) => {
  if (client) {
    editingClient.value = client
    clientForm.value = { ...client }
  } else {
    editingClient.value = null
    clientForm.value = {
      nome: '',
      telefone: '',
      email: '',
      observacoes: ''
    }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingClient.value = null
}

const saveClient = async () => {
  if (!valid.value) return
  
  saving.value = true
  clearAllErrors()
  
  try {
    let response
    
    if (editingClient.value) {
      response = await api.put(`/clientes/${editingClient.value.id}`, clientForm.value)
    } else {
      response = await api.post('/clientes', clientForm.value)
    }
    
    if (response.data.success) {
      showAlert('success', response.data.message)
      closeDialog()
      loadClientes()
    } else {
      showAlert('error', response.data.error)
    }
  } catch (error) {
    console.error('Erro ao salvar cliente:', error)
    
    if (error.response?.data?.error) {
      showAlert('error', error.response.data.error)
    } else {
      showAlert('error', 'Erro ao salvar cliente')
    }
  }
  
  saving.value = false
}

const viewClient = async (client) => {
  try {
    const response = await api.get(`/clientes/${client.id}`)
    if (response.data.success) {
      selectedClient.value = response.data
      historyDialog.value = true
    }
  } catch (error) {
    console.error('Erro ao carregar histórico:', error)
    showAlert('error', 'Erro ao carregar histórico do cliente')
  }
}

const editClient = (client) => {
  openDialog(client)
}

const deleteClient = async (client) => {
  if (confirm(`Tem certeza que deseja desativar o cliente ${client.nome}?\n\nO histórico será mantido.`)) {
    try {
      const response = await api.delete(`/clientes/${client.id}`)
      
      if (response.data.success) {
        showAlert('success', 'Cliente desativado com sucesso')
        loadClientes()
      } else {
        showAlert('error', response.data.error || 'Erro ao desativar cliente')
      }
    } catch (error) {
      console.error('Erro ao desativar cliente:', error)
      showAlert('error', 'Erro ao desativar cliente')
    }
  }
}

const getStatusColor = (status) => {
  const colors = {
    'agendado': 'blue',
    'confirmado': 'cyan',
    'em_andamento': 'orange',
    'concluido': 'green',
    'cancelado': 'red',
    'nao_compareceu': 'grey'
  }
  return colors[status] || 'grey'
}

onMounted(() => {
  loadClientes()
})
</script>
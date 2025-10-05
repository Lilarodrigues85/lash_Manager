<template>
  <v-container>
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

    <!-- Filtros -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="search"
          label="Buscar cliente"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          @input="loadClientes"
        ></v-text-field>
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
              label="Nome"
              variant="outlined"
              prepend-inner-icon="mdi-account-outline"
              :rules="[v => !!v || 'Nome é obrigatório']"
              required
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model="clientForm.telefone"
              label="Telefone"
              variant="outlined"
              prepend-inner-icon="mdi-phone-outline"
              :rules="[v => !!v || 'Telefone é obrigatório']"
              required
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model="clientForm.email"
              label="Email"
              variant="outlined"
              prepend-inner-icon="mdi-email-outline"
              type="email"
              class="mb-4"
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
          <v-btn color="primary" @click="saveClient" :disabled="!valid" class="pink-gradient">
            <v-icon left>mdi-content-save</v-icon>
            Salvar
          </v-btn>
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
const dialog = ref(false)
const valid = ref(false)
const editingClient = ref(null)

const clientes = ref([])

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

const loadClientes = async () => {
  loading.value = true
  try {
    const response = await api.get('/clientes', {
      params: { search: search.value }
    })
    clientes.value = response.data.clientes
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
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
  try {
    if (editingClient.value) {
      await api.put(`/clientes/${editingClient.value.id}`, clientForm.value)
    } else {
      await api.post('/clientes', clientForm.value)
    }
    closeDialog()
    loadClientes()
  } catch (error) {
    console.error('Erro ao salvar cliente:', error)
  }
}

const viewClient = (client) => {
  // Implementar visualização detalhada
  console.log('Ver cliente:', client)
}

const editClient = (client) => {
  openDialog(client)
}

const deleteClient = async (client) => {
  if (confirm('Tem certeza que deseja deletar este cliente?')) {
    try {
      await api.delete(`/clientes/${client.id}`)
      loadClientes()
    } catch (error) {
      console.error('Erro ao deletar cliente:', error)
    }
  }
}

onMounted(() => {
  loadClientes()
})
</script>
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h1 class="text-h4">Funcionários</h1>
          <v-btn color="primary" @click="openDialog()">
            <v-icon left>mdi-plus</v-icon>
            Novo Funcionário
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="headers"
            :items="funcionarios"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.porcentagem="{ item }">
              {{ item.porcentagem }}%
            </template>
            <template v-slot:item.ativo="{ item }">
              <v-chip :color="item.ativo ? 'success' : 'error'">
                {{ item.ativo ? 'Ativo' : 'Inativo' }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="editFuncionario(item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="toggleFuncionario(item)">
                {{ item.ativo ? 'mdi-account-off' : 'mdi-account-check' }}
              </v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingFuncionario ? 'Editar Funcionário' : 'Novo Funcionário' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="funcionarioForm.nome"
              label="Nome"
              :rules="[v => !!v || 'Nome é obrigatório']"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="funcionarioForm.especialidade"
              label="Especialidade"
              :rules="[v => !!v || 'Especialidade é obrigatória']"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="funcionarioForm.telefone"
              label="Telefone"
            ></v-text-field>
            
            <v-text-field
              v-model="funcionarioForm.porcentagem"
              label="Porcentagem (%)"
              type="number"
              step="0.01"
              min="0"
              max="100"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveFuncionario">
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

const loading = ref(false)
const dialog = ref(false)
const valid = ref(false)
const editingFuncionario = ref(null)

const funcionarios = ref([])

const headers = [
  { title: 'Nome', key: 'nome' },
  { title: 'Especialidade', key: 'especialidade' },
  { title: 'Telefone', key: 'telefone' },
  { title: 'Porcentagem', key: 'porcentagem' },
  { title: 'Status', key: 'ativo' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const funcionarioForm = ref({
  nome: '',
  especialidade: '',
  telefone: '',
  porcentagem: 25.00
})

const loadFuncionarios = async () => {
  loading.value = true
  try {
    const response = await api.get('/funcionarios')
    funcionarios.value = response.data
  } catch (error) {
    console.error('Erro ao carregar funcionários:', error)
  }
  loading.value = false
}

const openDialog = (funcionario = null) => {
  if (funcionario) {
    editingFuncionario.value = funcionario
    funcionarioForm.value = { ...funcionario }
  } else {
    editingFuncionario.value = null
    funcionarioForm.value = {
      nome: '',
      especialidade: '',
      telefone: '',
      porcentagem: 25.00
    }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingFuncionario.value = null
}

const saveFuncionario = async () => {
  // Validação manual
  if (!funcionarioForm.value.nome || !funcionarioForm.value.especialidade) {
    alert('Nome e Especialidade são obrigatórios')
    return
  }
  
  try {
    console.log('Dados enviados:', funcionarioForm.value)
    
    let response
    if (editingFuncionario.value) {
      response = await api.put(`/funcionarios/${editingFuncionario.value.id}`, funcionarioForm.value)
    } else {
      response = await api.post('/funcionarios', funcionarioForm.value)
    }
    
    console.log('Resposta:', response.data)
    closeDialog()
    loadFuncionarios()
  } catch (error) {
    console.error('Erro completo:', error)
    console.error('Resposta do erro:', error.response?.data)
    alert(`Erro ao salvar funcionário: ${error.response?.data?.error || error.message}`)
  }
}

const editFuncionario = (funcionario) => {
  openDialog(funcionario)
}

const toggleFuncionario = async (funcionario) => {
  try {
    await api.put(`/funcionarios/${funcionario.id}`, { ativo: !funcionario.ativo })
    loadFuncionarios()
  } catch (error) {
    console.error('Erro ao alterar status:', error)
  }
}

onMounted(() => {
  loadFuncionarios()
})
</script>
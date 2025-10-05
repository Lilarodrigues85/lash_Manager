<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h1 class="text-h4">Procedimentos</h1>
          <v-btn color="primary" @click="openDialog()">
            <v-icon left>mdi-plus</v-icon>
            Novo Procedimento
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="headers"
            :items="procedimentos"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.preco="{ item }">
              R$ {{ item.preco.toFixed(2) }}
            </template>
            <template v-slot:item.duracao_minutos="{ item }">
              {{ item.duracao_minutos }} min
            </template>
            <template v-slot:item.ativo="{ item }">
              <v-chip :color="item.ativo ? 'success' : 'error'">
                {{ item.ativo ? 'Ativo' : 'Inativo' }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="editProcedimento(item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="toggleProcedimento(item)">
                {{ item.ativo ? 'mdi-eye-off' : 'mdi-eye' }}
              </v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingProcedimento ? 'Editar Procedimento' : 'Novo Procedimento' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="procedimentoForm.nome"
              label="Nome"
              :rules="[v => !!v || 'Nome é obrigatório']"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="procedimentoForm.preco"
              label="Preço"
              type="number"
              step="0.01"
              :rules="[v => !!v || 'Preço é obrigatório']"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="procedimentoForm.duracao_minutos"
              label="Duração (minutos)"
              type="number"
              :rules="[v => !!v || 'Duração é obrigatória']"
              required
            ></v-text-field>
            
            <v-select
              v-model="procedimentoForm.funcionario_id"
              :items="funcionarios"
              item-title="nome"
              item-value="id"
              label="Funcionário"
              :rules="[v => !!v || 'Funcionário é obrigatório']"
              required
            ></v-select>
            
            <v-textarea
              v-model="procedimentoForm.descricao"
              label="Descrição"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveProcedimento" :disabled="!valid">
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
const editingProcedimento = ref(null)

const procedimentos = ref([])
const funcionarios = ref([])

const headers = [
  { title: 'Nome', key: 'nome' },
  { title: 'Preço', key: 'preco' },
  { title: 'Duração', key: 'duracao_minutos' },
  { title: 'Funcionário', key: 'funcionario_nome' },
  { title: 'Status', key: 'ativo' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const procedimentoForm = ref({
  nome: '',
  preco: '',
  duracao_minutos: '',
  funcionario_id: null,
  descricao: ''
})

const loadProcedimentos = async () => {
  loading.value = true
  try {
    const response = await api.get('/procedimentos')
    procedimentos.value = response.data
  } catch (error) {
    console.error('Erro ao carregar procedimentos:', error)
  }
  loading.value = false
}

const loadFuncionarios = async () => {
  try {
    const response = await api.get('/funcionarios')
    funcionarios.value = response.data
  } catch (error) {
    console.error('Erro ao carregar funcionários:', error)
  }
}

const openDialog = (procedimento = null) => {
  if (procedimento) {
    editingProcedimento.value = procedimento
    procedimentoForm.value = { ...procedimento }
  } else {
    editingProcedimento.value = null
    procedimentoForm.value = {
      nome: '',
      preco: '',
      duracao_minutos: '',
      funcionario_id: null,
      descricao: ''
    }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingProcedimento.value = null
}

const saveProcedimento = async () => {
  try {
    if (editingProcedimento.value) {
      await api.put(`/procedimentos/${editingProcedimento.value.id}`, procedimentoForm.value)
    } else {
      await api.post('/procedimentos', procedimentoForm.value)
    }
    closeDialog()
    loadProcedimentos()
  } catch (error) {
    console.error('Erro ao salvar procedimento:', error)
  }
}

const editProcedimento = (procedimento) => {
  openDialog(procedimento)
}

const toggleProcedimento = async (procedimento) => {
  try {
    await api.put(`/procedimentos/${procedimento.id}`, { ativo: !procedimento.ativo })
    loadProcedimentos()
  } catch (error) {
    console.error('Erro ao alterar status:', error)
  }
}

onMounted(() => {
  loadProcedimentos()
  loadFuncionarios()
})
</script>
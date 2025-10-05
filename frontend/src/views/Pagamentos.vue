<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h1 class="text-h4">Pagamentos</h1>
          <v-btn color="primary" @click="openDialog()">
            <v-icon left>mdi-plus</v-icon>
            Novo Pagamento
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Tabs -->
    <v-row>
      <v-col cols="12">
        <v-tabs v-model="tab">
          <v-tab value="pagamentos">Pagamentos</v-tab>
          <v-tab value="pendentes">Pendentes</v-tab>
        </v-tabs>
      </v-col>
    </v-row>

    <v-window v-model="tab">
      <!-- Tab Pagamentos -->
      <v-window-item value="pagamentos">
        <v-card>
          <v-data-table
            :headers="headersPagamentos"
            :items="pagamentos"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.valor="{ item }">
              R$ {{ item.valor.toFixed(2) }}
            </template>
            <template v-slot:item.data_pagamento="{ item }">
              {{ formatDate(item.data_pagamento) }}
            </template>
            <template v-slot:item.status="{ item }">
              <v-chip :color="getStatusColor(item.status)">
                {{ item.status }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon small class="mr-2" @click="editPagamento(item)">
                mdi-pencil
              </v-icon>
              <v-icon small @click="deletePagamento(item)">
                mdi-delete
              </v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>

      <!-- Tab Pendentes -->
      <v-window-item value="pendentes">
        <v-card>
          <v-data-table
            :headers="headersPendentes"
            :items="pendentes"
            :loading="loadingPendentes"
            class="elevation-1"
          >
            <template v-slot:item.valor_devido="{ item }">
              R$ {{ item.valor_devido.toFixed(2) }}
            </template>
            <template v-slot:item.valor_pago="{ item }">
              R$ {{ item.valor_pago.toFixed(2) }}
            </template>
            <template v-slot:item.valor_pendente="{ item }">
              <span class="text-error font-weight-bold">
                R$ {{ item.valor_pendente.toFixed(2) }}
              </span>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn small color="success" @click="pagarPendente(item)">
                Pagar
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>
    </v-window>

    <!-- Dialog Novo/Editar Pagamento -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingPagamento ? 'Editar Pagamento' : 'Novo Pagamento' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-select
              v-model="pagamentoForm.cliente_id"
              :items="clientes"
              item-title="nome"
              item-value="id"
              label="Cliente"
              :rules="[v => !!v || 'Cliente é obrigatório']"
              required
            ></v-select>
            
            <v-text-field
              v-model="pagamentoForm.valor"
              label="Valor"
              type="number"
              step="0.01"
              :rules="[v => !!v || 'Valor é obrigatório']"
              required
            ></v-text-field>
            
            <v-select
              v-model="pagamentoForm.forma_pagamento"
              :items="formasPagamento"
              label="Forma de Pagamento"
              :rules="[v => !!v || 'Forma de pagamento é obrigatória']"
              required
            ></v-select>
            
            <v-text-field
              v-model="pagamentoForm.data_pagamento"
              label="Data do Pagamento"
              type="datetime-local"
            ></v-text-field>
            
            <v-textarea
              v-model="pagamentoForm.observacoes"
              label="Observações"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="savePagamento" :disabled="!valid">
            Salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from '../services/api'
import { format } from 'date-fns'

const tab = ref('pagamentos')
const loading = ref(false)
const loadingPendentes = ref(false)
const dialog = ref(false)
const valid = ref(false)
const editingPagamento = ref(null)

const pagamentos = ref([])
const pendentes = ref([])
const clientes = ref([])

const headersPagamentos = [
  { title: 'Cliente', key: 'cliente_nome' },
  { title: 'Valor', key: 'valor' },
  { title: 'Forma', key: 'forma_pagamento' },
  { title: 'Data', key: 'data_pagamento' },
  { title: 'Status', key: 'status' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const headersPendentes = [
  { title: 'Cliente', key: 'agendamento.cliente_nome' },
  { title: 'Procedimento', key: 'agendamento.procedimento_nome' },
  { title: 'Valor Devido', key: 'valor_devido' },
  { title: 'Valor Pago', key: 'valor_pago' },
  { title: 'Valor Pendente', key: 'valor_pendente' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const formasPagamento = ['dinheiro', 'cartao', 'pix']

const pagamentoForm = ref({
  cliente_id: null,
  valor: '',
  forma_pagamento: '',
  data_pagamento: '',
  observacoes: ''
})

const formatDate = (dateTime: string) => {
  return format(new Date(dateTime), 'dd/MM/yyyy HH:mm')
}

const getStatusColor = (status: string) => {
  const colors = {
    'pago': 'success',
    'pendente': 'warning',
    'cancelado': 'error'
  }
  return colors[status] || 'grey'
}

const loadPagamentos = async () => {
  loading.value = true
  try {
    const response = await api.get('/pagamentos')
    pagamentos.value = response.data.pagamentos
  } catch (error) {
    console.error('Erro ao carregar pagamentos:', error)
  }
  loading.value = false
}

const loadPendentes = async () => {
  loadingPendentes.value = true
  try {
    const response = await api.get('/pagamentos/pendentes')
    pendentes.value = response.data
  } catch (error) {
    console.error('Erro ao carregar pendentes:', error)
  }
  loadingPendentes.value = false
}

const loadClientes = async () => {
  try {
    const response = await api.get('/clientes')
    clientes.value = response.data.clientes
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
  }
}

const openDialog = (pagamento = null) => {
  if (pagamento) {
    editingPagamento.value = pagamento
    pagamentoForm.value = {
      ...pagamento,
      data_pagamento: format(new Date(pagamento.data_pagamento), "yyyy-MM-dd'T'HH:mm")
    }
  } else {
    editingPagamento.value = null
    pagamentoForm.value = {
      cliente_id: null,
      valor: '',
      forma_pagamento: '',
      data_pagamento: format(new Date(), "yyyy-MM-dd'T'HH:mm"),
      observacoes: ''
    }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingPagamento.value = null
}

const savePagamento = async () => {
  try {
    if (editingPagamento.value) {
      await api.put(`/pagamentos/${editingPagamento.value.id}`, pagamentoForm.value)
    } else {
      await api.post('/pagamentos', pagamentoForm.value)
    }
    closeDialog()
    loadPagamentos()
  } catch (error) {
    console.error('Erro ao salvar pagamento:', error)
  }
}

const editPagamento = (pagamento) => {
  openDialog(pagamento)
}

const deletePagamento = async (pagamento) => {
  if (confirm('Tem certeza que deseja deletar este pagamento?')) {
    try {
      await api.delete(`/pagamentos/${pagamento.id}`)
      loadPagamentos()
    } catch (error) {
      console.error('Erro ao deletar pagamento:', error)
    }
  }
}

const pagarPendente = (pendente) => {
  pagamentoForm.value = {
    cliente_id: pendente.agendamento.cliente_id,
    valor: pendente.valor_pendente.toString(),
    forma_pagamento: '',
    data_pagamento: format(new Date(), "yyyy-MM-dd'T'HH:mm"),
    observacoes: `Pagamento do procedimento: ${pendente.agendamento.procedimento_nome}`
  }
  dialog.value = true
}

watch(tab, (newTab) => {
  if (newTab === 'pagamentos') {
    loadPagamentos()
  } else if (newTab === 'pendentes') {
    loadPendentes()
  }
})

onMounted(() => {
  loadPagamentos()
  loadClientes()
})
</script>
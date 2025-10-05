<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h1 class="text-h4">Agenda</h1>
          <v-btn color="primary" @click="openDialog()">
            <v-icon left>mdi-plus</v-icon>
            Novo Agendamento
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Filtros -->
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          v-model="selectedFuncionario"
          :items="funcionarios"
          item-title="nome"
          item-value="id"
          label="Funcionário"
          clearable
          @update:model-value="loadAgendamentos"
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model="dataInicio"
          label="Data Início"
          type="date"
          @change="loadAgendamentos"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          v-model="dataFim"
          label="Data Fim"
          type="date"
          @change="loadAgendamentos"
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- Lista de Agendamentos -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="headers"
            :items="agendamentos"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.data_hora="{ item }">
              {{ formatDateTime(item.data_hora) }}
            </template>
            <template v-slot:item.status="{ item }">
              <v-chip :color="getStatusColor(item.status)">
                {{ item.status }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn icon size="small" @click="sendWhatsApp(item, 'confirmacao')" class="mr-1">
                <v-icon color="success">mdi-whatsapp</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="editAgendamento(item)" class="mr-1">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="cancelAgendamento(item)">
                <v-icon color="error">mdi-cancel</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog Novo/Editar Agendamento -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingAgendamento ? 'Editar Agendamento' : 'Novo Agendamento' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-select
              v-model="agendamentoForm.cliente_id"
              :items="clientes"
              item-title="nome"
              item-value="id"
              label="Cliente"
              :rules="[v => !!v || 'Cliente é obrigatório']"
              required
            ></v-select>
            
            <v-select
              v-model="agendamentoForm.funcionario_id"
              :items="funcionarios"
              item-title="nome"
              item-value="id"
              label="Funcionário"
              :rules="[v => !!v || 'Funcionário é obrigatório']"
              required
              @update:model-value="loadProcedimentos"
            ></v-select>
            
            <v-select
              v-model="agendamentoForm.procedimento_id"
              :items="procedimentos"
              item-title="nome"
              item-value="id"
              label="Procedimento"
              :rules="[v => !!v || 'Procedimento é obrigatório']"
              required
            ></v-select>
            
            <v-text-field
              v-model="agendamentoForm.data"
              label="Data"
              type="date"
              :rules="[v => !!v || 'Data é obrigatória']"
              required
              @change="loadHorariosDisponiveis"
            ></v-text-field>
            
            <v-select
              v-model="agendamentoForm.horario"
              :items="horariosDisponiveis"
              label="Horário"
              :rules="[v => !!v || 'Horário é obrigatório']"
              required
            ></v-select>
            
            <v-textarea
              v-model="agendamentoForm.observacoes"
              label="Observações"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveAgendamento" :disabled="!valid">
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
import { format } from 'date-fns'

const loading = ref(false)
const dialog = ref(false)
const valid = ref(false)
const editingAgendamento = ref(null)

const selectedFuncionario = ref(null)
const dataInicio = ref('')
const dataFim = ref('')

const agendamentos = ref([])
const clientes = ref([])
const funcionarios = ref([])
const procedimentos = ref([])
const horariosDisponiveis = ref([])

const headers = [
  { title: 'Cliente', key: 'cliente_nome' },
  { title: 'Funcionário', key: 'funcionario_nome' },
  { title: 'Procedimento', key: 'procedimento_nome' },
  { title: 'Data/Hora', key: 'data_hora' },
  { title: 'Status', key: 'status' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const agendamentoForm = ref({
  cliente_id: null,
  funcionario_id: null,
  procedimento_id: null,
  data: '',
  horario: '',
  observacoes: ''
})

const formatDateTime = (dateTime: string) => {
  return format(new Date(dateTime), 'dd/MM/yyyy HH:mm')
}

const getStatusColor = (status: string) => {
  const colors = {
    'agendado': 'primary',
    'realizado': 'success',
    'cancelado': 'error'
  }
  return colors[status] || 'grey'
}

const loadAgendamentos = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedFuncionario.value) params.funcionario_id = selectedFuncionario.value
    if (dataInicio.value) params.data_inicio = dataInicio.value
    if (dataFim.value) params.data_fim = dataFim.value
    
    const response = await api.get('/agendamentos', { params })
    agendamentos.value = response.data
  } catch (error) {
    console.error('Erro ao carregar agendamentos:', error)
  }
  loading.value = false
}

const loadClientes = async () => {
  try {
    const response = await api.get('/clientes')
    clientes.value = response.data.clientes
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
  }
}

const loadFuncionarios = async () => {
  try {
    const response = await api.get('/funcionarios')
    funcionarios.value = response.data
  } catch (error) {
    console.error('Erro ao carregar funcionários:', error)
  }
}

const loadProcedimentos = async () => {
  if (!agendamentoForm.value.funcionario_id) return
  
  try {
    const response = await api.get('/procedimentos', {
      params: { funcionario_id: agendamentoForm.value.funcionario_id }
    })
    procedimentos.value = response.data
  } catch (error) {
    console.error('Erro ao carregar procedimentos:', error)
  }
}

const loadHorariosDisponiveis = async () => {
  if (!agendamentoForm.value.data || !agendamentoForm.value.funcionario_id) return
  
  try {
    const response = await api.get('/agendamentos/horarios-disponiveis', {
      params: {
        data: agendamentoForm.value.data,
        funcionario_id: agendamentoForm.value.funcionario_id
      }
    })
    horariosDisponiveis.value = response.data
  } catch (error) {
    console.error('Erro ao carregar horários:', error)
  }
}

const openDialog = (agendamento = null) => {
  if (agendamento) {
    editingAgendamento.value = agendamento
    const dataHora = new Date(agendamento.data_hora)
    agendamentoForm.value = {
      cliente_id: agendamento.cliente_id,
      funcionario_id: agendamento.funcionario_id,
      procedimento_id: agendamento.procedimento_id,
      data: format(dataHora, 'yyyy-MM-dd'),
      horario: format(dataHora, 'HH:mm'),
      observacoes: agendamento.observacoes
    }
    loadProcedimentos()
  } else {
    editingAgendamento.value = null
    agendamentoForm.value = {
      cliente_id: null,
      funcionario_id: null,
      procedimento_id: null,
      data: '',
      horario: '',
      observacoes: ''
    }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingAgendamento.value = null
}

const saveAgendamento = async () => {
  try {
    const dataHora = `${agendamentoForm.value.data}T${agendamentoForm.value.horario}:00`
    const payload = {
      ...agendamentoForm.value,
      data_hora: dataHora
    }
    delete payload.data
    delete payload.horario
    
    if (editingAgendamento.value) {
      await api.put(`/agendamentos/${editingAgendamento.value.id}`, payload)
    } else {
      await api.post('/agendamentos', payload)
    }
    closeDialog()
    loadAgendamentos()
    
    // Abrir WhatsApp automaticamente após criar agendamento
    if (!editingAgendamento.value && response.data.whatsapp_url) {
      setTimeout(() => {
        if (confirm('Deseja enviar mensagem de confirmação via WhatsApp?')) {
          window.open(response.data.whatsapp_url, '_blank')
        }
      }, 500)
    }
  } catch (error) {
    console.error('Erro ao salvar agendamento:', error)
    alert('Erro ao salvar agendamento')
  }
}

const editAgendamento = (agendamento) => {
  openDialog(agendamento)
}

const sendWhatsApp = async (agendamento, tipo) => {
  try {
    const response = await api.get(`/mensagens/${tipo}/${agendamento.id}`)
    window.open(response.data.whatsapp_url, '_blank')
  } catch (error) {
    console.error('Erro ao gerar mensagem:', error)
  }
}

const cancelAgendamento = async (agendamento) => {
  if (confirm('Tem certeza que deseja cancelar este agendamento?')) {
    try {
      await api.put(`/agendamentos/${agendamento.id}`, { status: 'cancelado' })
      loadAgendamentos()
    } catch (error) {
      console.error('Erro ao cancelar agendamento:', error)
    }
  }
}

onMounted(() => {
  loadAgendamentos()
  loadClientes()
  loadFuncionarios()
})
</script>
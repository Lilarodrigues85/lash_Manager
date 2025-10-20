<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Gestão de Usuários</span>
            <v-btn color="primary" @click="dialogNovo = true">
              <v-icon left>mdi-plus</v-icon>
              Novo Usuário
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="usuarios"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.tipo_usuario="{ item }">
                <v-chip :color="item.tipo_usuario === 'admin' ? 'red' : 'blue'" dark small>
                  {{ item.tipo_usuario === 'admin' ? 'Administrador' : 'Funcionário' }}
                </v-chip>
              </template>

              <template v-slot:item.ativo="{ item }">
                <v-chip :color="item.ativo ? 'success' : 'error'" small>
                  {{ item.ativo ? 'Ativo' : 'Inativo' }}
                </v-chip>
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn icon small @click="editarUsuario(item)">
                  <v-icon small>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon small @click="desativarUsuario(item)" v-if="item.ativo">
                  <v-icon small>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog Novo/Editar -->
    <v-dialog v-model="dialogNovo" max-width="600px">
      <v-card>
        <v-card-title>
          {{ usuarioEditando ? 'Editar Usuário' : 'Novo Usuário' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="formUsuario.nome"
              label="Nome Completo"
              :rules="[v => !!v || 'Nome é obrigatório']"
              required
            />
            <v-text-field
              v-model="formUsuario.username"
              label="Username"
              :rules="[v => !!v || 'Username é obrigatório']"
              :disabled="!!usuarioEditando"
              required
            />
            <v-text-field
              v-model="formUsuario.email"
              label="Email"
              type="email"
              :rules="[v => !!v || 'Email é obrigatório']"
              required
            />
            <v-text-field
              v-model="formUsuario.password"
              label="Senha"
              type="password"
              :rules="usuarioEditando ? [] : [v => !!v || 'Senha é obrigatória']"
              :hint="usuarioEditando ? 'Deixe em branco para manter a senha atual' : ''"
            />
            <v-select
              v-model="formUsuario.tipo_usuario"
              :items="tiposUsuario"
              label="Tipo de Usuário"
              item-title="text"
              item-value="value"
              :rules="[v => !!v || 'Tipo é obrigatório']"
              required
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="fecharDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="salvarUsuario">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const loading = ref(false)
const dialogNovo = ref(false)
const usuarioEditando = ref<any>(null)
const usuarios = ref<any[]>([])

const headers = [
  { title: 'Nome', key: 'nome' },
  { title: 'Username', key: 'username' },
  { title: 'Email', key: 'email' },
  { title: 'Tipo', key: 'tipo_usuario' },
  { title: 'Status', key: 'ativo' },
  { title: 'Ações', key: 'actions', sortable: false }
]

const tiposUsuario = [
  { text: 'Administrador', value: 'admin' },
  { text: 'Funcionário', value: 'funcionario' }
]

const formUsuario = ref({
  nome: '',
  username: '',
  email: '',
  password: '',
  tipo_usuario: 'funcionario'
})

const carregarUsuarios = async () => {
  loading.value = true
  try {
    const response = await api.get('/usuarios')
    usuarios.value = response.data
  } catch (error) {
    console.error('Erro ao carregar usuários:', error)
  } finally {
    loading.value = false
  }
}

const editarUsuario = (usuario: any) => {
  usuarioEditando.value = usuario
  formUsuario.value = {
    nome: usuario.nome,
    username: usuario.username,
    email: usuario.email,
    password: '',
    tipo_usuario: usuario.tipo_usuario
  }
  dialogNovo.value = true
}

const salvarUsuario = async () => {
  try {
    if (usuarioEditando.value) {
      await api.put(`/usuarios/${usuarioEditando.value.id}`, formUsuario.value)
    } else {
      await api.post('/usuarios', formUsuario.value)
    }
    await carregarUsuarios()
    fecharDialog()
  } catch (error: any) {
    alert(error.response?.data?.error || 'Erro ao salvar usuário')
  }
}

const desativarUsuario = async (usuario: any) => {
  if (confirm(`Desativar usuário ${usuario.nome}?`)) {
    try {
      await api.delete(`/usuarios/${usuario.id}`)
      await carregarUsuarios()
    } catch (error) {
      alert('Erro ao desativar usuário')
    }
  }
}

const fecharDialog = () => {
  dialogNovo.value = false
  usuarioEditando.value = null
  formUsuario.value = {
    nome: '',
    username: '',
    email: '',
    password: '',
    tipo_usuario: 'funcionario'
  }
}

onMounted(() => {
  carregarUsuarios()
})
</script>

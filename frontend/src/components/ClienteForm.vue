<template>
  <v-form ref="form" v-model="valid" @submit.prevent="handleSubmit">
    <v-text-field
      v-model="formData.nome"
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
      v-model="formData.telefone"
      label="Telefone *"
      variant="outlined"
      prepend-inner-icon="mdi-phone-outline"
      :rules="phoneRules"
      :error-messages="errors.telefone"
      required
      class="mb-4"
      @input="formatPhone"
      @blur="clearError('telefone')"
      placeholder="(11) 99999-9999"
    ></v-text-field>
    
    <v-text-field
      v-model="formData.email"
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
      v-model="formData.observacoes"
      label="Observações"
      variant="outlined"
      prepend-inner-icon="mdi-note-text-outline"
      rows="3"
      placeholder="Informações adicionais sobre o cliente..."
    ></v-textarea>
    
    <div class="d-flex justify-end mt-6">
      <v-btn variant="outlined" @click="$emit('cancel')" class="mr-4">
        Cancelar
      </v-btn>
      <v-btn 
        color="primary" 
        type="submit"
        :disabled="!valid || loading" 
        :loading="loading"
        class="pink-gradient"
      >
        <v-icon left>mdi-content-save</v-icon>
        {{ loading ? 'Salvando...' : 'Salvar' }}
      </v-btn>
    </div>
  </v-form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface ClienteData {
  nome: string
  telefone: string
  email: string
  observacoes: string
}

interface Props {
  modelValue: ClienteData
  loading?: boolean
  errors?: Record<string, string[]>
}

interface Emits {
  (e: 'update:modelValue', value: ClienteData): void
  (e: 'submit', value: ClienteData): void
  (e: 'cancel'): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  errors: () => ({})
})

const emit = defineEmits<Emits>()

const form = ref()
const valid = ref(false)
const formData = ref<ClienteData>({ ...props.modelValue })

// Regras de validação
const nameRules = [
  (v: string) => !!v || 'Nome é obrigatório',
  (v: string) => (v && v.length >= 2) || 'Nome deve ter pelo menos 2 caracteres'
]

const phoneRules = [
  (v: string) => !!v || 'Telefone é obrigatório',
  (v: string) => (v && v.replace(/\D/g, '').length >= 10) || 'Telefone deve ter pelo menos 10 dígitos'
]

const emailRules = [
  (v: string) => !v || /.+@.+\..+/.test(v) || 'Email deve ser válido'
]

// Watchers
watch(() => props.modelValue, (newValue) => {
  formData.value = { ...newValue }
}, { deep: true })

watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// Métodos
const clearError = (field: string) => {
  // Implementar lógica para limpar erros específicos
}

const formatPhone = () => {
  let phone = formData.value.telefone.replace(/\D/g, '')
  
  if (phone.length <= 11) {
    phone = phone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
    if (phone.length < 14) {
      phone = phone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3')
    }
  }
  
  formData.value.telefone = phone
}

const handleSubmit = () => {
  if (valid.value) {
    emit('submit', formData.value)
  }
}
</script>
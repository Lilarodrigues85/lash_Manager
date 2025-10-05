<template>
  <div>
    <div class="mb-8">
      <h1 class="text-h3 font-weight-bold text-gradient mb-2">
        💬 Mensagens WhatsApp
      </h1>
      <p class="text-h6 text-grey-darken-1">Gerencie mensagens automáticas</p>
    </div>

    <v-row>
      <v-col cols="12" md="4" v-for="template in templates" :key="template.tipo">
        <v-card class="elegant-shadow pa-6 text-center">
          <v-icon size="48" :color="template.color" class="mb-4">
            {{ template.icon }}
          </v-icon>
          <div class="text-h5 font-weight-bold mb-2">
            {{ template.titulo }}
          </div>
          <div class="text-body-2 text-grey-darken-1 mb-4">
            {{ template.descricao }}
          </div>
          <v-btn 
            :color="template.color" 
            variant="outlined" 
            @click="previewTemplate(template.tipo)"
          >
            <v-icon left>mdi-eye</v-icon>
            Visualizar
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog Preview -->
    <v-dialog v-model="previewDialog" max-width="500px">
      <v-card class="elegant-shadow">
        <v-card-title class="pa-6 pb-4">
          <v-icon left color="success">mdi-whatsapp</v-icon>
          <span class="text-h5 font-weight-bold">Preview da Mensagem</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-6">
          <div class="whatsapp-preview">
            <pre class="text-body-2">{{ previewText }}</pre>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" @click="previewDialog = false">
            Fechar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const previewDialog = ref(false)
const previewText = ref('')

const templates = [
  {
    tipo: 'confirmacao',
    titulo: 'Confirmação',
    descricao: 'Enviada automaticamente após criar agendamento',
    icon: 'mdi-check-circle',
    color: 'success'
  },
  {
    tipo: 'lembrete',
    titulo: 'Lembrete',
    descricao: 'Lembrete 24h antes do agendamento',
    icon: 'mdi-bell',
    color: 'warning'
  },
  {
    tipo: 'agradecimento',
    titulo: 'Agradecimento',
    descricao: 'Enviada após procedimento realizado',
    icon: 'mdi-heart',
    color: 'pink'
  }
]

const previewTemplate = (tipo: string) => {
  const previews = {
    confirmacao: `✨ *Agendamento Confirmado* ✨

Olá Maria! 💕

Seu agendamento foi confirmado:

📅 *Data:* 15/12/2024 às 14:00
👩💼 *Profissional:* Ana Silva
💅 *Procedimento:* Volume Brasileiro
💰 *Valor:* R$ 80,00

📍 *Endereço:* [Seu endereço aqui]

⚠️ *Importante:*
• Chegue 10 minutos antes
• Evite usar máscara de cílios no dia
• Em caso de cancelamento, avise com 24h de antecedência

Estamos ansiosas para te atender! 🌸

_LashManager - Beleza que encanta_ ✨`,

    lembrete: `🔔 *Lembrete de Agendamento* 🔔

Oi Maria! 💕

Lembrando que você tem agendamento amanhã:

📅 *Data:* 15/12/2024 às 14:00
💅 *Procedimento:* Volume Brasileiro

Nos vemos em breve! 🌸

_LashManager - Beleza que encanta_ ✨`,

    agradecimento: `💕 *Obrigada pela confiança!* 💕

Oi Maria! ✨

Esperamos que tenha amado seu novo olhar! 😍

📸 *Que tal uma foto?*
Marque a gente nas suas redes sociais!

⭐ *Avaliação:*
Sua opinião é muito importante para nós!

🗓️ *Próximo agendamento:*
Lembre-se: manutenção em 15-20 dias

Até breve! 🌸

_LashManager - Beleza que encanta_ ✨`
  }
  
  previewText.value = previews[tipo] || ''
  previewDialog.value = true
}
</script>

<style scoped>
.whatsapp-preview {
  background: #e8f5e8;
  border-radius: 12px;
  padding: 16px;
  border-left: 4px solid #25d366;
}

.whatsapp-preview pre {
  white-space: pre-wrap;
  font-family: 'Poppins', sans-serif;
  margin: 0;
}
</style>
import requests
from datetime import datetime, timedelta
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente

class WhatsAppService:
    def __init__(self):
        self.api_url = "https://api.whatsapp.com/send"
    
    def format_phone(self, phone):
        """Formatar telefone para WhatsApp"""
        phone = ''.join(filter(str.isdigit, phone))
        if phone.startswith('0'):
            phone = phone[1:]
        if not phone.startswith('55'):
            phone = '55' + phone
        return phone
    
    def send_confirmation_message(self, agendamento):
        """Enviar mensagem de confirmação de agendamento"""
        cliente = agendamento.cliente
        funcionario = agendamento.funcionario
        procedimento = agendamento.procedimento
        
        data_formatada = agendamento.data_hora.strftime('%d/%m/%Y às %H:%M')
        
        message = f"""✨ *Agendamento Confirmado* ✨

Olá {cliente.nome}! 💕

Seu agendamento foi confirmado:

📅 *Data:* {data_formatada}
👩‍💼 *Profissional:* {funcionario.nome}
💅 *Procedimento:* {procedimento.nome}
💰 *Valor:* R$ {procedimento.preco:.2f}

📍 *Endereço:* [Seu endereço aqui]

⚠️ *Importante:*
• Chegue 10 minutos antes
• Evite usar máscara de cílios no dia
• Em caso de cancelamento, avise com 24h de antecedência

Estamos ansiosas para te atender! 🌸

_LashManager - Beleza que encanta_ ✨"""
        
        phone = self.format_phone(cliente.telefone)
        whatsapp_url = f"{self.api_url}?phone={phone}&text={requests.utils.quote(message)}"
        
        return whatsapp_url
    
    def send_reminder_message(self, agendamento):
        """Enviar lembrete 24h antes"""
        cliente = agendamento.cliente
        data_formatada = agendamento.data_hora.strftime('%d/%m/%Y às %H:%M')
        
        message = f"""🔔 *Lembrete de Agendamento* 🔔

Oi {cliente.nome}! 💕

Lembrando que você tem agendamento amanhã:

📅 *Data:* {data_formatada}
💅 *Procedimento:* {agendamento.procedimento.nome}

Nos vemos em breve! 🌸

_LashManager - Beleza que encanta_ ✨"""
        
        phone = self.format_phone(cliente.telefone)
        whatsapp_url = f"{self.api_url}?phone={phone}&text={requests.utils.quote(message)}"
        
        return whatsapp_url
    
    def send_thank_you_message(self, agendamento):
        """Enviar agradecimento após procedimento"""
        cliente = agendamento.cliente
        
        message = f"""💕 *Obrigada pela confiança!* 💕

Oi {cliente.nome}! ✨

Esperamos que tenha amado seu novo olhar! 😍

📸 *Que tal uma foto?*
Marque a gente nas suas redes sociais!

⭐ *Avaliação:*
Sua opinião é muito importante para nós!

🗓️ *Próximo agendamento:*
Lembre-se: manutenção em 15-20 dias

Até breve! 🌸

_LashManager - Beleza que encanta_ ✨"""
        
        phone = self.format_phone(cliente.telefone)
        whatsapp_url = f"{self.api_url}?phone={phone}&text={requests.utils.quote(message)}"
        
        return whatsapp_url
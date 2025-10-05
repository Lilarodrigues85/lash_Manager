from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.agendamento import Agendamento
from app.services.whatsapp_service import WhatsAppService

mensagens_bp = Blueprint('mensagens', __name__)

@mensagens_bp.route('/confirmacao/<int:agendamento_id>', methods=['GET'])
@jwt_required()
def get_confirmacao_url(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    whatsapp = WhatsAppService()
    url = whatsapp.send_confirmation_message(agendamento)
    return jsonify({'whatsapp_url': url})

@mensagens_bp.route('/lembrete/<int:agendamento_id>', methods=['GET'])
@jwt_required()
def get_lembrete_url(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    whatsapp = WhatsAppService()
    url = whatsapp.send_reminder_message(agendamento)
    return jsonify({'whatsapp_url': url})

@mensagens_bp.route('/agradecimento/<int:agendamento_id>', methods=['GET'])
@jwt_required()
def get_agradecimento_url(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    whatsapp = WhatsAppService()
    url = whatsapp.send_thank_you_message(agendamento)
    return jsonify({'whatsapp_url': url})

@mensagens_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_templates():
    templates = {
        'confirmacao': '✨ Agendamento confirmado com data, horário e procedimento',
        'lembrete': '🔔 Lembrete 24h antes do agendamento',
        'agradecimento': '💕 Agradecimento após o procedimento realizado'
    }
    return jsonify(templates)
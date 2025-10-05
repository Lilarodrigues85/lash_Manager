from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.agendamento import Agendamento
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

agendamentos_bp = Blueprint('agendamentos', __name__)

@agendamentos_bp.route('/', methods=['GET'])
@jwt_required()
def get_agendamentos():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    funcionario_id = request.args.get('funcionario_id', type=int)
    status = request.args.get('status')
    
    query = Agendamento.query
    
    if data_inicio:
        query = query.filter(Agendamento.data_hora >= datetime.fromisoformat(data_inicio))
    if data_fim:
        query = query.filter(Agendamento.data_hora <= datetime.fromisoformat(data_fim))
    if funcionario_id:
        query = query.filter_by(funcionario_id=funcionario_id)
    if status:
        query = query.filter_by(status=status)
    
    agendamentos = query.order_by(Agendamento.data_hora).all()
    return jsonify([a.to_dict() for a in agendamentos])

@agendamentos_bp.route('/', methods=['POST'])
@jwt_required()
def create_agendamento():
    data = request.get_json()
    
    # Verificar conflitos de horário
    data_hora = datetime.fromisoformat(data.get('data_hora'))
    funcionario_id = data.get('funcionario_id')
    
    conflito = Agendamento.query.filter(
        and_(
            Agendamento.funcionario_id == funcionario_id,
            Agendamento.data_hora == data_hora,
            Agendamento.status != 'cancelado'
        )
    ).first()
    
    if conflito:
        return jsonify({'error': 'Horário já ocupado'}), 400
    
    agendamento = Agendamento(
        cliente_id=data.get('cliente_id'),
        funcionario_id=funcionario_id,
        procedimento_id=data.get('procedimento_id'),
        data_hora=data_hora,
        observacoes=data.get('observacoes')
    )
    
    db.session.add(agendamento)
    db.session.commit()
    
    # Enviar mensagem de confirmação
    from app.services.whatsapp_service import WhatsAppService
    whatsapp = WhatsAppService()
    whatsapp_url = whatsapp.send_confirmation_message(agendamento)
    
    response = agendamento.to_dict()
    response['whatsapp_url'] = whatsapp_url
    
    return jsonify(response), 201

@agendamentos_bp.route('/<int:agendamento_id>', methods=['PUT'])
@jwt_required()
def update_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    data = request.get_json()
    
    if 'data_hora' in data:
        nova_data_hora = datetime.fromisoformat(data.get('data_hora'))
        funcionario_id = data.get('funcionario_id', agendamento.funcionario_id)
        
        # Verificar conflitos (exceto o próprio agendamento)
        conflito = Agendamento.query.filter(
            and_(
                Agendamento.funcionario_id == funcionario_id,
                Agendamento.data_hora == nova_data_hora,
                Agendamento.status != 'cancelado',
                Agendamento.id != agendamento_id
            )
        ).first()
        
        if conflito:
            return jsonify({'error': 'Horário já ocupado'}), 400
        
        agendamento.data_hora = nova_data_hora
    
    agendamento.cliente_id = data.get('cliente_id', agendamento.cliente_id)
    agendamento.funcionario_id = data.get('funcionario_id', agendamento.funcionario_id)
    agendamento.procedimento_id = data.get('procedimento_id', agendamento.procedimento_id)
    agendamento.status = data.get('status', agendamento.status)
    agendamento.observacoes = data.get('observacoes', agendamento.observacoes)
    
    db.session.commit()
    return jsonify(agendamento.to_dict())

@agendamentos_bp.route('/<int:agendamento_id>', methods=['DELETE'])
@jwt_required()
def delete_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    agendamento.status = 'cancelado'
    db.session.commit()
    return jsonify({'message': 'Agendamento cancelado com sucesso'})

@agendamentos_bp.route('/horarios-disponiveis', methods=['GET'])
@jwt_required()
def get_horarios_disponiveis():
    data = request.args.get('data')  # YYYY-MM-DD
    funcionario_id = request.args.get('funcionario_id', type=int)
    
    if not data or not funcionario_id:
        return jsonify({'error': 'Data e funcionário são obrigatórios'}), 400
    
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    
    # Horários de funcionamento (9h às 18h)
    horarios_trabalho = []
    for hora in range(9, 18):
        for minuto in [0, 30]:  # Intervalos de 30 minutos
            horarios_trabalho.append(f"{hora:02d}:{minuto:02d}")
    
    # Buscar agendamentos do dia
    inicio_dia = datetime.combine(data_obj, datetime.min.time())
    fim_dia = datetime.combine(data_obj, datetime.max.time())
    
    agendamentos = Agendamento.query.filter(
        and_(
            Agendamento.funcionario_id == funcionario_id,
            Agendamento.data_hora >= inicio_dia,
            Agendamento.data_hora <= fim_dia,
            Agendamento.status != 'cancelado'
        )
    ).all()
    
    horarios_ocupados = [a.data_hora.strftime('%H:%M') for a in agendamentos]
    horarios_disponiveis = [h for h in horarios_trabalho if h not in horarios_ocupados]
    
    return jsonify(horarios_disponiveis)
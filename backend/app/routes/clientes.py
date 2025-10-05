from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.cliente import Cliente
from app.models.agendamento import Agendamento
from app.models.pagamento import Pagamento
from sqlalchemy import desc

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
@jwt_required()
def get_clientes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = Cliente.query
    if search:
        query = query.filter(Cliente.nome.contains(search))
    
    clientes = query.order_by(desc(Cliente.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'clientes': [cliente.to_dict() for cliente in clientes.items],
        'total': clientes.total,
        'pages': clientes.pages,
        'current_page': page
    })

@clientes_bp.route('/', methods=['POST'])
@jwt_required()
def create_cliente():
    data = request.get_json()
    
    cliente = Cliente(
        nome=data.get('nome'),
        telefone=data.get('telefone'),
        email=data.get('email'),
        observacoes=data.get('observacoes')
    )
    
    db.session.add(cliente)
    db.session.commit()
    
    return jsonify(cliente.to_dict()), 201

@clientes_bp.route('/<int:cliente_id>', methods=['GET'])
@jwt_required()
def get_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    # Buscar histórico de agendamentos
    agendamentos = Agendamento.query.filter_by(cliente_id=cliente_id).order_by(desc(Agendamento.data_hora)).all()
    
    # Buscar histórico de pagamentos
    pagamentos = Pagamento.query.filter_by(cliente_id=cliente_id).order_by(desc(Pagamento.data_pagamento)).all()
    
    # Calcular totais
    total_pago = sum(p.valor for p in pagamentos if p.status == 'pago')
    total_pendente = sum(a.procedimento.preco for a in agendamentos if a.status == 'realizado') - total_pago
    
    return jsonify({
        'cliente': cliente.to_dict(),
        'agendamentos': [a.to_dict() for a in agendamentos],
        'pagamentos': [p.to_dict() for p in pagamentos],
        'total_pago': float(total_pago),
        'total_pendente': float(total_pendente)
    })

@clientes_bp.route('/<int:cliente_id>', methods=['PUT'])
@jwt_required()
def update_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.get_json()
    
    cliente.nome = data.get('nome', cliente.nome)
    cliente.telefone = data.get('telefone', cliente.telefone)
    cliente.email = data.get('email', cliente.email)
    cliente.observacoes = data.get('observacoes', cliente.observacoes)
    
    db.session.commit()
    return jsonify(cliente.to_dict())

@clientes_bp.route('/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente deletado com sucesso'})
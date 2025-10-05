from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.pagamento import Pagamento
from datetime import datetime
from sqlalchemy import desc, func

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/', methods=['GET'])
@jwt_required()
def get_pagamentos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    cliente_id = request.args.get('cliente_id', type=int)
    status = request.args.get('status')
    
    query = Pagamento.query
    
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    if status:
        query = query.filter_by(status=status)
    
    pagamentos = query.order_by(desc(Pagamento.data_pagamento)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'pagamentos': [p.to_dict() for p in pagamentos.items],
        'total': pagamentos.total,
        'pages': pagamentos.pages,
        'current_page': page
    })

@pagamentos_bp.route('/', methods=['POST'])
@jwt_required()
def create_pagamento():
    data = request.get_json()
    
    # Calcular valor do funcionário se fornecido
    valor_funcionario = 0
    if data.get('funcionario_id'):
        from app.models.funcionario import Funcionario
        funcionario = Funcionario.query.get(data.get('funcionario_id'))
        if funcionario:
            valor_total = float(data.get('valor', 0))
            valor_funcionario = (valor_total * float(funcionario.porcentagem)) / 100
    
    pagamento = Pagamento(
        cliente_id=data.get('cliente_id'),
        agendamento_id=data.get('agendamento_id'),
        funcionario_id=data.get('funcionario_id'),
        valor=data.get('valor'),
        valor_funcionario=valor_funcionario,
        forma_pagamento=data.get('forma_pagamento'),
        data_pagamento=datetime.fromisoformat(data.get('data_pagamento')) if data.get('data_pagamento') else datetime.utcnow(),
        status=data.get('status', 'pago'),
        observacoes=data.get('observacoes')
    )
    
    db.session.add(pagamento)
    db.session.commit()
    
    return jsonify(pagamento.to_dict()), 201

@pagamentos_bp.route('/<int:pagamento_id>', methods=['PUT'])
@jwt_required()
def update_pagamento(pagamento_id):
    pagamento = Pagamento.query.get_or_404(pagamento_id)
    data = request.get_json()
    
    pagamento.valor = data.get('valor', pagamento.valor)
    pagamento.forma_pagamento = data.get('forma_pagamento', pagamento.forma_pagamento)
    pagamento.status = data.get('status', pagamento.status)
    pagamento.observacoes = data.get('observacoes', pagamento.observacoes)
    
    if data.get('data_pagamento'):
        pagamento.data_pagamento = datetime.fromisoformat(data.get('data_pagamento'))
    
    db.session.commit()
    return jsonify(pagamento.to_dict())

@pagamentos_bp.route('/<int:pagamento_id>', methods=['DELETE'])
@jwt_required()
def delete_pagamento(pagamento_id):
    pagamento = Pagamento.query.get_or_404(pagamento_id)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'message': 'Pagamento deletado com sucesso'})

@pagamentos_bp.route('/pendentes', methods=['GET'])
@jwt_required()
def get_pagamentos_pendentes():
    # Buscar agendamentos realizados sem pagamento completo
    from app.models.agendamento import Agendamento
    from sqlalchemy import and_
    
    agendamentos_realizados = db.session.query(
        Agendamento.id,
        Agendamento.cliente_id,
        Agendamento.data_hora,
        Agendamento.procedimento_id,
        func.coalesce(func.sum(Pagamento.valor), 0).label('valor_pago')
    ).outerjoin(Pagamento, Agendamento.id == Pagamento.agendamento_id)\
     .filter(Agendamento.status == 'realizado')\
     .group_by(Agendamento.id, Agendamento.cliente_id, Agendamento.data_hora, Agendamento.procedimento_id)\
     .all()
    
    pendentes = []
    for ag in agendamentos_realizados:
        agendamento = Agendamento.query.get(ag.id)
        valor_devido = float(agendamento.procedimento.preco)
        valor_pago = float(ag.valor_pago)
        
        if valor_pago < valor_devido:
            pendentes.append({
                'agendamento': agendamento.to_dict(),
                'valor_devido': valor_devido,
                'valor_pago': valor_pago,
                'valor_pendente': valor_devido - valor_pago
            })
    
    return jsonify(pendentes)
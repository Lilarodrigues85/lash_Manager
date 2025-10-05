from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.agendamento import Agendamento
from app.models.pagamento import Pagamento
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from datetime import datetime, timedelta
from sqlalchemy import func, and_, desc

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/resumo', methods=['GET'])
@jwt_required()
def get_resumo():
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    
    # Agendamentos de hoje
    agendamentos_hoje = Agendamento.query.filter(
        and_(
            func.date(Agendamento.data_hora) == hoje,
            Agendamento.status != 'cancelado'
        )
    ).count()
    
    # Receita do mês
    receita_mes = db.session.query(func.sum(Pagamento.valor)).filter(
        and_(
            func.date(Pagamento.data_pagamento) >= inicio_mes,
            Pagamento.status == 'pago'
        )
    ).scalar() or 0
    
    # Total de clientes
    total_clientes = Cliente.query.count()
    
    # Agendamentos pendentes
    agendamentos_pendentes = Agendamento.query.filter(
        and_(
            Agendamento.data_hora >= datetime.now(),
            Agendamento.status == 'agendado'
        )
    ).count()
    
    return jsonify({
        'agendamentos_hoje': agendamentos_hoje,
        'receita_mes': float(receita_mes),
        'total_clientes': total_clientes,
        'agendamentos_pendentes': agendamentos_pendentes
    })

@dashboard_bp.route('/agenda-hoje', methods=['GET'])
@jwt_required()
def get_agenda_hoje():
    hoje = datetime.now().date()
    
    agendamentos = Agendamento.query.filter(
        and_(
            func.date(Agendamento.data_hora) == hoje,
            Agendamento.status != 'cancelado'
        )
    ).order_by(Agendamento.data_hora).all()
    
    return jsonify([a.to_dict() for a in agendamentos])

@dashboard_bp.route('/receitas-mensais', methods=['GET'])
@jwt_required()
def get_receitas_mensais():
    # Últimos 6 meses
    meses = []
    for i in range(6):
        data = datetime.now().replace(day=1) - timedelta(days=30*i)
        inicio_mes = data.replace(day=1)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        receita = db.session.query(func.sum(Pagamento.valor)).filter(
            and_(
                Pagamento.data_pagamento >= inicio_mes,
                Pagamento.data_pagamento <= fim_mes,
                Pagamento.status == 'pago'
            )
        ).scalar() or 0
        
        meses.append({
            'mes': inicio_mes.strftime('%Y-%m'),
            'receita': float(receita)
        })
    
    return jsonify(list(reversed(meses)))

@dashboard_bp.route('/procedimentos-populares', methods=['GET'])
@jwt_required()
def get_procedimentos_populares():
    from app.models.procedimento import Procedimento
    
    resultado = db.session.query(
        Procedimento.nome,
        func.count(Agendamento.id).label('total')
    ).join(Agendamento)\
     .filter(Agendamento.status == 'realizado')\
     .group_by(Procedimento.nome)\
     .order_by(desc('total'))\
     .limit(5).all()
    
    return jsonify([{
        'nome': r.nome,
        'total': r.total
    } for r in resultado])

@dashboard_bp.route('/performance-funcionarios', methods=['GET'])
@jwt_required()
def get_performance_funcionarios():
    inicio_mes = datetime.now().replace(day=1)
    
    resultado = db.session.query(
        Funcionario.nome,
        func.count(Agendamento.id).label('agendamentos'),
        func.sum(Pagamento.valor).label('receita')
    ).join(Agendamento)\
     .outerjoin(Pagamento, Agendamento.id == Pagamento.agendamento_id)\
     .filter(
         and_(
             Agendamento.data_hora >= inicio_mes,
             Agendamento.status == 'realizado',
             Pagamento.status == 'pago'
         )
     )\
     .group_by(Funcionario.nome)\
     .all()
    
    return jsonify([{
        'funcionario': r.nome,
        'agendamentos': r.agendamentos,
        'receita': float(r.receita or 0)
    } for r in resultado])

@dashboard_bp.route('/clientes-recentes', methods=['GET'])
@jwt_required()
def get_clientes_recentes():
    clientes = Cliente.query.order_by(desc(Cliente.created_at)).limit(5).all()
    return jsonify([c.to_dict() for c in clientes])
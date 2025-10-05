from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.agendamento import Agendamento
from app.models.funcionario import Funcionario
from app.models.pagamento import Pagamento
from datetime import datetime
from sqlalchemy import func, and_

comissoes_bp = Blueprint('comissoes', __name__)

@comissoes_bp.route('/calcular/<int:agendamento_id>', methods=['GET'])
@jwt_required()
def calcular_comissao(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    funcionario = agendamento.funcionario
    procedimento = agendamento.procedimento
    
    valor_total = float(procedimento.preco)
    porcentagem_funcionario = float(funcionario.porcentagem)
    comissao = (valor_total * porcentagem_funcionario) / 100
    
    return jsonify({
        'agendamento_id': agendamento_id,
        'funcionario': funcionario.nome,
        'procedimento': procedimento.nome,
        'valor_total': valor_total,
        'porcentagem': porcentagem_funcionario,
        'comissao': round(comissao, 2)
    })

@comissoes_bp.route('/funcionario/<int:funcionario_id>', methods=['GET'])
@jwt_required()
def get_comissoes_funcionario(funcionario_id):
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    
    query = db.session.query(
        Agendamento,
        func.sum(Pagamento.valor).label('valor_pago')
    ).join(Pagamento, Agendamento.id == Pagamento.agendamento_id)\
     .filter(
         and_(
             Agendamento.funcionario_id == funcionario_id,
             Agendamento.status == 'realizado',
             Pagamento.status == 'pago'
         )
     )
    
    if data_inicio:
        query = query.filter(Agendamento.data_hora >= datetime.fromisoformat(data_inicio))
    if data_fim:
        query = query.filter(Agendamento.data_hora <= datetime.fromisoformat(data_fim))
    
    resultados = query.group_by(Agendamento.id).all()
    
    comissoes = []
    total_comissao = 0
    
    for agendamento, valor_pago in resultados:
        comissao = (float(valor_pago) * float(funcionario.porcentagem)) / 100
        total_comissao += comissao
        
        comissoes.append({
            'agendamento': agendamento.to_dict(),
            'valor_pago': float(valor_pago),
            'comissao': round(comissao, 2)
        })
    
    return jsonify({
        'funcionario': funcionario.to_dict(),
        'comissoes': comissoes,
        'total_comissao': round(total_comissao, 2)
    })
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.procedimento import Procedimento

procedimentos_bp = Blueprint('procedimentos', __name__)

@procedimentos_bp.route('/', methods=['GET'])
@jwt_required()
def get_procedimentos():
    funcionario_id = request.args.get('funcionario_id', type=int)
    
    query = Procedimento.query.filter_by(ativo=True)
    if funcionario_id:
        query = query.filter_by(funcionario_id=funcionario_id)
    
    procedimentos = query.all()
    return jsonify([p.to_dict() for p in procedimentos])

@procedimentos_bp.route('/', methods=['POST'])
@jwt_required()
def create_procedimento():
    data = request.get_json()
    
    procedimento = Procedimento(
        nome=data.get('nome'),
        preco=data.get('preco'),
        duracao_minutos=data.get('duracao_minutos'),
        descricao=data.get('descricao'),
        funcionario_id=data.get('funcionario_id')
    )
    
    db.session.add(procedimento)
    db.session.commit()
    
    return jsonify(procedimento.to_dict()), 201

@procedimentos_bp.route('/<int:procedimento_id>', methods=['PUT'])
@jwt_required()
def update_procedimento(procedimento_id):
    procedimento = Procedimento.query.get_or_404(procedimento_id)
    data = request.get_json()
    
    procedimento.nome = data.get('nome', procedimento.nome)
    procedimento.preco = data.get('preco', procedimento.preco)
    procedimento.duracao_minutos = data.get('duracao_minutos', procedimento.duracao_minutos)
    procedimento.descricao = data.get('descricao', procedimento.descricao)
    procedimento.funcionario_id = data.get('funcionario_id', procedimento.funcionario_id)
    procedimento.ativo = data.get('ativo', procedimento.ativo)
    
    db.session.commit()
    return jsonify(procedimento.to_dict())

@procedimentos_bp.route('/<int:procedimento_id>', methods=['DELETE'])
@jwt_required()
def delete_procedimento(procedimento_id):
    procedimento = Procedimento.query.get_or_404(procedimento_id)
    procedimento.ativo = False
    db.session.commit()
    return jsonify({'message': 'Procedimento desativado com sucesso'})
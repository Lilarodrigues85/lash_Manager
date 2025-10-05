from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.funcionario import Funcionario

funcionarios_bp = Blueprint('funcionarios', __name__)

@funcionarios_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Funcionarios API is working'}), 200

@funcionarios_bp.route('/', methods=['GET'])
@jwt_required()
def get_funcionarios():
    try:
        funcionarios = Funcionario.query.filter_by(ativo=True).all()
        return jsonify([f.to_dict() for f in funcionarios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcionarios_bp.route('/', methods=['POST'])
@jwt_required()
def create_funcionario():
    try:
        data = request.get_json()
        
        if not data.get('nome') or not data.get('especialidade'):
            return jsonify({'error': 'Nome e especialidade são obrigatórios'}), 400
        
        funcionario = Funcionario(
            nome=data.get('nome'),
            especialidade=data.get('especialidade'),
            telefone=data.get('telefone'),
            porcentagem=float(data.get('porcentagem', 25.00))
        )
        
        db.session.add(funcionario)
        db.session.commit()
        
        return jsonify(funcionario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcionarios_bp.route('/<int:funcionario_id>', methods=['PUT'])
@jwt_required()
def update_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    data = request.get_json()
    
    funcionario.nome = data.get('nome', funcionario.nome)
    funcionario.especialidade = data.get('especialidade', funcionario.especialidade)
    funcionario.telefone = data.get('telefone', funcionario.telefone)
    funcionario.porcentagem = data.get('porcentagem', funcionario.porcentagem)
    funcionario.ativo = data.get('ativo', funcionario.ativo)
    
    db.session.commit()
    return jsonify(funcionario.to_dict())

@funcionarios_bp.route('/<int:funcionario_id>', methods=['DELETE'])
@jwt_required()
def delete_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    funcionario.ativo = False
    db.session.commit()
    return jsonify({'message': 'Funcionário desativado com sucesso'})
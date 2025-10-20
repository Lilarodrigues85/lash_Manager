from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('', methods=['GET'])
@jwt_required()
def listar_usuarios():
    user_id = int(get_jwt_identity())
    usuario_atual = Usuario.query.get(user_id)
    
    if usuario_atual.tipo_usuario != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403
    
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])

@usuarios_bp.route('', methods=['POST'])
@jwt_required()
def criar_usuario():
    user_id = int(get_jwt_identity())
    usuario_atual = Usuario.query.get(user_id)
    
    if usuario_atual.tipo_usuario != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    if Usuario.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username já existe'}), 400
    
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email já existe'}), 400
    
    usuario = Usuario(
        username=data.get('username'),
        email=data.get('email'),
        nome=data.get('nome'),
        tipo_usuario=data.get('tipo_usuario', 'funcionario')
    )
    usuario.set_password(data.get('password'))
    
    db.session.add(usuario)
    db.session.commit()
    
    return jsonify(usuario.to_dict()), 201

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    user_id = int(get_jwt_identity())
    usuario_atual = Usuario.query.get(user_id)
    
    if usuario_atual.tipo_usuario != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403
    
    usuario = Usuario.query.get_or_404(id)
    data = request.get_json()
    
    if 'nome' in data:
        usuario.nome = data['nome']
    if 'email' in data:
        usuario.email = data['email']
    if 'tipo_usuario' in data:
        usuario.tipo_usuario = data['tipo_usuario']
    if 'ativo' in data:
        usuario.ativo = data['ativo']
    if 'password' in data:
        usuario.set_password(data['password'])
    
    db.session.commit()
    return jsonify(usuario.to_dict())

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(id):
    user_id = int(get_jwt_identity())
    usuario_atual = Usuario.query.get(user_id)
    
    if usuario_atual.tipo_usuario != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403
    
    usuario = Usuario.query.get_or_404(id)
    usuario.ativo = False
    db.session.commit()
    
    return jsonify({'message': 'Usuário desativado com sucesso'})

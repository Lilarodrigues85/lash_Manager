from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    usuario = Usuario.query.filter_by(username=username).first()
    
    if usuario and usuario.check_password(password) and usuario.ativo:
        access_token = create_access_token(identity=usuario.id)
        return jsonify({
            'access_token': access_token,
            'usuario': usuario.to_dict()
        })
    
    return jsonify({'error': 'Credenciais inválidas'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if Usuario.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username já existe'}), 400
    
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email já existe'}), 400
    
    usuario = Usuario(
        username=data.get('username'),
        email=data.get('email'),
        nome=data.get('nome')
    )
    usuario.set_password(data.get('password'))
    
    db.session.add(usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(user_id)
    return jsonify(usuario.to_dict())
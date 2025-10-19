from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.cliente import Cliente
from app.models.agendamento import Agendamento
from app.models.pagamento import Pagamento
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
@jwt_required()
def get_clientes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        query = Cliente.query.filter(Cliente.ativo == True)
        
        if search:
            query = Cliente.search(search)
        
        clientes = query.order_by(desc(Cliente.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'clientes': [cliente.to_dict() for cliente in clientes.items],
            'total': clientes.total,
            'pages': clientes.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/', methods=['POST'])
@jwt_required()
def create_cliente():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Dados não fornecidos'}), 400
        
        # Validar campos obrigatórios
        required_fields = ['nome', 'telefone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False, 
                    'error': f'Campo {field} é obrigatório'
                }), 400
        
        cliente = Cliente(
            nome=data.get('nome'),
            telefone=data.get('telefone'),
            email=data.get('email') if data.get('email') else None,
            observacoes=data.get('observacoes')
        )
        
        cliente.validate_data()
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente cadastrado com sucesso',
            'cliente': cliente.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'error': 'Email já cadastrado no sistema'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>', methods=['GET'])
@jwt_required()
def get_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        agendamentos = Agendamento.query.filter_by(cliente_id=cliente_id).order_by(desc(Agendamento.data_hora)).all()
        pagamentos = Pagamento.query.filter_by(cliente_id=cliente_id).order_by(desc(Pagamento.data_pagamento)).all()
        
        total_pago = sum(p.valor for p in pagamentos if p.status == 'pago')
        total_pendente = sum(a.procedimento.preco for a in agendamentos if hasattr(a, 'procedimento') and a.status == 'realizado') - total_pago
        
        return jsonify({
            'success': True,
            'cliente': cliente.to_dict(),
            'agendamentos': [a.to_dict() for a in agendamentos],
            'pagamentos': [p.to_dict() for p in pagamentos],
            'total_pago': float(total_pago),
            'total_pendente': float(max(0, total_pendente)),
            'total_agendamentos': len(agendamentos),
            'ultimo_agendamento': agendamentos[0].data_hora.isoformat() if agendamentos else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>', methods=['PUT'])
@jwt_required()
def update_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Dados não fornecidos'}), 400
        
        # Atualizar campos
        if 'nome' in data:
            cliente.nome = data['nome']
        if 'telefone' in data:
            cliente.telefone = data['telefone']
        if 'email' in data:
            cliente.email = data['email'] if data['email'] else None
        if 'observacoes' in data:
            cliente.observacoes = data['observacoes']
        
        cliente.validate_data()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente atualizado com sucesso',
            'cliente': cliente.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'error': 'Email já cadastrado no sistema'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        cliente.ativo = False
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Cliente desativado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
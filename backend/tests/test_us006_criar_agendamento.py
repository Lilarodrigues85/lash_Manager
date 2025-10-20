"""Teste Unitário - US006: Criar Agendamento"""
import pytest
from app import create_app, db
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.procedimento import Procedimento
from datetime import datetime, timedelta

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_criar_agendamento_valido(app):
    """Testa criação de agendamento válido"""
    with app.app_context():
        # Criar dados necessários
        cliente = Cliente(nome='Cliente Teste', telefone='11999999999')
        db.session.add(cliente)
        
        funcionario = Funcionario(nome='Funcionario Teste', especialidade='Lash Designer', telefone='11888888888')
        db.session.add(funcionario)
        db.session.flush()
        
        procedimento = Procedimento(nome='Volume Russo', preco=150.0, duracao_minutos=120, funcionario_id=funcionario.id)
        db.session.add(procedimento)
        
        db.session.commit()
        
        # Criar agendamento
        data_hora = datetime.now() + timedelta(days=1)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario.id,
            procedimento_id=procedimento.id,
            data_hora=data_hora
        )
        
        agendamento.validate_data()
        db.session.add(agendamento)
        db.session.commit()
        
        assert agendamento.id is not None
        assert agendamento.status == 'agendado'

def test_validacao_cliente_obrigatorio(app):
    """Testa validação de cliente obrigatório"""
    with app.app_context():
        agendamento = Agendamento(
            funcionario_id=1,
            procedimento_id=1,
            data_hora=datetime.now() + timedelta(days=1)
        )
        
        with pytest.raises(ValueError, match="Cliente é obrigatório"):
            agendamento.validate_data()

def test_validacao_funcionario_obrigatorio(app):
    """Testa validação de funcionário obrigatório"""
    with app.app_context():
        agendamento = Agendamento(
            cliente_id=1,
            procedimento_id=1,
            data_hora=datetime.now() + timedelta(days=1)
        )
        
        with pytest.raises(ValueError, match="Funcionário é obrigatório"):
            agendamento.validate_data()

def test_validacao_procedimento_obrigatorio(app):
    """Testa validação de procedimento obrigatório"""
    with app.app_context():
        agendamento = Agendamento(
            cliente_id=1,
            funcionario_id=1,
            data_hora=datetime.now() + timedelta(days=1)
        )
        
        with pytest.raises(ValueError, match="Procedimento é obrigatório"):
            agendamento.validate_data()

def test_validacao_data_hora_obrigatoria(app):
    """Testa validação de data/hora obrigatória"""
    with app.app_context():
        agendamento = Agendamento(
            cliente_id=1,
            funcionario_id=1,
            procedimento_id=1
        )
        
        with pytest.raises(ValueError, match="Data e hora são obrigatórios"):
            agendamento.validate_data()

def test_validacao_data_passado(app):
    """Testa que não permite agendar no passado"""
    with app.app_context():
        agendamento = Agendamento(
            cliente_id=1,
            funcionario_id=1,
            procedimento_id=1,
            data_hora=datetime.now() - timedelta(days=1)
        )
        
        with pytest.raises(ValueError, match="Data e hora não podem ser no passado"):
            agendamento.validate_data()

def test_status_default_agendado(app):
    """Testa que status padrão é 'agendado'"""
    with app.app_context():
        agendamento = Agendamento(
            cliente_id=1,
            funcionario_id=1,
            procedimento_id=1,
            data_hora=datetime.now() + timedelta(days=1)
        )
        
        assert agendamento.status == 'agendado'

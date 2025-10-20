"""Teste Unitário - US007: Visualizar Agenda do Funcionário"""
import pytest
from app import create_app, db
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.procedimento import Procedimento
from app.models.usuario import Usuario
from datetime import datetime, timedelta, date

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

@pytest.fixture
def funcionario_logado(app):
    """Cria funcionário com usuário e retorna token"""
    with app.app_context():
        # Criar funcionário
        funcionario = Funcionario(
            nome='Funcionario Teste',
            especialidade='Lash Designer',
            telefone='11999999999'
        )
        db.session.add(funcionario)
        db.session.flush()
        
        # Criar usuário
        usuario = Usuario(
            username='funcionario',
            email='func@test.com',
            nome='Funcionario Teste',
            tipo_usuario='funcionario'
        )
        usuario.set_password('senha123')
        db.session.add(usuario)
        db.session.flush()
        
        # Associar funcionário ao usuário
        funcionario.usuario_id = usuario.id
        db.session.commit()
        
        return funcionario.id

def test_visualizar_agenda_dia_atual(client, funcionario_logado, app):
    """Testa visualização da agenda do dia atual"""
    with app.app_context():
        # Login
        response = client.post('/api/auth/login', json={
            'username': 'funcionario',
            'password': 'senha123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Criar cliente e procedimento
        cliente = Cliente(nome='Cliente Teste', telefone='11888888888')
        db.session.add(cliente)
        db.session.flush()
        
        procedimento = Procedimento(
            nome='Volume Russo',
            preco=150.0,
            duracao_minutos=120,
            funcionario_id=funcionario_logado
        )
        db.session.add(procedimento)
        db.session.flush()
        
        # Criar agendamento para hoje
        hoje = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario_logado,
            procedimento_id=procedimento.id,
            data_hora=hoje
        )
        db.session.add(agendamento)
        db.session.commit()
        
        # Buscar agenda
        response = client.get('/api/agendamentos/minha-agenda', headers=headers)
        
        assert response.status_code == 200
        assert response.json['total'] == 1
        assert len(response.json['agendamentos']) == 1

def test_visualizar_agenda_data_especifica(client, funcionario_logado, app):
    """Testa visualização da agenda de data específica"""
    with app.app_context():
        # Login
        response = client.post('/api/auth/login', json={
            'username': 'funcionario',
            'password': 'senha123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Criar cliente e procedimento
        cliente = Cliente(nome='Cliente Teste', telefone='11888888888')
        db.session.add(cliente)
        db.session.flush()
        
        procedimento = Procedimento(
            nome='Volume Russo',
            preco=150.0,
            duracao_minutos=120,
            funcionario_id=funcionario_logado
        )
        db.session.add(procedimento)
        db.session.flush()
        
        # Criar agendamento para amanhã
        amanha = datetime.now() + timedelta(days=1)
        amanha = amanha.replace(hour=10, minute=0, second=0, microsecond=0)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario_logado,
            procedimento_id=procedimento.id,
            data_hora=amanha
        )
        db.session.add(agendamento)
        db.session.commit()
        
        # Buscar agenda de amanhã
        data_amanha = amanha.strftime('%Y-%m-%d')
        response = client.get(
            f'/api/agendamentos/minha-agenda?data={data_amanha}',
            headers=headers
        )
        
        assert response.status_code == 200
        assert response.json['total'] == 1
        assert response.json['data'] == data_amanha

def test_agenda_vazia(client, funcionario_logado, app):
    """Testa agenda sem agendamentos"""
    with app.app_context():
        # Login
        response = client.post('/api/auth/login', json={
            'username': 'funcionario',
            'password': 'senha123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Buscar agenda
        response = client.get('/api/agendamentos/minha-agenda', headers=headers)
        
        assert response.status_code == 200
        assert response.json['total'] == 0
        assert len(response.json['agendamentos']) == 0

def test_agenda_ordenada_por_horario(client, funcionario_logado, app):
    """Testa que agenda retorna agendamentos ordenados por horário"""
    with app.app_context():
        # Login
        response = client.post('/api/auth/login', json={
            'username': 'funcionario',
            'password': 'senha123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Criar cliente e procedimento
        cliente = Cliente(nome='Cliente Teste', telefone='11888888888')
        db.session.add(cliente)
        db.session.flush()
        
        procedimento = Procedimento(
            nome='Volume Russo',
            preco=150.0,
            duracao_minutos=120,
            funcionario_id=funcionario_logado
        )
        db.session.add(procedimento)
        db.session.flush()
        
        # Criar agendamentos em ordem aleatória
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        agendamento1 = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario_logado,
            procedimento_id=procedimento.id,
            data_hora=hoje.replace(hour=14)
        )
        agendamento2 = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario_logado,
            procedimento_id=procedimento.id,
            data_hora=hoje.replace(hour=10)
        )
        agendamento3 = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario_logado,
            procedimento_id=procedimento.id,
            data_hora=hoje.replace(hour=16)
        )
        
        db.session.add_all([agendamento1, agendamento2, agendamento3])
        db.session.commit()
        
        # Buscar agenda
        response = client.get('/api/agendamentos/minha-agenda', headers=headers)
        
        assert response.status_code == 200
        assert response.json['total'] == 3
        
        # Verificar ordem
        agendamentos = response.json['agendamentos']
        hora1 = datetime.fromisoformat(agendamentos[0]['data_hora']).hour
        hora2 = datetime.fromisoformat(agendamentos[1]['data_hora']).hour
        hora3 = datetime.fromisoformat(agendamentos[2]['data_hora']).hour
        
        assert hora1 < hora2 < hora3

def test_agenda_apenas_funcionario_logado(client, funcionario_logado, app):
    """Testa que retorna apenas agendamentos do funcionário logado"""
    with app.app_context():
        # Login
        response = client.post('/api/auth/login', json={
            'username': 'funcionario',
            'password': 'senha123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Criar outro funcionário
        outro_funcionario = Funcionario(
            nome='Outro Funcionario',
            especialidade='Lash Designer',
            telefone='11888888888'
        )
        db.session.add(outro_funcionario)
        db.session.flush()
        
        # Criar cliente e procedimentos
        cliente = Cliente(nome='Cliente Teste', telefone='11777777777')
        db.session.add(cliente)
        db.session.flush()
        
        proc1 = Procedimento(
            nome='Volume Russo',
            preco=150.0,
            duracao_minutos=120,
            funcionario_id=funcionario_logado
        )
        proc2 = Procedimento(
            nome='Fio a Fio',
            preco=100.0,
            duracao_minutos=90,
            funcionario_id=outro_funcionario.id
        )
        db.session.add_all([proc1, proc2])
        db.session.flush()
        
        # Criar agendamentos para ambos
        hoje = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
        
        agend1 = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario_logado,
            procedimento_id=proc1.id,
            data_hora=hoje
        )
        agend2 = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=outro_funcionario.id,
            procedimento_id=proc2.id,
            data_hora=hoje.replace(hour=15)
        )
        db.session.add_all([agend1, agend2])
        db.session.commit()
        
        # Buscar agenda
        response = client.get('/api/agendamentos/minha-agenda', headers=headers)
        
        assert response.status_code == 200
        assert response.json['total'] == 1
        assert response.json['agendamentos'][0]['funcionario_id'] == funcionario_logado

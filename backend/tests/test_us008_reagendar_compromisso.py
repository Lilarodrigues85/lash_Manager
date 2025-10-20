"""
Testes para US008 - Reagendar Compromisso

Como recepcionista
Eu quero alterar data/horário de um agendamento
Para que eu possa atender solicitações de mudança
"""

import pytest
from datetime import datetime, timedelta
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.procedimento import Procedimento
from app.models.usuario import Usuario

def test_reagendar_data_hora(app, client, auth_headers):
    """Deve permitir alterar data e horário do agendamento"""
    with app.app_context():
        from app import db
        usuario = Usuario(username='func1', email='func1@test.com', nome='Func 1', tipo_usuario='funcionario')
        usuario.set_password('123')
        cliente = Cliente(nome='Cliente Teste', telefone='11999999999')
        funcionario = Funcionario(nome='Func Teste', telefone='11888888888', especialidade='Lash', usuario=usuario)
        db.session.add_all([usuario, cliente, funcionario])
        db.session.commit()
        
        procedimento = Procedimento(nome='Lash Lifting', preco=150.0, duracao_minutos=60, funcionario_id=funcionario.id)
        db.session.add(procedimento)
        db.session.commit()
    
        data_original = datetime.now() + timedelta(days=1)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario.id,
            procedimento_id=procedimento.id,
            data_hora=data_original
        )
        db.session.add(agendamento)
        db.session.commit()
        agendamento_id = agendamento.id
    
    nova_data = data_original + timedelta(days=1)
    response = client.put(
        f'/api/agendamentos/{agendamento_id}',
        json={'data_hora': nova_data.isoformat()},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert datetime.fromisoformat(data['data_hora'].replace('Z', '+00:00')).date() == nova_data.date()

def test_reagendar_validar_conflito(app, client, auth_headers):
    """Não deve permitir reagendar para horário já ocupado"""
    with app.app_context():
        from app import db
        usuario = Usuario(username='func2', email='func2@test.com', nome='Func 2', tipo_usuario='funcionario')
        usuario.set_password('123')
        cliente1 = Cliente(nome='Cliente 1', telefone='11999999991')
        cliente2 = Cliente(nome='Cliente 2', telefone='11999999992')
        funcionario = Funcionario(nome='Func Teste', telefone='11888888888', especialidade='Lash', usuario=usuario)
        db.session.add_all([usuario, cliente1, cliente2, funcionario])
        db.session.commit()
        
        procedimento = Procedimento(nome='Lash Lifting', preco=150.0, duracao_minutos=60, funcionario_id=funcionario.id)
        db.session.add(procedimento)
        db.session.commit()
    
        data1 = datetime.now() + timedelta(days=1, hours=10)
        data2 = datetime.now() + timedelta(days=1, hours=14)
        
        agendamento1 = Agendamento(
            cliente_id=cliente1.id,
            funcionario_id=funcionario.id,
            procedimento_id=procedimento.id,
            data_hora=data1
        )
        agendamento2 = Agendamento(
            cliente_id=cliente2.id,
            funcionario_id=funcionario.id,
            procedimento_id=procedimento.id,
            data_hora=data2
        )
        db.session.add_all([agendamento1, agendamento2])
        db.session.commit()
        agendamento2_id = agendamento2.id
    
    response = client.put(
        f'/api/agendamentos/{agendamento2_id}',
        json={'data_hora': data1.isoformat()},
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert 'ocupado' in response.get_json()['error'].lower()

def test_reagendar_alterar_funcionario(app, client, auth_headers):
    """Deve permitir alterar funcionário do agendamento"""
    with app.app_context():
        from app import db
        usuario1 = Usuario(username='func3', email='func3@test.com', nome='Func 3', tipo_usuario='funcionario')
        usuario1.set_password('123')
        usuario2 = Usuario(username='func4', email='func4@test.com', nome='Func 4', tipo_usuario='funcionario')
        usuario2.set_password('123')
        cliente = Cliente(nome='Cliente Teste', telefone='11999999999')
        funcionario1 = Funcionario(nome='Func 1', telefone='11888888881', especialidade='Lash', usuario=usuario1)
        funcionario2 = Funcionario(nome='Func 2', telefone='11888888882', especialidade='Lash', usuario=usuario2)
        db.session.add_all([usuario1, usuario2, cliente, funcionario1, funcionario2])
        db.session.commit()
        
        procedimento = Procedimento(nome='Lash Lifting', preco=150.0, duracao_minutos=60, funcionario_id=funcionario1.id)
        db.session.add(procedimento)
        db.session.commit()
    
        data_hora = datetime.now() + timedelta(days=1)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario1.id,
            procedimento_id=procedimento.id,
            data_hora=data_hora
        )
        db.session.add(agendamento)
        db.session.commit()
        agendamento_id = agendamento.id
        funcionario2_id = funcionario2.id
    
    response = client.put(
        f'/api/agendamentos/{agendamento_id}',
        json={'funcionario_id': funcionario2_id},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['funcionario_id'] == funcionario2_id

def test_reagendar_alterar_procedimento(app, client, auth_headers):
    """Deve permitir alterar procedimento do agendamento"""
    with app.app_context():
        from app import db
        usuario = Usuario(username='func5', email='func5@test.com', nome='Func 5', tipo_usuario='funcionario')
        usuario.set_password('123')
        cliente = Cliente(nome='Cliente Teste', telefone='11999999999')
        funcionario = Funcionario(nome='Func Teste', telefone='11888888888', especialidade='Lash', usuario=usuario)
        db.session.add_all([usuario, cliente, funcionario])
        db.session.commit()
        
        procedimento1 = Procedimento(nome='Lash Lifting', preco=150.0, duracao_minutos=60, funcionario_id=funcionario.id)
        procedimento2 = Procedimento(nome='Volume Russo', preco=200.0, duracao_minutos=90, funcionario_id=funcionario.id)
        db.session.add_all([procedimento1, procedimento2])
        db.session.commit()
    
        data_hora = datetime.now() + timedelta(days=1)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario.id,
            procedimento_id=procedimento1.id,
            data_hora=data_hora
        )
        db.session.add(agendamento)
        db.session.commit()
        agendamento_id = agendamento.id
        procedimento2_id = procedimento2.id
    
    response = client.put(
        f'/api/agendamentos/{agendamento_id}',
        json={'procedimento_id': procedimento2_id},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['procedimento_id'] == procedimento2_id

def test_reagendar_alterar_observacoes(app, client, auth_headers):
    """Deve permitir alterar observações do agendamento"""
    with app.app_context():
        from app import db
        usuario = Usuario(username='func6', email='func6@test.com', nome='Func 6', tipo_usuario='funcionario')
        usuario.set_password('123')
        cliente = Cliente(nome='Cliente Teste', telefone='11999999999')
        funcionario = Funcionario(nome='Func Teste', telefone='11888888888', especialidade='Lash', usuario=usuario)
        db.session.add_all([usuario, cliente, funcionario])
        db.session.commit()
        
        procedimento = Procedimento(nome='Lash Lifting', preco=150.0, duracao_minutos=60, funcionario_id=funcionario.id)
        db.session.add(procedimento)
        db.session.commit()
    
        data_hora = datetime.now() + timedelta(days=1)
        agendamento = Agendamento(
            cliente_id=cliente.id,
            funcionario_id=funcionario.id,
            procedimento_id=procedimento.id,
            data_hora=data_hora,
            observacoes='Observação original'
        )
        db.session.add(agendamento)
        db.session.commit()
        agendamento_id = agendamento.id
    
    response = client.put(
        f'/api/agendamentos/{agendamento_id}',
        json={'observacoes': 'Nova observação'},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['observacoes'] == 'Nova observação'

def test_reagendar_agendamento_inexistente(client, auth_headers):
    """Deve retornar 404 para agendamento inexistente"""
    response = client.put(
        '/api/agendamentos/99999',
        json={'data_hora': datetime.now().isoformat()},
        headers=auth_headers
    )
    
    assert response.status_code == 404

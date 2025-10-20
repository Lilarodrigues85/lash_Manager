"""
Testes de Integração - ÉPICO 0 + ÉPICO 1
Testa a integração entre Sistema de Permissões e Gestão de Clientes
"""
import pytest
from app import create_app, db
from app.models.usuario import Usuario
from app.models.funcionario import Funcionario
from app.models.cliente import Cliente

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Criar admin se não existir
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(
                username='admin',
                email='admin@test.com',
                nome='Admin',
                tipo_usuario='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_headers(client):
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def funcionario_headers(client, admin_headers):
    """Cria funcionário e retorna headers autenticados"""
    # Criar funcionário
    client.post('/api/funcionarios/', 
        headers=admin_headers,
        json={
            'nome': 'Funcionário Teste',
            'especialidade': 'Lash Designer',
            'telefone': '11999999999',
            'porcentagem': 25.0,
            'email': 'func@test.com',
            'username': 'funcionario',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'funcionario',
        'password': 'senha123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_funcionario_pode_cadastrar_cliente(client, funcionario_headers):
    """Teste 1: Funcionário pode cadastrar cliente"""
    response = client.post('/api/clientes/',
        headers=funcionario_headers,
        json={
            'nome': 'Cliente Teste',
            'telefone': '11988888888',
            'email': 'cliente@test.com'
        }
    )
    
    assert response.status_code == 201
    assert response.json['nome'] == 'Cliente Teste'

def test_funcionario_pode_buscar_cliente(client, funcionario_headers):
    """Teste 2: Funcionário pode buscar cliente"""
    # Criar cliente
    client.post('/api/clientes/',
        headers=funcionario_headers,
        json={
            'nome': 'Maria Silva',
            'telefone': '11977777777',
            'email': 'maria@test.com'
        }
    )
    
    # Buscar
    response = client.get('/api/clientes/??busca=Maria', headers=funcionario_headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_funcionario_pode_editar_cliente(client, funcionario_headers):
    """Teste 3: Funcionário pode editar cliente"""
    # Criar cliente
    response = client.post('/api/clientes/',
        headers=funcionario_headers,
        json={
            'nome': 'João Santos',
            'telefone': '11966666666',
            'email': 'joao@test.com'
        }
    )
    cliente_id = response.json['id']
    
    # Editar
    response = client.put(f'/api/clientes/{cliente_id}',
        headers=funcionario_headers,
        json={
            'nome': 'João Santos Editado',
            'telefone': '11966666666',
            'email': 'joao@test.com'
        }
    )
    
    assert response.status_code == 200
    assert response.json['nome'] == 'João Santos Editado'

def test_funcionario_pode_ver_historico_cliente(client, funcionario_headers):
    """Teste 4: Funcionário pode ver histórico do cliente"""
    # Criar cliente
    response = client.post('/api/clientes/',
        headers=funcionario_headers,
        json={
            'nome': 'Ana Costa',
            'telefone': '11955555555',
            'email': 'ana@test.com'
        }
    )
    cliente_id = response.json['id']
    
    # Ver histórico
    response = client.get(f'/api/clientes/{cliente_id}/historico', headers=funcionario_headers)
    assert response.status_code == 200

def test_admin_pode_desativar_cliente(client, admin_headers):
    """Teste 5: Admin pode desativar cliente"""
    # Criar cliente
    response = client.post('/api/clientes/',
        headers=admin_headers,
        json={
            'nome': 'Pedro Lima',
            'telefone': '11944444444',
            'email': 'pedro@test.com'
        }
    )
    cliente_id = response.json['id']
    
    # Desativar
    response = client.delete(f'/api/clientes/{cliente_id}', headers=admin_headers)
    assert response.status_code == 200

def test_fluxo_completo_admin_funcionario_cliente(client, admin_headers, app):
    """Teste 6: Fluxo completo - Admin cria funcionário que gerencia clientes"""
    # 1. Admin cria funcionário
    response = client.post('/api/funcionarios/', 
        headers=admin_headers,
        json={
            'nome': 'Lash Designer',
            'especialidade': 'Volume Russo',
            'telefone': '11933333333',
            'porcentagem': 30.0,
            'email': 'lash@test.com',
            'username': 'lash',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    assert response.status_code == 201
    
    # 2. Funcionário faz login
    response = client.post('/api/auth/login', json={
        'username': 'lash',
        'password': 'senha123'
    })
    assert response.status_code == 200
    func_token = response.json['access_token']
    func_headers = {'Authorization': f'Bearer {func_token}'}
    
    # 3. Funcionário cadastra cliente
    response = client.post('/api/clientes/',
        headers=func_headers,
        json={
            'nome': 'Cliente VIP',
            'telefone': '11922222222',
            'email': 'vip@test.com',
            'observacoes': 'Cliente preferencial'
        }
    )
    assert response.status_code == 201
    cliente_id = response.json['id']
    
    # 4. Funcionário busca cliente
    response = client.get('/api/clientes/?search=VIP', headers=func_headers)
    assert response.status_code == 200
    assert response.json['success'] == True
    
    # 5. Funcionário edita cliente
    response = client.put(f'/api/clientes/{cliente_id}',
        headers=func_headers,
        json={
            'nome': 'Cliente VIP Premium',
            'telefone': '11922222222',
            'email': 'vip@test.com'
        }
    )
    assert response.status_code == 200
    
    # 6. Admin lista todos os clientes
    response = client.get('/api/clientes/', headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_multiplos_funcionarios_gerenciam_clientes(client, admin_headers):
    """Teste 7: Múltiplos funcionários podem gerenciar clientes"""
    # Criar funcionário 1
    client.post('/api/funcionarios/', 
        headers=admin_headers,
        json={
            'nome': 'Funcionário 1',
            'especialidade': 'Lash Designer',
            'telefone': '11911111111',
            'porcentagem': 25.0,
            'email': 'func1@test.com',
            'username': 'func1',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Criar funcionário 2
    client.post('/api/funcionarios/', 
        headers=admin_headers,
        json={
            'nome': 'Funcionário 2',
            'especialidade': 'Lash Designer',
            'telefone': '11900000000',
            'porcentagem': 25.0,
            'email': 'func2@test.com',
            'username': 'func2',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Login func1
    response = client.post('/api/auth/login', json={
        'username': 'func1',
        'password': 'senha123'
    })
    func1_headers = {'Authorization': f'Bearer {response.json["access_token"]}'}
    
    # Login func2
    response = client.post('/api/auth/login', json={
        'username': 'func2',
        'password': 'senha123'
    })
    func2_headers = {'Authorization': f'Bearer {response.json["access_token"]}'}
    
    # Func1 cria cliente
    response = client.post('/api/clientes/',
        headers=func1_headers,
        json={
            'nome': 'Cliente Func1',
            'telefone': '11988888888',
            'email': 'cliente1@test.com'
        }
    )
    assert response.status_code == 201
    
    # Func2 cria cliente
    response = client.post('/api/clientes/',
        headers=func2_headers,
        json={
            'nome': 'Cliente Func2',
            'telefone': '11977777777',
            'email': 'cliente2@test.com'
        }
    )
    assert response.status_code == 201
    
    # Ambos podem ver todos os clientes
    response = client.get('/api/clientes/', headers=func1_headers)
    assert len(response.json) >= 2
    
    response = client.get('/api/clientes/', headers=func2_headers)
    assert len(response.json) >= 2

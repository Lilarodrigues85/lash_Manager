"""
Testes de Integração - ÉPICO 0: Sistema de Permissões
Testa o fluxo completo de gestão de usuários e permissões
"""
import pytest
from app import create_app, db
from app.models.usuario import Usuario
from app.models.funcionario import Funcionario

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Criar admin padrão se não existir
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
def auth_headers(client):
    """Retorna headers com token de autenticação do admin"""
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_criar_funcionario_com_usuario_admin(client, auth_headers, app):
    """Teste 1: Criar funcionário com acesso admin"""
    response = client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'João Silva',
            'especialidade': 'Lash Designer',
            'telefone': '11999999999',
            'porcentagem': 30.0,
            'email': 'joao@test.com',
            'username': 'joao',
            'password': 'senha123',
            'tipo_usuario': 'admin'
        }
    )
    
    assert response.status_code == 201
    data = response.json
    assert data['nome'] == 'João Silva'
    assert 'usuario' in data
    assert data['usuario']['tipo_usuario'] == 'admin'
    
    # Verificar no banco
    with app.app_context():
        usuario = Usuario.query.filter_by(username='joao').first()
        assert usuario is not None
        assert usuario.tipo_usuario == 'admin'
        assert usuario.check_password('senha123')

def test_criar_funcionario_com_usuario_funcionario(client, auth_headers, app):
    """Teste 2: Criar funcionário com acesso funcionário"""
    response = client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Maria Santos',
            'especialidade': 'Lash Designer',
            'telefone': '11988888888',
            'porcentagem': 25.0,
            'email': 'maria@test.com',
            'username': 'maria',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    assert response.status_code == 201
    data = response.json
    assert data['usuario']['tipo_usuario'] == 'funcionario'

def test_login_funcionario_e_verificar_permissoes(client, auth_headers, app):
    """Teste 3: Login de funcionário e verificação de permissões"""
    # Criar funcionário
    client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Pedro Costa',
            'especialidade': 'Lash Designer',
            'telefone': '11977777777',
            'porcentagem': 25.0,
            'email': 'pedro@test.com',
            'username': 'pedro',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Login como funcionário
    response = client.post('/api/auth/login', json={
        'username': 'pedro',
        'password': 'senha123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert response.json['usuario']['tipo_usuario'] == 'funcionario'

def test_funcionario_nao_pode_acessar_usuarios(client, auth_headers, app):
    """Teste 4: Funcionário não pode acessar gestão de usuários"""
    # Criar funcionário
    client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Ana Lima',
            'especialidade': 'Lash Designer',
            'telefone': '11966666666',
            'porcentagem': 25.0,
            'email': 'ana@test.com',
            'username': 'ana',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Login como funcionário
    response = client.post('/api/auth/login', json={
        'username': 'ana',
        'password': 'senha123'
    })
    func_token = response.json['access_token']
    func_headers = {'Authorization': f'Bearer {func_token}'}
    
    # Tentar acessar rota de usuários
    response = client.get('/api/usuarios', headers=func_headers)
    assert response.status_code == 403

def test_validacao_email_duplicado(client, auth_headers):
    """Teste 5: Validação de email duplicado"""
    # Criar primeiro funcionário
    client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Carlos Silva',
            'especialidade': 'Lash Designer',
            'telefone': '11955555555',
            'porcentagem': 25.0,
            'email': 'carlos@test.com',
            'username': 'carlos',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Tentar criar com mesmo email
    response = client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Carlos Outro',
            'especialidade': 'Lash Designer',
            'telefone': '11944444444',
            'porcentagem': 25.0,
            'email': 'carlos@test.com',
            'username': 'carlos2',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    assert response.status_code == 400
    assert 'Email já existe' in response.json['error']

def test_validacao_username_duplicado(client, auth_headers):
    """Teste 6: Validação de username duplicado"""
    # Criar primeiro funcionário
    client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Lucia Souza',
            'especialidade': 'Lash Designer',
            'telefone': '11933333333',
            'porcentagem': 25.0,
            'email': 'lucia@test.com',
            'username': 'lucia',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    # Tentar criar com mesmo username
    response = client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Lucia Outra',
            'especialidade': 'Lash Designer',
            'telefone': '11922222222',
            'porcentagem': 25.0,
            'email': 'lucia2@test.com',
            'username': 'lucia',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    
    assert response.status_code == 400
    assert 'Username já existe' in response.json['error']

def test_fluxo_completo_epico0(client, auth_headers, app):
    """Teste 7: Fluxo completo do ÉPICO 0"""
    # 1. Admin cria funcionário com acesso
    response = client.post('/api/funcionarios/', 
        headers=auth_headers,
        json={
            'nome': 'Teste Completo',
            'especialidade': 'Lash Designer',
            'telefone': '11911111111',
            'porcentagem': 25.0,
            'email': 'teste@test.com',
            'username': 'teste',
            'password': 'senha123',
            'tipo_usuario': 'funcionario'
        }
    )
    assert response.status_code == 201
    funcionario_id = response.json['id']
    
    # 2. Funcionário faz login
    response = client.post('/api/auth/login', json={
        'username': 'teste',
        'password': 'senha123'
    })
    assert response.status_code == 200
    
    # 3. Admin lista funcionários
    response = client.get('/api/funcionarios/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) > 0
    
    # 4. Admin desativa funcionário
    response = client.delete(f'/api/funcionarios/{funcionario_id}', headers=auth_headers)
    assert response.status_code == 200
    
    # 5. Verificar se funcionário foi desativado
    with app.app_context():
        funcionario = Funcionario.query.get(funcionario_id)
        assert funcionario.ativo == False

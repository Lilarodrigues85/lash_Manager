"""
Configuração de fixtures para testes
"""
import pytest
import sys
sys.path.insert(0, '..')

@pytest.fixture
def app():
    """Cria instância da aplicação para testes"""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Cria cliente de teste"""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Headers de autenticação para testes"""
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }

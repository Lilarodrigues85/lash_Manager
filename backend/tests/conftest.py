"""
Configuração de fixtures para testes
"""
import pytest

@pytest.fixture
def app():
    """Cria instância da aplicação para testes"""
    from app import create_app, db
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cria cliente de teste"""
    return app.test_client()

@pytest.fixture
def auth_headers(app):
    """Headers de autenticação para testes"""
    from flask_jwt_extended import create_access_token
    from app.models.usuario import Usuario
    from app import db
    
    with app.app_context():
        user = Usuario(username='testuser', email='test@test.com', nome='Test User', tipo_usuario='admin')
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id))
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

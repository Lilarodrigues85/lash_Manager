from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///lash_manager.db?check_same_thread=False')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    CORS(app)
    
    from app.routes.auth import auth_bp
    from app.routes.clientes import clientes_bp
    from app.routes.funcionarios import funcionarios_bp
    from app.routes.procedimentos import procedimentos_bp
    from app.routes.agendamentos import agendamentos_bp
    from app.routes.pagamentos import pagamentos_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.mensagens import mensagens_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(funcionarios_bp, url_prefix='/api/funcionarios')
    app.register_blueprint(procedimentos_bp, url_prefix='/api/procedimentos')
    app.register_blueprint(agendamentos_bp, url_prefix='/api/agendamentos')
    app.register_blueprint(pagamentos_bp, url_prefix='/api/pagamentos')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(mensagens_bp, url_prefix='/api/mensagens')
    
    return app
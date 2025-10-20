from app import db
from datetime import datetime

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    porcentagem = db.Column(db.Numeric(5, 2), default=25.00)
    ativo = db.Column(db.Boolean, default=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    usuario = db.relationship('Usuario', backref='funcionario', lazy=True)
    procedimentos = db.relationship('Procedimento', backref='funcionario', lazy=True)
    agendamentos = db.relationship('Agendamento', backref='funcionario', lazy=True)
    
    def to_dict(self):
        result = {
            'id': self.id,
            'nome': self.nome,
            'especialidade': self.especialidade,
            'telefone': self.telefone,
            'porcentagem': float(self.porcentagem),
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if self.usuario:
            result['usuario'] = {
                'id': self.usuario.id,
                'username': self.usuario.username,
                'email': self.usuario.email,
                'tipo_usuario': self.usuario.tipo_usuario
            }
        return result
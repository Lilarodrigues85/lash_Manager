from app import db
from datetime import datetime

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    procedimentos = db.relationship('Procedimento', backref='funcionario', lazy=True)
    agendamentos = db.relationship('Agendamento', backref='funcionario', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'especialidade': self.especialidade,
            'telefone': self.telefone,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
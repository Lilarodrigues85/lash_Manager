from app import db
from datetime import datetime

class Procedimento(db.Model):
    __tablename__ = 'procedimentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='procedimento', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': float(self.preco),
            'duracao_minutos': self.duracao_minutos,
            'descricao': self.descricao,
            'funcionario_id': self.funcionario_id,
            'funcionario_nome': self.funcionario.nome if self.funcionario else None,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
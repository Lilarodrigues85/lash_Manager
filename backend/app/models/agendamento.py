from app import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    procedimento_id = db.Column(db.Integer, db.ForeignKey('procedimentos.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='agendado')  # agendado, realizado, cancelado
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    pagamentos = db.relationship('Pagamento', backref='agendamento', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'funcionario_id': self.funcionario_id,
            'funcionario_nome': self.funcionario.nome if self.funcionario else None,
            'procedimento_id': self.procedimento_id,
            'procedimento_nome': self.procedimento.nome if self.procedimento else None,
            'procedimento_preco': float(self.procedimento.preco) if self.procedimento else None,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
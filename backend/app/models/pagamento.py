from app import db
from datetime import datetime

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamentos.id'))
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)  # dinheiro, cartao, pix
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pago')  # pago, pendente, cancelado
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'agendamento_id': self.agendamento_id,
            'valor': float(self.valor),
            'forma_pagamento': self.forma_pagamento,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
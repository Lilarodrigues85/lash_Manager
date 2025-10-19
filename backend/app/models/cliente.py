from app import db
from datetime import datetime
import re

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True)
    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)
    pagamentos = db.relationship('Pagamento', backref='cliente', lazy=True)
    
    def validate_data(self):
        """Valida os dados do cliente"""
        if not self.nome or len(self.nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if not self.telefone or len(self.telefone.strip()) < 10:
            raise ValueError("Telefone deve ter pelo menos 10 dígitos")
        
        if self.email and not self._is_valid_email(self.email):
            raise ValueError("Email inválido")
        
        # Limpar e formatar dados
        self.nome = self.nome.strip().title()
        self.telefone = self._format_phone(self.telefone)
        if self.email:
            self.email = self.email.strip().lower()
    
    def _is_valid_email(self, email):
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _format_phone(self, phone):
        """Formata telefone removendo caracteres especiais"""
        return re.sub(r'\D', '', phone)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'observacoes': self.observacoes,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def search(cls, query):
        """Busca clientes por nome, telefone ou email"""
        return cls.query.filter(
            db.or_(
                cls.nome.ilike(f'%{query}%'),
                cls.telefone.ilike(f'%{query}%'),
                cls.email.ilike(f'%{query}%')
            )
        ).filter(cls.ativo == True)
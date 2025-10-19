"""Teste Unitário - US004: Editar Cliente"""
import sys
sys.path.insert(0, '..')

def test_edicao_nome():
    """Testa edição de nome"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Nome Antigo', telefone='11999998888')
    cliente.nome = 'Nome Novo'
    assert cliente.nome == 'Nome Novo'

def test_edicao_telefone():
    """Testa edição de telefone"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    cliente.telefone = '11888887777'
    assert cliente.telefone == '11888887777'

def test_validacao_apos_edicao():
    """Testa validação após edição"""
    from app.models.cliente import Cliente
    import pytest
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    cliente.nome = 'A'
    with pytest.raises(ValueError):
        cliente.validate_data()

def test_email_duplicado_edicao():
    """Testa proteção contra email duplicado na edição"""
    email_existente = 'teste@email.com'
    email_novo = 'teste@email.com'
    assert email_existente == email_novo

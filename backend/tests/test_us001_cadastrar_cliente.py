"""Teste Unitário - US001: Cadastrar Cliente"""
import pytest
import sys
sys.path.insert(0, '..')

def test_cadastrar_cliente_valido():
    """Testa cadastro com dados válidos"""
    from app.models.cliente import Cliente
    cliente = Cliente(nome='Maria Silva', telefone='11999998888', email='maria@test.com')
    assert cliente.nome == 'Maria Silva'
    assert len(cliente.telefone) >= 10

def test_validacao_nome_minimo():
    """Testa validação de nome mínimo"""
    from app.models.cliente import Cliente
    with pytest.raises(ValueError):
        cliente = Cliente(nome='A', telefone='11999998888')
        cliente.validate_data()

def test_validacao_telefone_minimo():
    """Testa validação de telefone mínimo"""
    from app.models.cliente import Cliente
    with pytest.raises(ValueError):
        cliente = Cliente(nome='João Silva', telefone='123')
        cliente.validate_data()

def test_validacao_email_formato():
    """Testa validação de formato de email"""
    from app.models.cliente import Cliente
    with pytest.raises(ValueError):
        cliente = Cliente(nome='Pedro', telefone='11999998888', email='invalido')
        cliente.validate_data()

def test_formatacao_automatica():
    """Testa formatação automática de dados"""
    from app.models.cliente import Cliente
    cliente = Cliente(nome='ana costa', telefone='(11) 99999-8888', email='ANA@TEST.COM')
    cliente.validate_data()
    assert cliente.nome == 'Ana Costa'
    assert cliente.email == 'ana@test.com'

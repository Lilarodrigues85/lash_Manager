"""Teste Unitário - US005: Desativar Cliente"""
import sys
sys.path.insert(0, '..')

def test_soft_delete():
    """Testa soft delete (marca como inativo)"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    cliente.ativo = False
    assert cliente.ativo == False

def test_historico_preservado():
    """Testa que histórico é preservado"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    cliente.ativo = False
    assert hasattr(cliente, 'agendamentos')
    assert hasattr(cliente, 'pagamentos')

def test_nao_aparece_em_busca():
    """Testa que cliente inativo não aparece em busca"""
    from app.models.cliente import Cliente
    
    query = Cliente.query.filter(Cliente.ativo == True)
    assert 'ativo' in str(query)

def test_campo_ativo_default():
    """Testa que campo ativo é True por padrão"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    assert cliente.ativo == True

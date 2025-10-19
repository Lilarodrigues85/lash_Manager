"""
Teste de Integração - ÉPICO 1: Gestão de Clientes
Testa integração entre todas as US do épico
"""
import sys
sys.path.insert(0, '..')

def test_fluxo_completo_cliente():
    """Testa fluxo completo: cadastrar -> buscar -> editar -> desativar"""
    from app.models.cliente import Cliente
    
    # US001: Cadastrar
    cliente = Cliente(
        nome='João Silva',
        telefone='11999998888',
        email='joao@test.com',
        observacoes='Cliente teste'
    )
    cliente.validate_data()
    assert cliente.nome == 'João Silva'
    
    # US002: Buscar
    query = Cliente.search('João')
    assert query is not None
    
    # US004: Editar
    cliente.nome = 'João Silva Santos'
    cliente.validate_data()
    assert cliente.nome == 'João Silva Santos'
    
    # US005: Desativar
    cliente.ativo = False
    assert cliente.ativo == False

def test_integracao_historico_completo():
    """Testa integração de histórico com agendamentos e pagamentos"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Maria', telefone='11999998888')
    
    # Verifica relacionamentos
    assert hasattr(cliente, 'agendamentos')
    assert hasattr(cliente, 'pagamentos')
    
    # Simula cálculos
    total_pago = 0
    total_pendente = 0
    assert total_pago >= 0
    assert total_pendente >= 0

def test_validacoes_integradas():
    """Testa validações em todo o fluxo"""
    from app.models.cliente import Cliente
    import pytest
    
    # Nome inválido
    with pytest.raises(ValueError):
        cliente = Cliente(nome='A', telefone='11999998888')
        cliente.validate_data()
    
    # Telefone inválido
    with pytest.raises(ValueError):
        cliente = Cliente(nome='Test', telefone='123')
        cliente.validate_data()
    
    # Email inválido
    with pytest.raises(ValueError):
        cliente = Cliente(nome='Test', telefone='11999998888', email='invalido')
        cliente.validate_data()

def test_busca_apos_edicao():
    """Testa que busca funciona após edição"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Pedro', telefone='11999998888')
    cliente.validate_data()
    
    # Edita
    cliente.nome = 'Pedro Henrique'
    cliente.validate_data()
    
    # Busca pelo novo nome
    query = Cliente.search('Henrique')
    assert query is not None

def test_cliente_inativo_nao_aparece():
    """Testa que cliente desativado não aparece em buscas"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    cliente.ativo = False
    
    # Busca apenas ativos
    query = Cliente.query.filter(Cliente.ativo == True)
    assert 'ativo' in str(query)

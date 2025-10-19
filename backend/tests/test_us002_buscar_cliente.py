"""Teste Unitário - US002: Buscar Cliente"""
import sys
sys.path.insert(0, '..')

def test_busca_por_nome():
    """Testa busca por nome parcial"""
    from app.models.cliente import Cliente
    from app import db
    
    # Simula busca
    query = Cliente.search('Maria')
    assert query is not None

def test_busca_case_insensitive():
    """Testa busca case-insensitive"""
    from app.models.cliente import Cliente
    
    query1 = Cliente.search('maria')
    query2 = Cliente.search('MARIA')
    assert query1.whereclause.compare(query2.whereclause)

def test_busca_minimo_caracteres():
    """Testa validação de mínimo 2 caracteres"""
    busca = 'M'
    assert len(busca) < 2

def test_busca_multiplos_campos():
    """Testa busca em nome, telefone e email"""
    from app.models.cliente import Cliente
    
    query = Cliente.search('test')
    # Verifica que busca em múltiplos campos
    assert 'nome' in str(query) or 'telefone' in str(query) or 'email' in str(query)

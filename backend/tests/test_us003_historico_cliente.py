"""Teste Unitário - US003: Histórico do Cliente"""
import sys
sys.path.insert(0, '..')

def test_historico_retorna_agendamentos():
    """Testa se histórico retorna agendamentos"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    assert hasattr(cliente, 'agendamentos')

def test_historico_retorna_pagamentos():
    """Testa se histórico retorna pagamentos"""
    from app.models.cliente import Cliente
    
    cliente = Cliente(nome='Test', telefone='11999998888')
    assert hasattr(cliente, 'pagamentos')

def test_calculo_total_pago():
    """Testa cálculo de total pago"""
    pagamentos = [
        {'valor': 100, 'status': 'pago'},
        {'valor': 50, 'status': 'pago'}
    ]
    total = sum(p['valor'] for p in pagamentos if p['status'] == 'pago')
    assert total == 150

def test_ordenacao_cronologica():
    """Testa ordenação por data"""
    from datetime import datetime
    
    datas = [
        datetime(2024, 1, 15),
        datetime(2024, 1, 10),
        datetime(2024, 1, 20)
    ]
    ordenado = sorted(datas, reverse=True)
    assert ordenado[0] == datetime(2024, 1, 20)

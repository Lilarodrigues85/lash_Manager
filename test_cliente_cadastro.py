#!/usr/bin/env python3
"""
Teste do cadastro de clientes - ÉPICO 1: Gestão de Clientes - US001
Sistema LashManager - Padrões DATAMETRIA
"""

import requests
import json
import sys

# Configurações
BASE_URL = "http://localhost:5000/api"
TEST_USER = {
    "username": "admin",
    "password": "admin123"
}

def get_auth_token():
    """Obtém token de autenticação"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=TEST_USER)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"❌ Erro na autenticação: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def test_cliente_cadastro():
    """Testa o cadastro de clientes"""
    print("🧪 Iniciando testes do cadastro de clientes...")
    
    # Obter token
    token = get_auth_token()
    if not token:
        print("❌ Não foi possível obter token de autenticação")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Casos de teste
    test_cases = [
        {
            "name": "Cliente válido completo",
            "data": {
                "nome": "Maria Silva Santos",
                "telefone": "(11) 99999-8888",
                "email": "maria.silva@email.com",
                "observacoes": "Cliente preferencial, gosta de extensões volume russo"
            },
            "should_pass": True
        },
        {
            "name": "Cliente válido sem email",
            "data": {
                "nome": "Ana Costa",
                "telefone": "11987654321",
                "observacoes": "Primeira vez no salão"
            },
            "should_pass": True
        },
        {
            "name": "Cliente inválido - nome muito curto",
            "data": {
                "nome": "A",
                "telefone": "11999998888"
            },
            "should_pass": False
        },
        {
            "name": "Cliente inválido - telefone muito curto",
            "data": {
                "nome": "João Silva",
                "telefone": "123"
            },
            "should_pass": False
        },
        {
            "name": "Cliente inválido - email inválido",
            "data": {
                "nome": "Pedro Santos",
                "telefone": "11999998888",
                "email": "email-invalido"
            },
            "should_pass": False
        },
        {
            "name": "Cliente inválido - sem nome",
            "data": {
                "telefone": "11999998888"
            },
            "should_pass": False
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Teste {i}: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/clientes",
                json=test_case['data'],
                headers=headers
            )
            
            success = response.status_code in [200, 201]
            response_data = response.json()
            
            if test_case['should_pass']:
                if success and response_data.get('success'):
                    print(f"✅ PASSOU - Cliente cadastrado: {response_data.get('cliente', {}).get('nome', 'N/A')}")
                    results.append(True)
                else:
                    print(f"❌ FALHOU - Deveria passar mas falhou: {response_data.get('error', 'Erro desconhecido')}")
                    results.append(False)
            else:
                if not success or not response_data.get('success'):
                    print(f"✅ PASSOU - Erro esperado: {response_data.get('error', 'Erro de validação')}")
                    results.append(True)
                else:
                    print(f"❌ FALHOU - Deveria falhar mas passou")
                    results.append(False)
                    
        except Exception as e:
            print(f"❌ ERRO - Exceção durante o teste: {e}")
            results.append(False)
    
    # Teste de listagem
    print(f"\n📋 Teste {len(test_cases) + 1}: Listagem de clientes")
    try:
        response = requests.get(f"{BASE_URL}/clientes", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'clientes' in data:
                print(f"✅ PASSOU - {len(data['clientes'])} clientes encontrados")
                results.append(True)
            else:
                print(f"❌ FALHOU - Resposta inválida: {data}")
                results.append(False)
        else:
            print(f"❌ FALHOU - Status: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"❌ ERRO - Exceção durante listagem: {e}")
        results.append(False)
    
    # Resultados finais
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 RESULTADOS FINAIS:")
    print(f"✅ Testes passaram: {passed}/{total}")
    print(f"❌ Testes falharam: {total - passed}/{total}")
    print(f"📈 Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema de cadastro funcionando corretamente.")
        return True
    else:
        print(f"\n⚠️  {total - passed} TESTE(S) FALHARAM. Revisar implementação.")
        return False

if __name__ == "__main__":
    success = test_cliente_cadastro()
    sys.exit(0 if success else 1)
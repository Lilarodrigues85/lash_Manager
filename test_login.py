#!/usr/bin/env python3
"""
Teste de login direto no backend
"""
import requests
import json

def test_login():
    url = 'http://localhost:5000/api/auth/login'
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    print("Testando login no backend...")
    print(f"URL: {url}")
    print(f"Dados: {data}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("Login bem-sucedido!")
            print(f"Resposta: {json.dumps(result, indent=2)}")
            
            if 'access_token' in result:
                print(f"Token recebido: {result['access_token'][:20]}...")
            else:
                print("ERRO: Token não encontrado na resposta!")
        else:
            print(f"Erro no login: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERRO: Backend não está rodando em localhost:5000")
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == '__main__':
    test_login()
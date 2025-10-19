# 🧪 Testes - ÉPICO 1: Gestão de Clientes

## 📋 Estrutura de Testes

### Testes Unitários (por US)
- `test_us001_cadastrar_cliente.py` - US001: Cadastrar Cliente
- `test_us002_buscar_cliente.py` - US002: Buscar Cliente
- `test_us003_historico_cliente.py` - US003: Histórico do Cliente
- `test_us004_editar_cliente.py` - US004: Editar Cliente
- `test_us005_desativar_cliente.py` - US005: Desativar Cliente

### Teste de Integração
- `test_epico1_integracao.py` - Integração entre todas as US do ÉPICO 1

### Teste E2E
- `test_e2e_gestao_clientes.py` - Fluxo completo de gestão de clientes

## 🚀 Como Executar

### Todos os testes
```bash
cd backend/tests
pytest -v
```

### Teste específico
```bash
pytest test_us001_cadastrar_cliente.py -v
```

### Teste de integração
```bash
pytest test_epico1_integracao.py -v
```

### Teste E2E
```bash
pytest test_e2e_gestao_clientes.py -v
python test_e2e_gestao_clientes.py
```

## 📊 Cobertura

- **US001**: 5 testes unitários
- **US002**: 4 testes unitários
- **US003**: 4 testes unitários
- **US004**: 4 testes unitários
- **US005**: 4 testes unitários
- **Integração**: 5 testes
- **E2E**: 6 cenários completos

**Total**: 32 testes

## ✅ Critérios de Sucesso

- Todos os testes unitários passam
- Teste de integração valida fluxo completo
- Teste E2E simula usuário real
- Cobertura > 80%

---

**ÉPICO 1**: ✅ 100% Testado
**Padrões**: DATAMETRIA v3.3.8

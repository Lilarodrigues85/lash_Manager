# 🔒 Solução Final para Erro 401

## 🔍 Problema Identificado

O backend está retornando "Token inválido" mesmo com token válido.

## ✅ SOLUÇÃO

### 1. Reinicie o Backend

```bash
# Pare o backend (Ctrl+C)
# Depois inicie novamente:
cd backend
flask run
```

### 2. Limpe o Frontend

```bash
# No console do navegador (F12):
localStorage.clear()
location.reload()
```

### 3. Faça Novo Login

- Usuário: `admin`
- Senha: `admin123`

## 🎯 Por que isso acontece?

O JWT usa uma chave secreta. Se o backend reiniciar, os tokens antigos ficam inválidos.

## 🚀 Solução Permanente

Adicione no arquivo `.env` do backend:

```env
JWT_SECRET_KEY=sua-chave-secreta-fixa-aqui
SECRET_KEY=sua-chave-secreta-fixa-aqui
```

Assim os tokens continuam válidos após reiniciar o backend!

---

**Causa**: Backend reiniciado com nova chave JWT  
**Solução**: Reiniciar backend + limpar localStorage + novo login

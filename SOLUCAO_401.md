# 🔒 Solução para Erro 401 (UNAUTHORIZED)

## 🔍 Diagnóstico

O token está sendo carregado do localStorage mas as requisições retornam 401.

## ✅ Soluções

### 1. Token Expirado (Mais Provável)

O token JWT expira após 1 hora. Se passou desse tempo, faça:

```javascript
// No console do navegador
localStorage.clear()
// Depois recarregue e faça login novamente
```

### 2. Verificar se Header está sendo enviado

Abra o console e veja os logs:
- 🔑 Token: Existe
- ✅ Header Authorization adicionado
- 📤 Request: GET /api/clientes

Se aparecer isso, o problema é token expirado.

### 3. Fazer Novo Login

1. Limpe o localStorage:
```bash
F12 > Console > localStorage.clear()
```

2. Recarregue a página (F5)

3. Faça login novamente:
   - Usuário: `admin`
   - Senha: `admin123`

### 4. Verificar Backend

Se o problema persistir, verifique se o backend está rodando:

```bash
cd backend
flask run
```

## 🚀 Solução Rápida

Execute no console do navegador:

```javascript
localStorage.clear()
location.reload()
```

Depois faça login novamente!

---

**Causa**: Token JWT expira após 1 hora  
**Solução**: Limpar localStorage e fazer novo login

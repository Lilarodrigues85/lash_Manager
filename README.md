# 💅 LashManager - Sistema de Gestão para Salão de Lash Designer

<div align="center">

[![DATAMETRIA](https://img.shields.io/badge/DATAMETRIA-Standards-blue)](https://github.com/datametria/DATAMETRIA-standards)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3.4-brightgreen)](https://vuejs.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.21-orange)](https://www.sqlalchemy.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)

Sistema completo de gestão para salões de lash designer com controle de clientes, procedimentos, agenda e financeiro.

[🚀 Instalação](#-instalação) • [📖 Documentação](#-documentação) • [🎯 Funcionalidades](#-funcionalidades) • [🏗️ Arquitetura](#️-arquitetura)

</div>

---

## 🎯 Funcionalidades

### 👥 Gestão de Clientes
- ✅ Cadastro completo de clientes
- ✅ Histórico de procedimentos realizados
- ✅ Controle de pagamentos e pendências
- ✅ Notas e observações personalizadas

### 👩‍💼 Gestão de Funcionários
- ✅ Cadastro de 3 funcionários especializados
- ✅ Tipos de procedimentos por funcionário
- ✅ Controle de agenda individual
- ✅ Relatórios de performance

### 📅 Sistema de Agenda
- ✅ Agendamento por funcionário
- ✅ Controle de horários disponíveis
- ✅ Notificações de compromissos
- ✅ Reagendamento e cancelamentos

### 💰 Controle Financeiro
- ✅ Registro de pagamentos recebidos
- ✅ Controle de valores pendentes
- ✅ Relatórios financeiros detalhados
- ✅ Dashboard de receitas

### 🎨 Procedimentos
- ✅ Catálogo de procedimentos de lash
- ✅ Preços e durações configuráveis
- ✅ Histórico por cliente
- ✅ Fotos antes/depois

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Setup Rápido

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/lash-manager.git
cd lash-manager

# Backend (Flask)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
flask db upgrade
flask run

# Frontend (Vue.js)
cd ../frontend
npm install
npm run dev
```

### Configuração do Banco

```bash
# PostgreSQL
createdb lash_manager
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🏗️ Arquitetura

### Stack Tecnológico

```mermaid
graph TB
    subgraph "Frontend"
        A[Vue.js 3 + TypeScript]
        B[Pinia Store]
        C[Vue Router]
        D[Vuetify 3]
    end

    subgraph "Backend"
        E[Flask + SQLAlchemy]
        F[Flask-JWT-Extended]
        G[Flask-CORS]
        H[Marshmallow]
    end

    subgraph "Database"
        I[PostgreSQL]
        J[Redis Cache]
    end

    A --> E
    B --> F
    E --> I
    F --> J
```

### Estrutura do Projeto

```
lash-manager/
├── backend/                 # API Flask
│   ├── app/
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── routes/         # Endpoints da API
│   │   ├── services/       # Lógica de negócio
│   │   └── utils/          # Utilitários
│   ├── migrations/         # Migrações do banco
│   └── requirements.txt
├── frontend/               # Interface Vue.js
│   ├── src/
│   │   ├── components/     # Componentes Vue
│   │   ├── views/          # Páginas
│   │   ├── stores/         # Pinia stores
│   │   └── services/       # Serviços HTTP
│   └── package.json
└── docs/                   # Documentação
```

---

## 📊 Modelos de Dados

### Principais Entidades

```mermaid
erDiagram
    Cliente ||--o{ Agendamento : tem
    Cliente ||--o{ Pagamento : faz
    Funcionario ||--o{ Agendamento : atende
    Funcionario ||--o{ Procedimento : realiza
    Agendamento ||--|| Procedimento : inclui
    Agendamento ||--o{ Pagamento : gera

    Cliente {
        int id PK
        string nome
        string telefone
        string email
        text observacoes
        datetime created_at
    }

    Funcionario {
        int id PK
        string nome
        string especialidade
        string telefone
        boolean ativo
    }

    Procedimento {
        int id PK
        string nome
        decimal preco
        int duracao_minutos
        string descricao
        int funcionario_id FK
    }

    Agendamento {
        int id PK
        int cliente_id FK
        int funcionario_id FK
        int procedimento_id FK
        datetime data_hora
        string status
        text observacoes
    }

    Pagamento {
        int id PK
        int cliente_id FK
        int agendamento_id FK
        decimal valor
        string forma_pagamento
        datetime data_pagamento
        string status
    }
```

---

## 🎨 Interface do Usuário

### Dashboard Principal

- **Agenda do Dia**: Próximos agendamentos
- **Receita Diária**: Valores recebidos e pendentes
- **Clientes Ativos**: Lista de clientes recentes
- **Alertas**: Pagamentos em atraso e lembretes

### Módulos Principais

1. **👥 Clientes**
   - Lista com busca e filtros
   - Perfil detalhado do cliente
   - Histórico de procedimentos
   - Controle de pagamentos

2. **📅 Agenda**
   - Calendário semanal/mensal
   - Agendamento rápido
   - Gestão de horários
   - Notificações automáticas

3. **💰 Financeiro**
   - Dashboard de receitas
   - Controle de pendências
   - Relatórios mensais
   - Formas de pagamento

4. **👩‍💼 Funcionários**
   - Perfil e especialidades
   - Agenda individual
   - Performance e métricas
   - Configuração de horários

---

## 🔧 Configuração

### Variáveis de Ambiente

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/lash_manager
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Configuração de Produção

```bash
# Build do frontend
cd frontend
npm run build

# Deploy com Docker
docker-compose up -d
```

---

## 📱 Responsividade

O sistema é totalmente responsivo e funciona perfeitamente em:

- 💻 **Desktop**: Interface completa
- 📱 **Mobile**: Interface otimizada para toque
- 📟 **Tablet**: Layout adaptativo

---

## 🔒 Segurança

- ✅ Autenticação JWT
- ✅ Validação de dados
- ✅ Proteção CSRF
- ✅ Sanitização de inputs
- ✅ HTTPS obrigatório em produção

---

## 📈 Métricas e Analytics

### KPIs Principais
- Taxa de ocupação da agenda
- Receita média por cliente
- Procedimentos mais populares
- Performance por funcionário

### Relatórios Disponíveis
- Relatório mensal de receitas
- Análise de clientes
- Performance de funcionários
- Procedimentos realizados

---

## 🚀 Roadmap

### v1.0 - MVP (Atual)
- [x] Gestão básica de clientes
- [x] Sistema de agenda
- [x] Controle financeiro
- [x] Dashboard principal

### v1.1 - Melhorias
- [ ] Notificações por WhatsApp
- [ ] Relatórios avançados
- [ ] Backup automático
- [ ] App mobile

### v2.0 - Expansão
- [ ] Multi-salão
- [ ] Integração com redes sociais
- [ ] Sistema de fidelidade
- [ ] IA para recomendações

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Suporte

- 📧 **Email**: dalila.analistadesistema@gmail.com  
- 💬 **WhatsApp**:
- 📖 **Documentação**: [docs.lashmanager.com](https://docs.lashmanager.com)

---

<div align="center">

**Desenvolvido com 💜 pela equipe DATAMETRIA**

*Sistema profissional para gestão completa de salões de lash designer*

</div>
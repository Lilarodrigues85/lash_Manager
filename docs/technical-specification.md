# 🏗️ LashManager - Especificação Técnica

<div align="center">

[![DATAMETRIA](https://img.shields.io/badge/DATAMETRIA-Standards-blue)](https://github.com/datametria/DATAMETRIA-standards)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3.4-brightgreen)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)

Especificação técnica completa do sistema de gestão para salões de lash designer

[🏗️ Arquitetura](#️-arquitetura) • [🗄️ Banco de Dados](#️-banco-de-dados) • [🔌 APIs](#-apis) • [🎨 Frontend](#-frontend)

</div>

---

## 🏗️ Arquitetura do Sistema

### 📊 Visão Geral da Arquitetura

```mermaid
graph TB
    subgraph "Client Layer"
        A[Vue.js 3 SPA]
        B[PWA Service Worker]
        C[Vuetify Components]
    end

    subgraph "API Gateway"
        D[Flask Application]
        E[JWT Authentication]
        F[CORS Middleware]
    end

    subgraph "Business Logic"
        G[Service Layer]
        H[Repository Pattern]
        I[Domain Models]
    end

    subgraph "Data Layer"
        J[PostgreSQL Database]
        K[Redis Cache]
        L[File Storage]
    end

    subgraph "External Services"
        M[WhatsApp API]
        N[Email Service]
        O[Payment Gateway]
    end

    A --> D
    B --> D
    C --> D
    D --> E
    D --> F
    E --> G
    F --> G
    G --> H
    H --> I
    I --> J
    G --> K
    G --> L
    G --> M
    G --> N
    G --> O

    classDef frontend fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    classDef api fill:#E8F5E8,stroke:#388E3C,stroke-width:2px
    classDef business fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    classDef data fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    classDef external fill:#FFEBEE,stroke:#D32F2F,stroke-width:2px

    class A,B,C frontend
    class D,E,F api
    class G,H,I business
    class J,K,L data
    class M,N,O external
```

### 🎯 Padrões Arquiteturais

#### Clean Architecture
```
├── Domain Layer (Entities)
│   ├── Cliente
│   ├── Funcionario
│   ├── Agendamento
│   └── Pagamento
├── Application Layer (Use Cases)
│   ├── ClienteService
│   ├── AgendamentoService
│   └── PagamentoService
├── Infrastructure Layer
│   ├── Database (SQLAlchemy)
│   ├── External APIs
│   └── File System
└── Presentation Layer
    ├── REST API (Flask)
    └── Web UI (Vue.js)
```

#### Repository Pattern
```python
# Interface
class ClienteRepository(ABC):
    @abstractmethod
    def criar(self, cliente: Cliente) -> Cliente:
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Cliente]:
        pass

# Implementação
class SQLAlchemyClienteRepository(ClienteRepository):
    def criar(self, cliente: Cliente) -> Cliente:
        db.session.add(cliente)
        db.session.commit()
        return cliente
```

---

## 🗄️ Banco de Dados

### 📋 Modelo de Dados Completo

```mermaid
erDiagram
    Cliente ||--o{ Agendamento : "tem"
    Cliente ||--o{ Pagamento : "faz"
    Funcionario ||--o{ Agendamento : "atende"
    Funcionario ||--o{ Procedimento : "realiza"
    Agendamento ||--|| Procedimento : "inclui"
    Agendamento ||--o{ Pagamento : "gera"
    Usuario ||--|| Funcionario : "é"

    Cliente {
        int id PK
        string nome "NOT NULL"
        string telefone "UNIQUE, NOT NULL"
        string email "UNIQUE"
        date data_nascimento
        text endereco
        text observacoes
        boolean ativo "DEFAULT TRUE"
        timestamp created_at "DEFAULT NOW()"
        timestamp updated_at "DEFAULT NOW()"
    }

    Funcionario {
        int id PK
        string nome "NOT NULL"
        string especialidade
        string telefone
        string email
        json horario_trabalho
        boolean ativo "DEFAULT TRUE"
        decimal comissao_percentual "DEFAULT 0"
        timestamp created_at "DEFAULT NOW()"
    }

    Usuario {
        int id PK
        string username "UNIQUE, NOT NULL"
        string password_hash "NOT NULL"
        string email "UNIQUE, NOT NULL"
        enum role "admin, funcionario, recepcionista"
        int funcionario_id FK
        boolean ativo "DEFAULT TRUE"
        timestamp last_login
        timestamp created_at "DEFAULT NOW()"
    }

    Procedimento {
        int id PK
        string nome "NOT NULL"
        text descricao
        decimal preco "NOT NULL"
        int duracao_minutos "NOT NULL"
        int funcionario_id FK
        boolean ativo "DEFAULT TRUE"
        timestamp created_at "DEFAULT NOW()"
    }

    Agendamento {
        int id PK
        int cliente_id FK "NOT NULL"
        int funcionario_id FK "NOT NULL"
        int procedimento_id FK "NOT NULL"
        timestamp data_hora "NOT NULL"
        enum status "agendado, confirmado, em_andamento, concluido, cancelado, nao_compareceu"
        text observacoes
        decimal valor_cobrado
        timestamp created_at "DEFAULT NOW()"
        timestamp updated_at "DEFAULT NOW()"
    }

    Pagamento {
        int id PK
        int cliente_id FK "NOT NULL"
        int agendamento_id FK
        decimal valor "NOT NULL"
        enum forma_pagamento "dinheiro, pix, debito, credito, transferencia"
        enum status "pendente, pago, cancelado"
        date data_vencimento
        timestamp data_pagamento
        text observacoes
        timestamp created_at "DEFAULT NOW()"
    }

    Configuracao {
        int id PK
        string chave "UNIQUE, NOT NULL"
        text valor
        string tipo "string, number, boolean, json"
        text descricao
        timestamp updated_at "DEFAULT NOW()"
    }
```

### 🔧 Scripts de Criação

#### Tabela Clientes
```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    data_nascimento DATE,
    endereco TEXT,
    observacoes TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clientes_nome ON clientes(nome);
CREATE INDEX idx_clientes_telefone ON clientes(telefone);
CREATE INDEX idx_clientes_ativo ON clientes(ativo);
```

#### Tabela Agendamentos
```sql
CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    funcionario_id INTEGER NOT NULL REFERENCES funcionarios(id),
    procedimento_id INTEGER NOT NULL REFERENCES procedimentos(id),
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'agendado' CHECK (status IN ('agendado', 'confirmado', 'em_andamento', 'concluido', 'cancelado', 'nao_compareceu')),
    observacoes TEXT,
    valor_cobrado DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agendamentos_data_hora ON agendamentos(data_hora);
CREATE INDEX idx_agendamentos_funcionario ON agendamentos(funcionario_id);
CREATE INDEX idx_agendamentos_status ON agendamentos(status);
```

### 📊 Otimizações de Performance

#### Índices Estratégicos
```sql
-- Busca rápida de clientes
CREATE INDEX idx_clientes_busca ON clientes USING gin(to_tsvector('portuguese', nome || ' ' || COALESCE(telefone, '')));

-- Agenda por funcionário e data
CREATE INDEX idx_agendamentos_funcionario_data ON agendamentos(funcionario_id, data_hora);

-- Pagamentos por status e data
CREATE INDEX idx_pagamentos_status_data ON pagamentos(status, data_vencimento);
```

#### Particionamento (Futuro)
```sql
-- Particionamento por mês para agendamentos
CREATE TABLE agendamentos_2024_01 PARTITION OF agendamentos
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

---

## 🔌 APIs REST

### 🎯 Estrutura de Endpoints

#### Clientes API
```python
# GET /api/clientes - Listar clientes
@app.route('/api/clientes', methods=['GET'])
@jwt_required()
def listar_clientes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Cliente.query
    if search:
        query = query.filter(
            Cliente.nome.ilike(f'%{search}%') |
            Cliente.telefone.ilike(f'%{search}%')
        )
    
    clientes = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return {
        'clientes': [cliente.to_dict() for cliente in clientes.items],
        'total': clientes.total,
        'pages': clientes.pages,
        'current_page': page
    }

# POST /api/clientes - Criar cliente
@app.route('/api/clientes', methods=['POST'])
@jwt_required()
def criar_cliente():
    data = request.get_json()
    
    # Validação
    schema = ClienteSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return {'errors': err.messages}, 400
    
    # Verificar duplicatas
    if Cliente.query.filter_by(telefone=validated_data['telefone']).first():
        return {'error': 'Telefone já cadastrado'}, 409
    
    cliente = Cliente(**validated_data)
    db.session.add(cliente)
    db.session.commit()
    
    return cliente.to_dict(), 201
```

#### Agendamentos API
```python
# GET /api/agendamentos - Listar agendamentos
@app.route('/api/agendamentos', methods=['GET'])
@jwt_required()
def listar_agendamentos():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    funcionario_id = request.args.get('funcionario_id', type=int)
    status = request.args.get('status')
    
    query = Agendamento.query
    
    if data_inicio:
        query = query.filter(Agendamento.data_hora >= data_inicio)
    if data_fim:
        query = query.filter(Agendamento.data_hora <= data_fim)
    if funcionario_id:
        query = query.filter(Agendamento.funcionario_id == funcionario_id)
    if status:
        query = query.filter(Agendamento.status == status)
    
    agendamentos = query.order_by(Agendamento.data_hora).all()
    
    return {
        'agendamentos': [ag.to_dict() for ag in agendamentos]
    }

# POST /api/agendamentos - Criar agendamento
@app.route('/api/agendamentos', methods=['POST'])
@jwt_required()
def criar_agendamento():
    data = request.get_json()
    
    # Validações de negócio
    if not validar_horario_disponivel(
        data['funcionario_id'], 
        data['data_hora'], 
        data['duracao']
    ):
        return {'error': 'Horário não disponível'}, 409
    
    agendamento = Agendamento(**data)
    db.session.add(agendamento)
    db.session.commit()
    
    # Enviar notificação
    enviar_confirmacao_agendamento(agendamento)
    
    return agendamento.to_dict(), 201
```

### 📋 Schemas de Validação

#### Cliente Schema
```python
from marshmallow import Schema, fields, validate

class ClienteSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    telefone = fields.Str(required=True, validate=validate.Regexp(r'^\(\d{2}\)\s\d{4,5}-\d{4}$'))
    email = fields.Email(allow_none=True)
    data_nascimento = fields.Date(allow_none=True)
    endereco = fields.Str(allow_none=True)
    observacoes = fields.Str(allow_none=True)
```

#### Agendamento Schema
```python
class AgendamentoSchema(Schema):
    cliente_id = fields.Int(required=True)
    funcionario_id = fields.Int(required=True)
    procedimento_id = fields.Int(required=True)
    data_hora = fields.DateTime(required=True)
    observacoes = fields.Str(allow_none=True)
    
    @validates('data_hora')
    def validate_data_hora(self, value):
        if value < datetime.now():
            raise ValidationError('Data deve ser futura')
        
        if value.weekday() == 6:  # Domingo
            raise ValidationError('Não atendemos aos domingos')
```

### 🔐 Autenticação JWT

```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Configuração JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
jwt = JWTManager(app)

# Login endpoint
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = Usuario.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'role': user.role,
                'funcionario_id': user.funcionario_id
            }
        )
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }
    
    return {'error': 'Credenciais inválidas'}, 401
```

---

## 🎨 Frontend (Vue.js 3)

### 🏗️ Estrutura de Componentes

```
src/
├── components/
│   ├── common/
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   └── AppFooter.vue
│   ├── clientes/
│   │   ├── ClienteList.vue
│   │   ├── ClienteForm.vue
│   │   └── ClienteCard.vue
│   ├── agendamentos/
│   │   ├── AgendaCalendar.vue
│   │   ├── AgendamentoForm.vue
│   │   └── AgendamentoCard.vue
│   └── dashboard/
│       ├── DashboardStats.vue
│       ├── RecentClients.vue
│       └── TodaySchedule.vue
├── views/
│   ├── Dashboard.vue
│   ├── Clientes.vue
│   ├── Agendamentos.vue
│   └── Financeiro.vue
├── stores/
│   ├── auth.js
│   ├── clientes.js
│   └── agendamentos.js
└── services/
    ├── api.js
    ├── auth.js
    └── utils.js
```

### 🔄 Gerenciamento de Estado (Pinia)

#### Auth Store
```javascript
import { defineStore } from 'pinia'
import { authService } from '@/services/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),

  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    isFuncionario: (state) => state.user?.role === 'funcionario'
  },

  actions: {
    async login(credentials) {
      try {
        const response = await authService.login(credentials)
        this.token = response.access_token
        this.user = response.user
        this.isAuthenticated = true
        
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    }
  }
})
```

#### Clientes Store
```javascript
export const useClientesStore = defineStore('clientes', {
  state: () => ({
    clientes: [],
    loading: false,
    currentPage: 1,
    totalPages: 1,
    searchQuery: ''
  }),

  actions: {
    async fetchClientes(page = 1, search = '') {
      this.loading = true
      try {
        const response = await api.get('/clientes', {
          params: { page, search, per_page: 20 }
        })
        
        this.clientes = response.data.clientes
        this.currentPage = response.data.current_page
        this.totalPages = response.data.pages
        this.searchQuery = search
      } catch (error) {
        console.error('Erro ao buscar clientes:', error)
      } finally {
        this.loading = false
      }
    },

    async createCliente(clienteData) {
      try {
        const response = await api.post('/clientes', clienteData)
        this.clientes.unshift(response.data)
        return response.data
      } catch (error) {
        throw error
      }
    }
  }
})
```

### 📱 Componentes Principais

#### Cliente Form
```vue
<template>
  <v-form ref="form" v-model="valid" @submit.prevent="submit">
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="cliente.nome"
          label="Nome completo"
          :rules="nomeRules"
          required
        />
      </v-col>
      
      <v-col cols="12" md="6">
        <v-text-field
          v-model="cliente.telefone"
          label="Telefone"
          :rules="telefoneRules"
          v-mask="'(##) #####-####'"
          required
        />
      </v-col>
      
      <v-col cols="12" md="6">
        <v-text-field
          v-model="cliente.email"
          label="Email"
          :rules="emailRules"
          type="email"
        />
      </v-col>
      
      <v-col cols="12">
        <v-textarea
          v-model="cliente.observacoes"
          label="Observações"
          rows="3"
        />
      </v-col>
    </v-row>
    
    <v-row>
      <v-col>
        <v-btn
          type="submit"
          color="primary"
          :loading="loading"
          :disabled="!valid"
        >
          {{ isEdit ? 'Atualizar' : 'Cadastrar' }}
        </v-btn>
        
        <v-btn
          @click="$emit('cancel')"
          class="ml-2"
        >
          Cancelar
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useClientesStore } from '@/stores/clientes'

const props = defineProps({
  clienteData: Object,
  isEdit: Boolean
})

const emit = defineEmits(['success', 'cancel'])

const clientesStore = useClientesStore()
const form = ref(null)
const valid = ref(false)
const loading = ref(false)

const cliente = ref({
  nome: '',
  telefone: '',
  email: '',
  observacoes: '',
  ...props.clienteData
})

const nomeRules = [
  v => !!v || 'Nome é obrigatório',
  v => v.length >= 2 || 'Nome deve ter pelo menos 2 caracteres'
]

const telefoneRules = [
  v => !!v || 'Telefone é obrigatório',
  v => /^\(\d{2}\)\s\d{4,5}-\d{4}$/.test(v) || 'Formato inválido'
]

const emailRules = [
  v => !v || /.+@.+\..+/.test(v) || 'Email inválido'
]

const submit = async () => {
  if (!valid.value) return
  
  loading.value = true
  try {
    if (props.isEdit) {
      await clientesStore.updateCliente(cliente.value)
    } else {
      await clientesStore.createCliente(cliente.value)
    }
    
    emit('success')
  } catch (error) {
    console.error('Erro ao salvar cliente:', error)
  } finally {
    loading.value = false
  }
}
</script>
```

### 🎨 Tema e Estilização

#### Vuetify Theme
```javascript
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#E91E63',
          secondary: '#FF4081',
          accent: '#9C27B0',
          error: '#F44336',
          warning: '#FF9800',
          info: '#2196F3',
          success: '#4CAF50'
        }
      },
      dark: {
        colors: {
          primary: '#E91E63',
          secondary: '#FF4081',
          accent: '#9C27B0',
          error: '#CF6679',
          warning: '#FF9800',
          info: '#2196F3',
          success: '#4CAF50'
        }
      }
    }
  }
})
```

---

## 🔧 Configurações de Deploy

### 🐳 Docker Configuration

#### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### Dockerfile (Frontend)
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: lash_manager
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/lash_manager
      REDIS_URL: redis://redis:6379
      JWT_SECRET_KEY: your-secret-key
    depends_on:
      - db
      - redis
    ports:
      - "5000:5000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### ☁️ Configuração de Produção

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name lashmanager.com;

    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Static files
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Environment Variables
```bash
# Production
DATABASE_URL=postgresql://user:pass@prod-db:5432/lash_manager
REDIS_URL=redis://prod-redis:6379
JWT_SECRET_KEY=super-secret-production-key
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=noreply@lashmanager.com
MAIL_PASSWORD=app-specific-password
```

---

## 📊 Monitoramento e Logs

### 📈 Métricas de Performance

#### Application Metrics
```python
from prometheus_client import Counter, Histogram, generate_latest

# Métricas customizadas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
    REQUEST_LATENCY.observe(time.time() - request.start_time)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest()
```

### 📝 Sistema de Logs

```python
import logging
from logging.handlers import RotatingFileHandler

# Configuração de logs
if not app.debug:
    file_handler = RotatingFileHandler('logs/lashmanager.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('LashManager startup')

# Log de auditoria
def log_user_action(user_id, action, resource, resource_id=None):
    app.logger.info(f'User {user_id} performed {action} on {resource} {resource_id}')
```

---

## 🔒 Segurança

### 🛡️ Medidas de Proteção

#### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass
```

#### Input Validation
```python
from marshmallow import ValidationError
import bleach

def sanitize_input(data):
    """Sanitiza inputs do usuário"""
    if isinstance(data, str):
        return bleach.clean(data, strip=True)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    return data

@app.before_request
def sanitize_request_data():
    if request.is_json:
        request.json = sanitize_input(request.get_json())
```

#### CORS Configuration
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://lashmanager.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 🧪 Testes

### 🔬 Estrutura de Testes

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
├── e2e/
│   ├── test_user_flows.py
│   └── test_critical_paths.py
└── fixtures/
    ├── clientes.json
    └── agendamentos.json
```

#### Testes Unitários
```python
import pytest
from app.models import Cliente
from app.services import ClienteService

class TestClienteService:
    def test_criar_cliente_valido(self):
        data = {
            'nome': 'Maria Silva',
            'telefone': '(11) 99999-9999',
            'email': 'maria@email.com'
        }
        
        cliente = ClienteService.criar(data)
        
        assert cliente.id is not None
        assert cliente.nome == 'Maria Silva'
        assert cliente.ativo is True

    def test_criar_cliente_telefone_duplicado(self):
        # Criar primeiro cliente
        ClienteService.criar({
            'nome': 'João',
            'telefone': '(11) 88888-8888'
        })
        
        # Tentar criar com mesmo telefone
        with pytest.raises(ValidationError):
            ClienteService.criar({
                'nome': 'Pedro',
                'telefone': '(11) 88888-8888'
            })
```

#### Testes de API
```python
def test_listar_clientes_autenticado(client, auth_headers):
    response = client.get('/api/clientes', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'clientes' in data
    assert isinstance(data['clientes'], list)

def test_criar_cliente_dados_validos(client, auth_headers):
    cliente_data = {
        'nome': 'Ana Costa',
        'telefone': '(11) 77777-7777',
        'email': 'ana@email.com'
    }
    
    response = client.post('/api/clientes', 
                          json=cliente_data, 
                          headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['nome'] == 'Ana Costa'
```

---

## 📋 Checklist de Deploy

### ✅ Pré-Deploy
- [ ] Testes unitários passando (>90% cobertura)
- [ ] Testes de integração passando
- [ ] Build do frontend sem erros
- [ ] Migrações de banco testadas
- [ ] Variáveis de ambiente configuradas
- [ ] Certificados SSL válidos
- [ ] Backup do banco de dados

### ✅ Deploy
- [ ] Deploy do banco de dados
- [ ] Deploy do backend
- [ ] Deploy do frontend
- [ ] Configuração do proxy reverso
- [ ] Testes de smoke em produção
- [ ] Monitoramento ativo
- [ ] Logs funcionando

### ✅ Pós-Deploy
- [ ] Verificação de funcionalidades críticas
- [ ] Teste de performance
- [ ] Monitoramento de erros
- [ ] Backup automático configurado
- [ ] Documentação atualizada

---

<div align="center">

**Desenvolvido com 💜 por Lila Rodrigues**

*Especificação técnica completa do LashManager v1.0*

**Última atualização**: 29/09/2025
**Próxima revisão**: Dezembro 2025

</div>
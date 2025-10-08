# 💅 LashManager - Product Backlog

<div align="center">

[![DATAMETRIA](https://img.shields.io/badge/DATAMETRIA-Standards-blue)](https://github.com/datametria/DATAMETRIA-standards)
[![Product Backlog](https://img.shields.io/badge/Product-Backlog-green)](https://github.com/datametria/DATAMETRIA-standards)
[![Version](https://img.shields.io/badge/version-1.0-blue)](https://github.com/Lilarodrigues85/lash_Manager)

Sistema completo de gestão para salões de lash designer

[🎯 Épicos](#-épicos) • [📋 User Stories](#-user-stories) • [🚀 Roadmap](#-roadmap) • [📊 Métricas](#-métricas)

</div>

---

## 🎯 Épicos

### Epic 1: Gestão de Clientes
**Objetivo**: Sistema completo para cadastro, histórico e acompanhamento de clientes

### Epic 2: Sistema de Agenda
**Objetivo**: Agendamento inteligente com controle de horários e notificações

### Epic 3: Controle Financeiro
**Objetivo**: Gestão completa de pagamentos, receitas e relatórios financeiros

### Epic 4: Gestão de Funcionários
**Objetivo**: Cadastro de profissionais, especialidades e controle de performance

### Epic 5: Catálogo de Procedimentos
**Objetivo**: Gestão de serviços, preços e durações

### Epic 6: Dashboard e Relatórios
**Objetivo**: Visão analítica do negócio com KPIs e métricas

---

## 📋 User Stories

### 🎯 Epic 1: Gestão de Clientes

#### US001 - Cadastro de Cliente
**Como** proprietária do salão  
**Eu quero** cadastrar novos clientes com informações completas  
**Para que** eu possa manter um registro organizado da minha clientela

**Critérios de Aceitação:**
- [ ] Campos obrigatórios: Nome, Telefone
- [ ] Campos opcionais: Email, Observações
- [ ] Validação de telefone brasileiro
- [ ] Validação de email (se preenchido)
- [ ] Não permitir clientes duplicados (mesmo telefone)

**Estimativa:** 5 Story Points  
**Prioridade:** Alta  
**Sprint:** 1

#### US002 - Histórico do Cliente
**Como** lash designer  
**Eu quero** visualizar o histórico completo de procedimentos de um cliente  
**Para que** eu possa oferecer um atendimento personalizado

**Critérios de Aceitação:**
- [ ] Lista cronológica de procedimentos realizados
- [ ] Detalhes: data, procedimento, funcionário, valor
- [ ] Fotos antes/depois (se disponível)
- [ ] Observações específicas de cada atendimento
- [ ] Tempo desde último procedimento

**Estimativa:** 8 Story Points  
**Prioridade:** Média  
**Sprint:** 2

#### US003 - Busca e Filtros de Clientes
**Como** recepcionista  
**Eu quero** buscar clientes rapidamente  
**Para que** eu possa agilizar o atendimento

**Critérios de Aceitação:**
- [ ] Busca por nome (parcial)
- [ ] Busca por telefone
- [ ] Filtro por data de cadastro
- [ ] Filtro por último atendimento
- [ ] Ordenação por nome, data de cadastro

**Estimativa:** 3 Story Points  
**Prioridade:** Média  
**Sprint:** 2

### 🎯 Epic 2: Sistema de Agenda

#### US004 - Agendamento Básico
**Como** recepcionista  
**Eu quero** agendar procedimentos para clientes  
**Para que** eu possa organizar a agenda do salão

**Critérios de Aceitação:**
- [ ] Seleção de cliente, funcionário, procedimento
- [ ] Seleção de data e horário
- [ ] Validação de conflitos de horário
- [ ] Cálculo automático de duração
- [ ] Status: Agendado, Realizado, Cancelado

**Estimativa:** 13 Story Points  
**Prioridade:** Alta  
**Sprint:** 1

#### US005 - Visualização de Agenda
**Como** lash designer  
**Eu quero** visualizar minha agenda diária/semanal  
**Para que** eu possa me organizar para os atendimentos

**Critérios de Aceitação:**
- [ ] Visualização por dia, semana, mês
- [ ] Filtro por funcionário
- [ ] Cores diferentes por status
- [ ] Detalhes do agendamento ao clicar
- [ ] Horários livres visíveis

**Estimativa:** 8 Story Points  
**Prioridade:** Alta  
**Sprint:** 1

#### US006 - Reagendamento
**Como** recepcionista  
**Eu quero** reagendar compromissos  
**Para que** eu possa ajustar a agenda conforme necessário

**Critérios de Aceitação:**
- [ ] Arrastar e soltar para novo horário
- [ ] Validação de conflitos
- [ ] Histórico de reagendamentos
- [ ] Notificação automática (futuro)

**Estimativa:** 5 Story Points  
**Prioridade:** Média  
**Sprint:** 3

### 🎯 Epic 3: Controle Financeiro

#### US007 - Registro de Pagamento
**Como** recepcionista  
**Eu quero** registrar pagamentos recebidos  
**Para que** eu possa controlar as receitas do salão

**Critérios de Aceitação:**
- [ ] Formas de pagamento: Dinheiro, PIX, Cartão
- [ ] Valor pago (pode ser parcial)
- [ ] Data do pagamento
- [ ] Vinculação com agendamento
- [ ] Status: Pago, Pendente, Parcial

**Estimativa:** 8 Story Points  
**Prioridade:** Alta  
**Sprint:** 2

#### US008 - Controle de Pendências
**Como** proprietária  
**Eu quero** visualizar pagamentos pendentes  
**Para que** eu possa fazer o acompanhamento de cobranças

**Critérios de Aceitação:**
- [ ] Lista de pagamentos em aberto
- [ ] Ordenação por data de vencimento
- [ ] Valor total em aberto
- [ ] Filtro por cliente
- [ ] Alertas de atraso

**Estimativa:** 5 Story Points  
**Prioridade:** Média  
**Sprint:** 3

#### US009 - Relatório Financeiro
**Como** proprietária  
**Eu quero** gerar relatórios financeiros  
**Para que** eu possa analisar a performance do negócio

**Critérios de Aceitação:**
- [ ] Receita por período (dia/mês/ano)
- [ ] Receita por funcionário
- [ ] Receita por procedimento
- [ ] Gráficos de evolução
- [ ] Exportação para PDF/Excel

**Estimativa:** 13 Story Points  
**Prioridade:** Baixa  
**Sprint:** 4

### 🎯 Epic 4: Gestão de Funcionários

#### US010 - Cadastro de Funcionário
**Como** proprietária  
**Eu quero** cadastrar funcionários e suas especialidades  
**Para que** eu possa organizar a equipe

**Critérios de Aceitação:**
- [ ] Nome, telefone, especialidade
- [ ] Porcentagem de comissão
- [ ] Status ativo/inativo
- [ ] Procedimentos que realiza
- [ ] Horário de trabalho

**Estimativa:** 5 Story Points  
**Prioridade:** Alta  
**Sprint:** 1

#### US011 - Performance de Funcionário
**Como** proprietária  
**Eu quero** acompanhar a performance dos funcionários  
**Para que** eu possa avaliar e motivar a equipe

**Critérios de Aceitação:**
- [ ] Número de atendimentos por período
- [ ] Receita gerada
- [ ] Avaliação média dos clientes
- [ ] Comparativo entre funcionários
- [ ] Metas e objetivos

**Estimativa:** 8 Story Points  
**Prioridade:** Baixa  
**Sprint:** 4

### 🎯 Epic 5: Catálogo de Procedimentos

#### US012 - Cadastro de Procedimentos
**Como** proprietária  
**Eu quero** cadastrar os procedimentos oferecidos  
**Para que** eu possa padronizar os serviços

**Critérios de Aceitação:**
- [ ] Nome do procedimento
- [ ] Preço padrão
- [ ] Duração em minutos
- [ ] Descrição detalhada
- [ ] Funcionário responsável
- [ ] Status ativo/inativo

**Estimativa:** 3 Story Points  
**Prioridade:** Alta  
**Sprint:** 1

#### US013 - Galeria de Procedimentos
**Como** cliente  
**Eu quero** visualizar fotos dos procedimentos  
**Para que** eu possa escolher o serviço desejado

**Critérios de Aceitação:**
- [ ] Upload de múltiplas fotos
- [ ] Fotos antes/depois
- [ ] Galeria organizada por procedimento
- [ ] Zoom nas imagens
- [ ] Compartilhamento nas redes sociais

**Estimativa:** 8 Story Points  
**Prioridade:** Baixa  
**Sprint:** 5

### 🎯 Epic 6: Dashboard e Relatórios

#### US014 - Dashboard Principal
**Como** proprietária  
**Eu quero** visualizar um resumo do negócio  
**Para que** eu possa tomar decisões estratégicas

**Critérios de Aceitação:**
- [ ] Agendamentos do dia
- [ ] Receita diária/mensal
- [ ] Total de clientes
- [ ] Agendamentos pendentes
- [ ] Gráficos de performance
- [ ] Alertas importantes

**Estimativa:** 13 Story Points  
**Prioridade:** Alta  
**Sprint:** 2

#### US015 - Relatórios Gerenciais
**Como** proprietária  
**Eu quero** gerar relatórios detalhados  
**Para que** eu possa analisar tendências e oportunidades

**Critérios de Aceitação:**
- [ ] Relatório de clientes mais frequentes
- [ ] Procedimentos mais populares
- [ ] Horários de maior movimento
- [ ] Análise de sazonalidade
- [ ] Projeções de receita

**Estimativa:** 21 Story Points  
**Prioridade:** Baixa  
**Sprint:** 5

---

## 🚀 Roadmap

### Sprint 1 (2 semanas) - MVP Core
**Objetivo**: Funcionalidades essenciais para operação básica

- [x] US001 - Cadastro de Cliente
- [x] US004 - Agendamento Básico  
- [x] US005 - Visualização de Agenda
- [x] US010 - Cadastro de Funcionário
- [x] US012 - Cadastro de Procedimentos

**Entregáveis:**
- Sistema de login funcional
- CRUD básico de clientes, funcionários e procedimentos
- Agenda básica com visualização diária

### Sprint 2 (2 semanas) - Gestão Financeira
**Objetivo**: Controle básico de pagamentos e dashboard

- [ ] US002 - Histórico do Cliente
- [ ] US003 - Busca e Filtros de Clientes
- [ ] US007 - Registro de Pagamento
- [ ] US014 - Dashboard Principal

**Entregáveis:**
- Sistema de pagamentos
- Dashboard com métricas básicas
- Histórico completo de clientes

### Sprint 3 (2 semanas) - Melhorias de UX
**Objetivo**: Funcionalidades que melhoram a experiência

- [ ] US006 - Reagendamento
- [ ] US008 - Controle de Pendências
- [ ] Notificações por WhatsApp
- [ ] Tema escuro completo

**Entregáveis:**
- Reagendamento drag-and-drop
- Controle de inadimplência
- Integração WhatsApp básica

### Sprint 4 (2 semanas) - Analytics e Performance
**Objetivo**: Relatórios e análises avançadas

- [ ] US009 - Relatório Financeiro
- [ ] US011 - Performance de Funcionário
- [ ] Backup automático
- [ ] Otimizações de performance

**Entregáveis:**
- Relatórios financeiros completos
- Dashboard de funcionários
- Sistema de backup

### Sprint 5 (2 semanas) - Expansão e Futuro
**Objetivo**: Funcionalidades avançadas e preparação para escala

- [ ] US013 - Galeria de Procedimentos
- [ ] US015 - Relatórios Gerenciais
- [ ] App mobile (PWA)
- [ ] Multi-salão (preparação)

**Entregáveis:**
- Galeria de fotos
- Relatórios avançados
- Versão mobile

---

## 📊 Métricas de Sucesso

### KPIs Principais

| Métrica | Objetivo | Atual | Meta Sprint 5 |
|---------|----------|-------|---------------|
| **Taxa de Ocupação** | Agenda preenchida | 60% | 85% |
| **Receita Média/Cliente** | Valor por atendimento | R$ 80 | R$ 120 |
| **Tempo Médio de Agendamento** | Eficiência operacional | 5 min | 2 min |
| **Clientes Recorrentes** | Fidelização | 40% | 70% |
| **Satisfação do Cliente** | NPS | - | 8.5/10 |

### Métricas Técnicas

| Métrica | Objetivo | Meta |
|---------|----------|------|
| **Performance Web** | Core Web Vitals | > 90 |
| **Uptime** | Disponibilidade | > 99.5% |
| **Tempo de Resposta** | API Response | < 200ms |
| **Cobertura de Testes** | Qualidade | > 80% |

---

## 🎯 Definição de Pronto (DoD)

### Para User Stories
- [ ] Código desenvolvido e revisado
- [ ] Testes unitários implementados (>80% cobertura)
- [ ] Testes de integração passando
- [ ] Interface responsiva (mobile/desktop)
- [ ] Documentação atualizada
- [ ] Deploy em ambiente de teste
- [ ] Validação com stakeholder
- [ ] Sem bugs críticos ou bloqueantes

### Para Sprints
- [ ] Todas as User Stories da sprint concluídas
- [ ] Demo realizada com stakeholders
- [ ] Retrospectiva da equipe executada
- [ ] Deploy em produção realizado
- [ ] Métricas de performance validadas
- [ ] Documentação de release atualizada

---

## 🏷️ Critérios de Priorização

### Matriz de Prioridade (Valor vs Esforço)

#### Alto Valor + Baixo Esforço (Fazer Primeiro)
- US001 - Cadastro de Cliente
- US012 - Cadastro de Procedimentos
- US003 - Busca e Filtros

#### Alto Valor + Alto Esforço (Planejar Bem)
- US004 - Agendamento Básico
- US014 - Dashboard Principal
- US007 - Registro de Pagamento

#### Baixo Valor + Baixo Esforço (Fazer Depois)
- US006 - Reagendamento
- US008 - Controle de Pendências

#### Baixo Valor + Alto Esforço (Evitar)
- US013 - Galeria de Procedimentos
- US015 - Relatórios Gerenciais

---

## 📝 Notas e Observações

### Dependências Técnicas
- **Backend**: Flask + SQLAlchemy + PostgreSQL
- **Frontend**: Vue.js 3 + Vuetify + TypeScript
- **Mobile**: PWA (Progressive Web App)
- **Integração**: WhatsApp Business API

### Riscos Identificados
1. **Integração WhatsApp**: Dependência de API externa
2. **Performance**: Crescimento da base de dados
3. **Backup**: Perda de dados críticos
4. **Usabilidade**: Adoção pela equipe

### Stakeholders
- **Product Owner**: Dalila Rodrigues (Proprietária)
- **Scrum Master**: Equipe DATAMETRIA
- **Usuários Finais**: Lash designers, recepcionistas
- **Clientes**: Clientes do salão

---

<div align="center">

**Desenvolvido por**: Equipe DATAMETRIA  
**Última Atualização**: 06/10/2025  
**Versão**: 1.0  
**Próxima Revisão**: Sprint Review

---

### 💅 LashManager - Transformando a gestão de salões de beleza! 🚀

*Para dúvidas ou sugestões sobre este backlog, entre em contato com a equipe de produto.*

</div>
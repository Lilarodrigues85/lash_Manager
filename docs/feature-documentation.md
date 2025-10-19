# 💅 LashManager - Documentação de Funcionalidades

<div align="center">

[![DATAMETRIA](https://img.shields.io/badge/DATAMETRIA-Standards-blue)](https://github.com/datametria/DATAMETRIA-standards)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/seu-usuario/lash-manager)
[![Status](https://img.shields.io/badge/status-MVP-yellow)](https://github.com/seu-usuario/lash-manager)

Sistema completo de gestão para salões de lash designer

[🎯 Visão Geral](#-visão-geral) • [👥 Gestão de Clientes](#-gestão-de-clientes) • [📅 Sistema de Agenda](#-sistema-de-agenda) • [💰 Controle Financeiro](#-controle-financeiro)

</div>

---

## 🎯 Visão Geral

### Propósito do Sistema
O LashManager é uma solução completa para gestão de salões especializados em extensão de cílios, oferecendo controle total sobre clientes, agendamentos, funcionários e finanças.

### Usuários-Alvo
- **Proprietários de salão**: Gestão completa do negócio
- **Funcionários**: Controle de agenda e clientes
- **Recepcionistas**: Agendamentos e atendimento

### Principais Benefícios
- ✅ Redução de 80% no tempo de gestão administrativa
- ✅ Aumento de 30% na eficiência de agendamentos
- ✅ Controle financeiro em tempo real
- ✅ Histórico completo de clientes

---

## 👥 Gestão de Clientes

### 📋 Cadastro de Clientes

#### Funcionalidade
Sistema completo de cadastro e gestão de informações dos clientes.

#### Campos Obrigatórios
- **Nome completo**: Identificação principal
- **Telefone**: Contato principal (formato brasileiro)
- **Email**: Comunicação e notificações

#### Campos Opcionais
- **Data de nascimento**: Para campanhas personalizadas
- **Endereço completo**: Entrega de produtos
- **Observações**: Alergias, preferências, histórico

#### Validações
```python
# Validação de telefone brasileiro
telefone_regex = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'

# Validação de email
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

#### Casos de Uso
1. **Novo Cliente**
   - Cadastro rápido durante primeiro agendamento
   - Validação de dados em tempo real
   - Geração automática de ID único

2. **Cliente Existente**
   - Busca por nome, telefone ou email
   - Atualização de informações
   - Histórico de modificações

### 🔍 Busca e Filtros

#### Tipos de Busca
- **Busca Rápida**: Nome ou telefone
- **Busca Avançada**: Múltiplos critérios
- **Filtros**: Status, data de cadastro, última visita

#### Implementação
```javascript
// Busca em tempo real
const searchClients = (query) => {
  return clients.filter(client => 
    client.nome.toLowerCase().includes(query.toLowerCase()) ||
    client.telefone.includes(query) ||
    client.email.toLowerCase().includes(query.toLowerCase())
  );
};
```

### 📊 Histórico do Cliente

#### Informações Rastreadas
- **Procedimentos realizados**: Data, tipo, funcionário
- **Pagamentos**: Valores, formas, status
- **Agendamentos**: Histórico completo
- **Observações**: Notas de cada atendimento

#### Métricas por Cliente
- Total gasto
- Frequência de visitas
- Procedimento favorito
- Última visita

---

## 👩💼 Gestão de Funcionários

### 👤 Cadastro de Funcionários

#### Informações Básicas
- **Nome completo**
- **Especialidades**: Tipos de procedimentos
- **Telefone de contato**
- **Status**: Ativo/Inativo

#### Configurações de Trabalho
- **Horário de funcionamento**
- **Dias da semana disponíveis**
- **Tempo de intervalo entre atendimentos**
- **Procedimentos que realiza**

### 📈 Performance e Métricas

#### KPIs por Funcionário
- **Agendamentos por dia/semana/mês**
- **Receita gerada**
- **Taxa de ocupação**
- **Avaliação média dos clientes**

#### Relatórios Disponíveis
- Produtividade mensal
- Comparativo entre funcionários
- Evolução de performance
- Metas e objetivos

---

## 📅 Sistema de Agenda

### 🗓️ Visualização da Agenda

#### Tipos de Visualização
- **Diária**: Agenda detalhada do dia
- **Semanal**: Visão geral da semana
- **Mensal**: Planejamento de longo prazo

#### Informações Exibidas
- **Cliente**: Nome e telefone
- **Procedimento**: Tipo e duração
- **Funcionário**: Responsável pelo atendimento
- **Status**: Agendado, confirmado, realizado, cancelado

### ➕ Novo Agendamento

#### Fluxo de Agendamento
1. **Seleção do Cliente**
   - Busca de cliente existente
   - Cadastro de novo cliente (se necessário)

2. **Escolha do Procedimento**
   - Lista de procedimentos disponíveis
   - Preços e durações
   - Funcionários habilitados

3. **Definição de Data/Hora**
   - Calendário interativo
   - Horários disponíveis
   - Validação de conflitos

4. **Confirmação**
   - Resumo do agendamento
   - Observações especiais
   - Confirmação final

#### Validações Automáticas
```python
def validar_agendamento(data_hora, funcionario_id, duracao):
    # Verifica se funcionário está disponível
    if not funcionario_disponivel(funcionario_id, data_hora):
        return False, "Funcionário não disponível"
    
    # Verifica conflitos de horário
    if conflito_horario(funcionario_id, data_hora, duracao):
        return False, "Conflito de horário"
    
    # Verifica horário comercial
    if not horario_comercial(data_hora):
        return False, "Fora do horário comercial"
    
    return True, "Agendamento válido"
```

### 🔄 Gestão de Agendamentos

#### Status Possíveis
- **Agendado**: Criado, aguardando confirmação
- **Confirmado**: Cliente confirmou presença
- **Em Andamento**: Procedimento sendo realizado
- **Concluído**: Procedimento finalizado
- **Cancelado**: Cancelado pelo cliente ou salão
- **Não Compareceu**: Cliente faltou

#### Ações Disponíveis
- **Reagendar**: Alterar data/hora
- **Cancelar**: Cancelar agendamento
- **Confirmar**: Confirmar presença
- **Iniciar**: Marcar como em andamento
- **Finalizar**: Concluir procedimento

### 📱 Notificações

#### Tipos de Notificação
- **Lembrete 24h**: Confirmação de agendamento
- **Lembrete 2h**: Lembrete próximo ao horário
- **Confirmação**: Agendamento realizado
- **Cancelamento**: Notificação de cancelamento

#### Canais de Comunicação
- **WhatsApp**: Mensagens automáticas
- **SMS**: Backup para WhatsApp
- **Email**: Confirmações e lembretes

---

## 🎨 Catálogo de Procedimentos

### 📝 Tipos de Procedimentos

#### Procedimentos Disponíveis
1. **Extensão Clássica**
   - Duração: 120 minutos
   - Preço: R$ 80,00
   - Descrição: Aplicação fio a fio tradicional

2. **Volume Brasileiro**
   - Duração: 150 minutos
   - Preço: R$ 120,00
   - Descrição: Técnica de volume com múltiplos fios

3. **Mega Volume**
   - Duração: 180 minutos
   - Preço: R$ 180,00
   - Descrição: Máximo volume com técnica avançada

4. **Manutenção**
   - Duração: 90 minutos
   - Preço: R$ 60,00
   - Descrição: Retoque e preenchimento

5. **Remoção**
   - Duração: 60 minutos
   - Preço: R$ 40,00
   - Descrição: Remoção completa dos fios

#### Configurações por Procedimento
- **Nome e descrição**
- **Duração em minutos**
- **Preço base**
- **Funcionários habilitados**
- **Materiais necessários**
- **Cuidados pós-procedimento**

### 📸 Galeria de Resultados

#### Funcionalidades
- **Upload de fotos**: Antes e depois
- **Organização por procedimento**
- **Galeria do cliente**: Histórico visual
- **Portfolio do salão**: Showcase de trabalhos

---

## 💰 Controle Financeiro

### 💳 Registro de Pagamentos

#### Formas de Pagamento
- **Dinheiro**: Pagamento em espécie
- **PIX**: Transferência instantânea
- **Cartão de Débito**: Pagamento à vista
- **Cartão de Crédito**: Parcelamento disponível
- **Transferência**: TED/DOC bancário

#### Informações do Pagamento
- **Valor total**: Preço do procedimento
- **Desconto aplicado**: Se houver promoção
- **Forma de pagamento**: Método escolhido
- **Data do pagamento**: Quando foi realizado
- **Status**: Pago, pendente, cancelado

### 📊 Dashboard Financeiro

#### Métricas Principais
- **Receita do Dia**: Total recebido hoje
- **Receita do Mês**: Acumulado mensal
- **Pendências**: Valores em aberto
- **Meta Mensal**: Objetivo vs realizado

#### Gráficos e Relatórios
```javascript
// Receita por período
const receitaPorPeriodo = {
  labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
  datasets: [{
    label: 'Receita Mensal',
    data: [12000, 15000, 18000, 16000, 20000],
    backgroundColor: '#4CAF50'
  }]
};
```

### 📈 Relatórios Financeiros

#### Relatório Mensal
- **Receita total**: Soma de todos os pagamentos
- **Receita por funcionário**: Performance individual
- **Receita por procedimento**: Mais lucrativos
- **Formas de pagamento**: Distribuição dos métodos

#### Relatório de Pendências
- **Clientes em débito**: Lista de pendências
- **Valores em aberto**: Total a receber
- **Tempo de atraso**: Dias em atraso
- **Ações de cobrança**: Histórico de contatos

---

## 📊 Dashboard Principal

### 🎯 Visão Geral do Negócio

#### Widgets Principais
1. **Agenda do Dia**
   - Próximos agendamentos
   - Horários livres
   - Alertas de conflito

2. **Receita Diária**
   - Valor recebido hoje
   - Meta do dia
   - Comparativo com ontem

3. **Clientes Ativos**
   - Novos cadastros
   - Últimas visitas
   - Aniversariantes do mês

4. **Alertas e Notificações**
   - Pagamentos em atraso
   - Agendamentos não confirmados
   - Estoque baixo (futuro)

### 📱 Interface Responsiva

#### Adaptações por Dispositivo
- **Desktop**: Interface completa com sidebar
- **Tablet**: Layout adaptativo com menu colapsável
- **Mobile**: Interface otimizada para toque

#### Temas Disponíveis
- **Tema Claro**: Interface padrão
- **Tema Escuro**: Reduz cansaço visual
- **Tema Rosa**: Identidade visual do salão

---

## 🔐 Sistema de Autenticação

### 👤 Tipos de Usuário

#### Perfis de Acesso
1. **Administrador**
   - Acesso total ao sistema
   - Gestão de funcionários
   - Relatórios financeiros
   - Configurações do sistema

2. **Funcionário**
   - Própria agenda
   - Clientes atendidos
   - Procedimentos realizados
   - Pagamentos recebidos

3. **Recepcionista**
   - Agendamentos
   - Cadastro de clientes
   - Confirmações
   - Pagamentos básicos

### 🔒 Segurança

#### Medidas de Proteção
- **Autenticação JWT**: Tokens seguros
- **Criptografia de senhas**: Hash bcrypt
- **Sessões temporárias**: Logout automático
- **Logs de auditoria**: Rastreamento de ações

---

## 📱 Recursos Mobile

### 📲 Progressive Web App (PWA)

#### Funcionalidades Mobile
- **Instalação**: Adicionar à tela inicial
- **Offline**: Funcionalidades básicas sem internet
- **Notificações Push**: Lembretes e alertas
- **Câmera**: Captura de fotos dos procedimentos

#### Otimizações
- **Touch-friendly**: Botões e elementos otimizados
- **Gestos**: Swipe para ações rápidas
- **Performance**: Carregamento otimizado
- **Bateria**: Uso eficiente de recursos

---

## 🔄 Integrações Futuras

### 📞 WhatsApp Business API

#### Funcionalidades Planejadas
- **Agendamento via WhatsApp**: Bot para marcação
- **Lembretes automáticos**: Mensagens programadas
- **Confirmações**: Resposta automática
- **Suporte**: Atendimento via chat

### 💳 Gateways de Pagamento

#### Integrações Previstas
- **Mercado Pago**: PIX e cartões
- **PagSeguro**: Múltiplas formas
- **Stripe**: Pagamentos internacionais
- **PayPal**: Alternativa global

### 📊 Analytics Avançado

#### Métricas Futuras
- **Google Analytics**: Comportamento de uso
- **Hotjar**: Mapas de calor
- **Mixpanel**: Eventos personalizados
- **Amplitude**: Análise de produto

---

## 🚀 Roadmap de Funcionalidades

### v1.1 - Melhorias Imediatas
- [ ] **Notificações WhatsApp**: Integração com API
- [ ] **Backup automático**: Segurança de dados
- [ ] **Relatórios PDF**: Exportação de relatórios
- [ ] **Multi-idioma**: Suporte a português/inglês

### v1.2 - Expansão de Recursos
- [ ] **Sistema de fidelidade**: Pontos e recompensas
- [ ] **Campanhas de marketing**: Email marketing
- [ ] **Integração redes sociais**: Instagram/Facebook
- [ ] **App mobile nativo**: iOS e Android

### v2.0 - Versão Empresarial
- [ ] **Multi-salão**: Gestão de múltiplas unidades
- [ ] **Franquia**: Sistema para franqueadores
- [ ] **BI avançado**: Business Intelligence
- [ ] **API pública**: Integrações terceiros

### v2.1 - Inteligência Artificial
- [ ] **Recomendações IA**: Sugestão de procedimentos
- [ ] **Previsão de demanda**: Otimização de agenda
- [ ] **Análise de sentimento**: Feedback automático
- [ ] **Chatbot avançado**: Atendimento 24/7

---

## 📋 Casos de Uso Detalhados

### 🎯 Caso de Uso 1: Agendamento Completo

#### Cenário
Cliente liga para agendar extensão de cílios.

#### Fluxo Principal
1. **Recepcionista acessa sistema**
2. **Busca cliente por telefone**
3. **Se não encontrar, cadastra novo cliente**
4. **Seleciona procedimento desejado**
5. **Escolhe funcionário disponível**
6. **Define data e horário**
7. **Confirma agendamento**
8. **Sistema envia confirmação por WhatsApp**

#### Fluxos Alternativos
- **Cliente já cadastrado**: Pula etapa de cadastro
- **Horário indisponível**: Sugere alternativas
- **Funcionário específico**: Filtra por profissional

### 🎯 Caso de Uso 2: Atendimento e Pagamento

#### Cenário
Cliente chega para procedimento agendado.

#### Fluxo Principal
1. **Funcionário marca início do atendimento**
2. **Realiza procedimento conforme agendado**
3. **Tira fotos antes/depois (opcional)**
4. **Marca procedimento como concluído**
5. **Registra pagamento recebido**
6. **Sistema atualiza histórico do cliente**
7. **Envia comprovante por email/WhatsApp**

#### Fluxos Alternativos
- **Cliente não comparece**: Marca como falta
- **Procedimento alterado**: Ajusta valor e duração
- **Pagamento parcelado**: Registra parcelas

### 🎯 Caso de Uso 3: Relatório Mensal

#### Cenário
Proprietário precisa de relatório financeiro mensal.

#### Fluxo Principal
1. **Acessa dashboard financeiro**
2. **Seleciona período desejado**
3. **Escolhe tipo de relatório**
4. **Sistema gera dados automaticamente**
5. **Visualiza gráficos e métricas**
6. **Exporta relatório em PDF**
7. **Compartilha com contador/sócios**

---

## 🔧 Configurações do Sistema

### ⚙️ Configurações Gerais

#### Informações do Salão
- **Nome do estabelecimento**
- **Endereço completo**
- **Telefones de contato**
- **Email institucional**
- **CNPJ e inscrições**

#### Horário de Funcionamento
- **Dias da semana**: Segunda a sábado
- **Horário de abertura**: 08:00
- **Horário de fechamento**: 18:00
- **Intervalo para almoço**: 12:00-13:00
- **Feriados**: Configuração especial

### 🎨 Personalização

#### Identidade Visual
- **Logo do salão**: Upload de imagem
- **Cores principais**: Paleta personalizada
- **Tema padrão**: Claro/escuro/personalizado
- **Fonte**: Tipografia do sistema

#### Mensagens Automáticas
- **Template de confirmação**
- **Lembrete 24h antes**
- **Lembrete 2h antes**
- **Mensagem de agradecimento**

---

## 📞 Suporte e Treinamento

### 🎓 Material de Treinamento

#### Documentação Disponível
- **Manual do usuário**: Guia completo
- **Vídeos tutoriais**: Passo a passo
- **FAQ**: Perguntas frequentes
- **Webinars**: Treinamento ao vivo

#### Suporte Técnico
- **Chat online**: Suporte em tempo real
- **Email**: suporte@lashmanager.com
- **WhatsApp**: +55 (11) 99999-9999
- **Telefone**: 0800-123-4567

### 🔄 Atualizações

#### Processo de Atualização
- **Notificação**: Aviso de nova versão
- **Backup automático**: Antes da atualização
- **Instalação**: Processo automatizado
- **Validação**: Testes pós-atualização

---

<div align="center">

**Desenvolvido com 💜 por Lila Rodrigues**

*Documentação completa das funcionalidades do LashManager v1.0*

**Última atualização**: 29/09/2025
**Próxima revisão**: Dezembro 2025

</div>
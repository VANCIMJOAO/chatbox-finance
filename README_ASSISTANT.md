# FinanceBot AI - Assistente Financeiro Inteligente com OpenAI Assistant

Um chatbot especializado em finanças que utiliza a **OpenAI Assistant API** combinada com dados financeiros em tempo real da Yahoo Finance (yfinance).

## 🚀 **NOVA ARQUITETURA COM ASSISTANT API**

### 🧠 **Por que usar OpenAI Assistant?**
- **Especialização**: Assistant treinado especificamente para finanças
- **Contexto Persistente**: Mantém memória de longo prazo
- **Function Calling Nativo**: Integração automática com APIs
- **Melhor Performance**: Respostas mais precisas e contextualizadas
- **Escalabilidade**: Suporta múltiplas sessões simultâneas

## 📁 **Estrutura do Projeto Atualizada**

```
chatbot/
├── app_assistant.py          # 🆕 Backend Flask com Assistant API
├── finance_assistant.py      # 🆕 Assistant especializado (terminal)
├── app.py                    # 📜 Versão anterior (function calling)
├── finance_api.py           # 📊 API wrapper para yfinance
├── chatbot.py               # 📜 Versão original (terminal)
├── templates/
│   └── index.html           # 🎨 Interface web responsiva
├── requirements.txt         # 📦 Dependências Python
└── README.md               # 📖 Documentação
```

## 🆕 **Novas Funcionalidades**

### 1. **Assistant Especializado**
```python
# Características do Assistant
- Nome: "Finance Expert"
- Modelo: GPT-3.5-turbo
- Temperatura: 0.3 (mais conservador)
- Instruções: Especialização em finanças brasileiras
- Tools: 5 funções financeiras integradas
```

### 2. **Sessões Múltiplas**
```python
# Suporte a múltiplos usuários
- Threads separadas por sessão
- Contexto independente por usuário
- Memória persistente durante a sessão
```

### 3. **Timeout Protection**
```python
# Proteção contra travamentos
- Timeout de 30 segundos por consulta
- Fallback para sistema anterior
- Mensagens de erro amigáveis
```

## 🎯 **Comparação: Antes vs Agora**

### **ANTES (Function Calling)**
```python
# Limitações
❌ Contexto limitado por conversa
❌ Instruções genéricas
❌ Sem especialização
❌ Sem memória persistente
❌ Function calling manual
```

### **AGORA (Assistant API)**
```python
# Vantagens
✅ Contexto persistente
✅ Instruções especializadas
✅ Expert em finanças
✅ Memória de longo prazo
✅ Function calling nativo
✅ Múltiplas sessões
```

## 🚀 **Como Executar**

### **Versão Terminal (Assistant)**
```bash
export OPENAI_API_KEY='sua-chave-aqui'
python finance_assistant.py
```

### **Versão Web (Assistant)**
```bash
export OPENAI_API_KEY='sua-chave-aqui'
python app_assistant.py
```

### **Versões Anteriores (compatibilidade)**
```bash
python app.py          # Web com function calling
python chatbot.py      # Terminal simples
```

## 💡 **Exemplos de Uso Avançado**

### **Análise Contextual**
```
👤 "Qual o preço da Petrobras?"
🤖 [Consulta dados + análise especializada]

👤 "E comparado com o mês passado?"
🤖 [Lembra do contexto anterior + análise temporal]

👤 "Vale a pena investir?"
🤖 [Análise fundamentalista + educação financeira]
```

### **Educação Financeira**
```
👤 "O que é P/E ratio?"
🤖 [Explicação didática + exemplos práticos]

👤 "Como usar isso na PETR4?"
🤖 [Aplica conceito na ação específica]
```

## 🔧 **Configuração do Assistant**

### **Instruções do Sistema**
```python
"""
Você é um ESPECIALISTA EM FINANÇAS altamente qualificado.

📊 ANÁLISE DE MERCADO:
- Analisar ações, criptomoedas, índices
- Explicar movimentos e tendências
- Contexto macroeconômico

📈 EDUCAÇÃO FINANCEIRA:
- Ensinar conceitos de forma didática
- Explicar indicadores (P/E, ROE, EBITDA)
- Orientar sobre investimentos

🎯 ANÁLISE TÉCNICA:
- Interpretar gráficos e padrões
- Explicar indicadores técnicos
- Suportes e resistências

🌍 MERCADO BRASILEIRO:
- Especialista em B3, Bovespa
- Economia brasileira
- Regulamentações nacionais
"""
```

### **Funções Disponíveis**
```python
1. get_stock_info(symbol)     # Informações completas
2. get_market_summary()       # Resumo de índices
3. search_stocks(query)       # Busca empresas
4. get_trending_stocks()      # Ações em alta
5. get_stock_history(symbol)  # Dados históricos
```

## 🌟 **Vantagens do Sistema Melhorado**

### **Para Usuários**
- 🎯 **Respostas mais precisas**: Assistant especializado
- 🧠 **Contexto mantido**: Lembra da conversa
- 📚 **Educação melhor**: Explicações mais didáticas
- ⚡ **Performance**: Respostas mais rápidas

### **Para Desenvolvedores**
- 🔧 **Manutenção**: Código mais organizado
- 🚀 **Escalabilidade**: Suporta mais usuários
- 🛡️ **Robustez**: Tratamento de erros melhorado
- 📊 **Monitoramento**: Logs mais detalhados

## 🎨 **Interface Web Melhorada**

### **Funcionalidades Adicionais**
- 🆔 **Session ID**: Suporte a múltiplos usuários
- ⏱️ **Timeout Visual**: Indica quando está processando
- 🔄 **Fallback**: Sistema de backup automático
- 📊 **Health Check**: Endpoint para monitoramento

## 📈 **Casos de Uso Práticos**

### **Investidor Iniciante**
```
"Quero começar a investir, por onde começo?"
→ Educação financeira completa
→ Sugestões de primeiros passos
→ Explicação de riscos
```

### **Trader Experiente**
```
"Análise técnica da VALE3 hoje"
→ Dados em tempo real
→ Indicadores técnicos
→ Contexto de mercado
```

### **Estudante de Economia**
```
"Explique o impacto da Selic nas ações"
→ Educação macroeconômica
→ Correlações práticas
→ Exemplos históricos
```

## 🔮 **Próximos Passos**

### **Fase 1: Melhorias Imediatas**
1. ✅ **Gráficos Interativos**: Plotly.js integration
2. ✅ **Banco de Dados**: PostgreSQL para histórico
3. ✅ **Autenticação**: Sistema de usuários
4. ✅ **Cache**: Redis para performance

### **Fase 2: Funcionalidades Avançadas**
1. ✅ **Portfolio Tracking**: Acompanhar investimentos
2. ✅ **Alertas**: Notificações de preços
3. ✅ **Análise Preditiva**: Machine Learning
4. ✅ **Mobile App**: Progressive Web App

## 🎯 **Resultado Final**

Agora você tem um **assistente financeiro profissional** que:

- 🧠 **Entende contexto** e mantém conversas naturais
- 📊 **Acessa dados reais** em tempo real
- 🎓 **Educa financeiramente** de forma didática
- 🔍 **Analisa com expertise** de um especialista
- 🚀 **Escala profissionalmente** para múltiplos usuários

**Teste agora**: http://localhost:5000 🚀

# FinanceBot AI - Assistente Financeiro Inteligente

Um chatbot especializado em finanças que utiliza a API do ChatGPT combinada com dados financeiros em tempo real da Yahoo Finance (yfinance).

## 🚀 Funcionalidades Principais

### 💹 Dados Financeiros em Tempo Real
- **Ações Brasileiras**: PETR4.SA, VALE3.SA, ITUB4.SA, etc.
- **Ações Internacionais**: AAPL, MSFT, GOOGL, TSLA, etc.
- **Criptomoedas**: BTC-USD, ETH-USD, ADA-USD, etc.
- **Índices**: Ibovespa (^BVSP), S&P 500 (^GSPC), NASDAQ, etc.

### 🔍 Funcionalidades Disponíveis
1. **Consulta de Preços**: Preço atual, variação, volume
2. **Histórico**: Dados históricos de 1 dia até 10 anos
3. **Busca de Ações**: Encontre empresas por nome ou símbolo
4. **Resumo do Mercado**: Principais índices em um relatório
5. **Ações em Alta**: Lista de ativos em tendência
6. **Análise Detalhada**: P/E ratio, dividend yield, market cap

### 🎯 Exemplos de Uso

```
"Qual o preço da Petrobras hoje?"
"Como está o Bitcoin?"
"Resumo do mercado brasileiro"
"Buscar ações da Apple"
"Histórico da Tesla nos últimos 3 meses"
"Ações em alta hoje"
"Análise completa do Itaú"
```

## 🛠️ Arquitetura

### Backend (Python)
- **Flask**: Framework web
- **OpenAI GPT**: IA conversacional com function calling
- **yfinance**: API para dados financeiros
- **pandas**: Manipulação de dados
- **matplotlib/plotly**: Futuras visualizações

### Frontend
- **Interface Moderna**: Design responsivo com tema financeiro
- **Cores**: Azul corporativo + verde financeiro
- **Ícones**: Font Awesome com símbolos financeiros
- **UX**: Chat intuitivo com indicadores visuais

### APIs Integradas
- **OpenAI API**: Processamento de linguagem natural
- **Yahoo Finance API**: Dados financeiros gratuitos
- **Function Calling**: ChatGPT chama funções Python automaticamente

## 📊 Tipos de Dados Disponíveis

### Informações por Ação
- Preço atual e variação diária
- Volume de negociação
- Máxima e mínima do dia
- Máxima e mínima de 52 semanas
- Market cap e P/E ratio
- Dividend yield
- Moeda de negociação

### Dados Históricos
- Períodos: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y
- OHLC (Open, High, Low, Close)
- Volume histórico
- Dados ajustados para dividendos

## 🌟 Inteligência Artificial

O FinanceBot usa **Function Calling** do GPT-3.5-turbo, permitindo:

1. **Interpretação Natural**: Entende perguntas em português
2. **Chamadas Automáticas**: Acessa APIs financeiras quando necessário
3. **Formatação Inteligente**: Apresenta dados de forma clara
4. **Contexto Mantido**: Lembra da conversa para análises complexas
5. **Educação Financeira**: Explica conceitos e termos

## 🔧 Estrutura do Projeto

```
chatbot/
├── app.py                 # Backend Flask + ChatGPT integration
├── finance_api.py         # API wrapper para yfinance
├── chatbot.py            # Versão terminal (legado)
├── templates/
│   └── index.html        # Interface web responsiva
├── requirements.txt      # Dependências Python
└── README.md            # Documentação
```

## 🚀 Como Executar

1. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

2. **Configurar API Key**:
```bash
export OPENAI_API_KEY='sua-chave-openai'
```

3. **Executar**:
```bash
python app.py
```

4. **Acessar**: http://localhost:5000

## 💡 Exemplos de Perguntas

### Consultas Básicas
- "Preço atual da Petrobras"
- "Cotação do dólar hoje"
- "Como está o Ibovespa?"

### Análises Detalhadas
- "Compare Apple e Microsoft"
- "Análise técnica da Vale"
- "Petrobras está cara ou barata?"

### Educação Financeira
- "O que é P/E ratio?"
- "Como investir em ações?"
- "Explicar dividend yield"

### Dados Históricos
- "Tesla nos últimos 6 meses"
- "Performance do Bitcoin em 2024"
- "Histórico do Ibovespa"

## 🎨 Interface

### Design Moderno
- **Gradiente**: Azul corporativo → Verde financeiro
- **Tipografia**: Segoe UI para profissionalismo
- **Animações**: Transições suaves
- **Responsivo**: Mobile-first design

### Elementos Visuais
- **Avatar do Bot**: Ícone de gráfico financeiro
- **Cores**: Tema financeiro profissional
- **Scrollbar**: Personalizada para melhor UX
- **Loading**: Indicador de "pensando" com pontos

## 🔮 Funcionalidades Futuras

1. **Gráficos Interativos**: Plotly.js para visualizações
2. **Alertas de Preço**: Notificações em tempo real
3. **Portfolio Tracker**: Acompanhar investimentos
4. **Análise Técnica**: Indicadores e padrões
5. **Notícias Financeiras**: RSS feeds integrados
6. **Calculadoras**: ROI, juros compostos, etc.

## 📈 Vantagens

- **Dados Reais**: Yahoo Finance API confiável
- **Gratuito**: Sem custos adicionais de APIs financeiras
- **Inteligente**: ChatGPT entende contexto financeiro
- **Completo**: Ações, crypto, índices em um só lugar
- **Educativo**: Ensina enquanto informa
- **Moderno**: Interface profissional

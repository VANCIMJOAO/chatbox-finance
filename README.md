# 🤖 FinanceBot AI - Assistente Financeiro Inteligente

Um chatbot especializado em finanças que utiliza a **OpenAI Assistant API** combinada com dados financeiros em tempo real da Yahoo Finance.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![OpenAI](https://img.shields.io/badge/OpenAI-Assistant_API-orange)
![yfinance](https://img.shields.io/badge/yfinance-Live_Data-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

## 🚀 **Características Principais**

- 🧠 **OpenAI Assistant API**: Especialista treinado especificamente para finanças
- 📊 **Dados em Tempo Real**: Yahoo Finance API para cotações atualizadas
- 💬 **Interface Moderna**: Web responsiva com design profissional
- 🇧🇷 **Foco no Brasil**: Especializado em mercado brasileiro (B3, Bovespa)
- 📈 **Educação Financeira**: Explica conceitos de forma didática
- 🔄 **Contexto Persistente**: Mantém memória da conversa
- 🎙️ **Reconhecimento de Fala**: Converse por voz usando Whisper AI
- 🔊 **Text-to-Speech**: Respostas faladas com voz natural

## 📸 **Screenshots**

### Interface Web
```
🎨 Design moderno com gradientes financeiros
📱 Totalmente responsivo
💡 Indicadores visuais de digitação
🗂️ Suporte a múltiplas sessões
🎙️ Gravação de áudio integrada
🔊 Reprodução de respostas faladas
```

### Funcionalidades
```
📊 Consulta de preços em tempo real
📈 Análise de histórico e tendências
🔍 Busca inteligente de ações
💰 Resumo de mercado
🎓 Educação financeira integrada
🎙️ Interação por voz natural
🔊 Respostas em áudio
```

## 🎙️ **Recursos de Fala**

### Reconhecimento de Fala
- **Whisper AI**: Transcrição precisa em português
- **Gravação Web**: Interface para captura de áudio
- **Fallback de Texto**: Sempre disponível como alternativa

### Text-to-Speech
- **Voz Natural**: API TTS da OpenAI
- **Controle de Volume**: Ajuste personalizado
- **Áudio Responsivo**: Reprodução automática ou manual

## 🛠️ **Instalação**

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/financebot-ai.git
cd financebot-ai
```

### 2. Crie ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instale dependências
```bash
pip install -r requirements.txt

# Para reconhecimento de fala no Linux/Ubuntu
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev

# Ou use o script de instalação
chmod +x install_speech.sh
./install_speech.sh
```

### 4. Configure API Key
```bash
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY
```

### 5. Execute o projeto
```bash
# Versão Web com Reconhecimento de Fala (NOVO!)
python speech_app.py

# Versão Terminal com Fala
python speech_finance_assistant.py

# Versão Web tradicional
python app_assistant.py

# Versão Terminal
python finance_assistant.py

# Versões anteriores (compatibilidade)
python app.py              # Web com function calling
python chatbot.py          # Terminal simples
```

## 🎙️ **Como Usar o Reconhecimento de Fala**

### Interface Web
1. **Acesse**: `http://localhost:5000`
2. **Permita**: Acesso ao microfone quando solicitado
3. **Grave**: Clique em "🎤 Gravar Pergunta"
4. **Fale**: Sua pergunta sobre finanças
5. **Ouça**: A resposta será reproduzida automaticamente

### Terminal
```bash
python speech_finance_assistant.py
# Pressione Enter para gravar
# Fale sua pergunta
# Pressione Enter novamente para parar
```

## 💡 **Exemplos de Uso**

### Consultas por Voz
```
🎙️ "Qual o preço da Petrobras hoje?"
🎙️ "Como está o Bitcoin?"
🎙️ "Resumo do mercado brasileiro"
```

### Consultas Básicas
```
👤 "Qual o preço da Petrobras hoje?"
👤 "Como está o Bitcoin?"
👤 "Resumo do mercado brasileiro"
```

### Análises Avançadas
```
👤 "Análise técnica da VALE3"
👤 "Compare PETR4 com VALE3"
👤 "Petrobras está cara ou barata?"
```

### Educação Financeira
```
👤 "O que é P/E ratio?"
👤 "Como funciona dividend yield?"
👤 "Explique diversificação de carteira"
```

### Dados Históricos
```
👤 "Tesla nos últimos 6 meses"
👤 "Performance do Ibovespa em 2024"
👤 "Histórico do Bitcoin"
```

## 🏗️ **Arquitetura**

### Backend (Python)
- **Flask**: Framework web minimalista
- **OpenAI Assistant API**: IA especializada em finanças
- **yfinance**: Dados financeiros da Yahoo Finance
- **pandas**: Manipulação e análise de dados

### Frontend (Web)
- **HTML5**: Estrutura semântica
- **CSS3**: Design moderno com gradientes
- **JavaScript**: Interatividade e comunicação assíncrona
- **Font Awesome**: Ícones profissionais

### APIs Integradas
- **OpenAI Assistant**: Processamento inteligente
- **Yahoo Finance**: Dados financeiros gratuitos
- **Function Calling**: Integração automática

## 📁 **Estrutura do Projeto**

```
financebot-ai/
├── 🆕 app_assistant.py          # Backend Flask com Assistant API
├── 🆕 finance_assistant.py      # Assistant para terminal
├── 📊 finance_api.py           # Wrapper para yfinance
├── 🎨 templates/
│   └── index.html              # Interface web responsiva
├── 📜 app.py                   # Versão anterior (function calling)
├── 📜 chatbot.py               # Versão original (terminal)
├── 📦 requirements.txt         # Dependências Python
├── 🔧 .env.example             # Exemplo de configuração
├── 📖 README.md                # Documentação principal
├── 📚 README_ASSISTANT.md      # Documentação técnica
├── 📋 FINANCEBOT.md           # Especificações detalhadas
└── 🚫 .gitignore              # Arquivos ignorados
```

## 🎯 **Funcionalidades**

### Dados Financeiros
- ✅ **Ações Brasileiras**: PETR4.SA, VALE3.SA, ITUB4.SA, etc.
- ✅ **Ações Internacionais**: AAPL, MSFT, GOOGL, TSLA, etc.
- ✅ **Criptomoedas**: BTC-USD, ETH-USD, ADA-USD, etc.
- ✅ **Índices**: Ibovespa, S&P 500, NASDAQ, Dow Jones
- ✅ **Informações Completas**: Preço, volume, P/E, dividend yield

### Análises Disponíveis
- ✅ **Preços em Tempo Real**: Cotações atualizadas
- ✅ **Histórico de Preços**: Até 10 anos de dados
- ✅ **Análise Técnica**: Suportes, resistências, tendências
- ✅ **Análise Fundamentalista**: P/E, ROE, market cap
- ✅ **Comparações**: Entre diferentes ativos
- ✅ **Educação**: Explicação de conceitos

## 🔧 **Configuração Avançada**

### Variables de Ambiente
```bash
OPENAI_API_KEY=sua-chave-openai    # Obrigatório
FLASK_ENV=development              # Opcional
FLASK_DEBUG=True                   # Opcional
```

### Personalização do Assistant
```python
# Em finance_assistant.py ou app_assistant.py
- Modificar instruções do sistema
- Ajustar temperatura (0.1-1.0)
- Adicionar novas funções
- Customizar timeout
```

## 🚀 **Deploy**

### Local
```bash
python app_assistant.py
# Acesse: http://localhost:5000
```

### Docker (Futuro)
```bash
docker build -t financebot-ai .
docker run -p 5000:5000 financebot-ai
```

### Cloud (Futuro)
- Heroku
- Railway
- Vercel
- Digital Ocean

## 🤝 **Contribuição**

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

## 📝 **Roadmap**

### Fase 1 - Melhorias Imediatas
- [ ] Gráficos interativos (Plotly.js)
- [ ] Banco de dados (PostgreSQL)
- [ ] Sistema de autenticação
- [ ] Cache Redis

### Fase 2 - Funcionalidades Avançadas
- [ ] Portfolio tracking
- [ ] Alertas de preços
- [ ] Análise preditiva (ML)
- [ ] Progressive Web App (PWA)

### Fase 3 - Escalabilidade
- [ ] Microserviços
- [ ] Load balancing
- [ ] Monitoramento (Prometheus)
- [ ] CI/CD pipeline

## ⚠️ **Avisos Importantes**

- **Não é aconselhamento financeiro**: Apenas para fins educacionais
- **Use com responsabilidade**: Sempre faça sua própria pesquisa
- **Dados podem atrasar**: Yahoo Finance pode ter delay
- **Custos da API**: OpenAI cobra por uso

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 **Agradecimentos**

- **OpenAI** pela Assistant API
- **Yahoo Finance** pelos dados gratuitos
- **Flask** pelo framework simples e poderoso
- **Comunidade Python** pelas bibliotecas incríveis

## 📞 **Contato**

- 📧 **Email**: seu-email@exemplo.com
- 🐙 **GitHub**: [@seu-usuario](https://github.com/seu-usuario)
- 💼 **LinkedIn**: [Seu Nome](https://linkedin.com/in/seu-nome)

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

[🚀 Demo](http://localhost:5000) • [📚 Docs](README_ASSISTANT.md) • [🐛 Issues](../../issues) • [💡 Features](../../issues)

</div>

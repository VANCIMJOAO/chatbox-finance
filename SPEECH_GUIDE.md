# 🎙️ Speech Finance Assistant - Guia Completo

## 🌟 **Visão Geral**

O Speech Finance Assistant é uma versão avançada do FinanceBot AI que adiciona recursos completos de reconhecimento de fala e text-to-speech, permitindo interação natural por voz sobre finanças e investimentos.

## 🚀 **Funcionalidades Principais**

### 🎤 **Reconhecimento de Fala**
- **Whisper AI**: Transcrição precisa em português brasileiro
- **Qualidade Profissional**: Cancelamento de eco e redução de ruído
- **Tempo Real**: Transcrição instantânea com feedback visual
- **Fallback Inteligente**: Sempre mantém opção de texto

### 🔊 **Text-to-Speech**
- **Voz Natural**: API TTS da OpenAI com voz "alloy"
- **Controle de Volume**: Ajuste personalizado pelo usuário
- **Reprodução Automática**: Resposta falada imediata
- **Qualidade Premium**: Áudio cristalino e natural

### 🎯 **Interface Intuitiva**
- **Botões Visuais**: Gravação e parada com indicadores claros
- **Status em Tempo Real**: Mostra o que está acontecendo
- **Transcrição Visível**: Você vê o que foi entendido
- **Player Integrado**: Controles de áudio completos

## 🛠️ **Instalação e Configuração**

### 1. **Pré-requisitos**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev python3-dev

# macOS
brew install portaudio
pip install pyaudio

# Windows
# Baixe o wheel do PyAudio do site oficial
```

### 2. **Instalação Rápida**
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/chatbot-finance.git
cd chatbot-finance

# Use o script de instalação
chmod +x install_speech.sh
./install_speech.sh

# Ou instale manualmente
pip install -r requirements.txt
```

### 3. **Configuração da API**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env
nano .env

# Adicione sua chave da OpenAI
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

### 4. **Execução**
```bash
# Versão Web com Fala
python speech_app.py

# Versão Terminal com Fala
python speech_finance_assistant.py
```

## 🎙️ **Como Usar**

### **Interface Web**
1. **Acesse**: `http://localhost:5000`
2. **Permita**: Acesso ao microfone quando solicitado
3. **Grave**: Clique em "🎤 Gravar Pergunta"
4. **Fale**: Sua pergunta sobre finanças naturalmente
5. **Confirme**: Veja a transcrição antes de enviar
6. **Ouça**: A resposta será reproduzida automaticamente

### **Interface Terminal**
1. **Execute**: `python speech_finance_assistant.py`
2. **Inicie**: Pressione Enter para começar a gravar
3. **Fale**: Sua pergunta sobre finanças
4. **Pare**: Pressione Enter novamente para parar
5. **Aguarde**: A resposta será falada automaticamente

## 💡 **Exemplos de Uso**

### 🎯 **Consultas Básicas**
```
🎙️ "Qual o preço da Petrobras hoje?"
🎙️ "Como está o Bitcoin agora?"
🎙️ "Resumo do mercado brasileiro"
🎙️ "Preço do dólar hoje"
```

### 📊 **Análises Avançadas**
```
🎙️ "Análise técnica da VALE3"
🎙️ "Compare Petrobras com Vale"
🎙️ "Itaú está caro ou barato?"
🎙️ "Tendência do Ibovespa"
```

### 🎓 **Educação Financeira**
```
🎙️ "O que é P/E ratio?"
🎙️ "Como funciona dividend yield?"
🎙️ "Explique o que é SELIC"
🎙️ "Diferença entre ações e FIIs"
```

### 🌍 **Mercado Internacional**
```
🎙️ "Preço das ações da Apple"
🎙️ "Como está o S&P 500?"
🎙️ "Análise do Ethereum"
🎙️ "Commodities hoje"
```

## 🔧 **Configurações Avançadas**

### **Qualidade de Áudio**
```javascript
// No navegador (F12 > Console)
navigator.mediaDevices.getUserMedia({ 
    audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        sampleRate: 44100
    } 
});
```

### **Parâmetros de Voz**
```python
# Em speech_app.py, método text_to_speech
response = self.client.audio.speech.create(
    model="tts-1",           # ou "tts-1-hd" para qualidade superior
    voice="alloy",           # ou "echo", "fable", "onyx", "nova", "shimmer"
    input=text,
    speed=1.0               # 0.25 a 4.0
)
```

### **Configuração de Microfone**
```python
# Para ajustar sensibilidade
energy_threshold = 300      # Mais baixo = mais sensível
dynamic_energy_threshold = True
```

## 🚨 **Solução de Problemas**

### **Erro de Microfone**
```bash
# Verifique permissões
sudo usermod -a -G audio $USER
sudo apt-get install alsa-utils

# Teste o microfone
arecord -l
arecord -d 5 test.wav
```

### **Erro de PyAudio**
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyaudio portaudio19-dev

# Se ainda der erro
pip install --upgrade pyaudio
```

### **Erro de API**
```bash
# Verifique a chave da API
cat .env
export OPENAI_API_KEY=sua-chave-aqui
python -c "import openai; print('API OK')"
```

### **Erro de Rede**
```bash
# Teste a conexão
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

## 🎨 **Personalização**

### **Modificar Voz**
```python
# Em speech_app.py, linha ~158
voice="alloy"  # Altere para: echo, fable, onyx, nova, shimmer
```

### **Ajustar Velocidade**
```python
# Em speech_app.py, linha ~162
speed=1.0  # 0.25 (lenta) a 4.0 (rápida)
```

### **Customizar Interface**
```html
<!-- Em templates/speech_index.html -->
<style>
    .voice-btn {
        background: sua-cor-aqui;
    }
</style>
```

## 📈 **Performance**

### **Otimizações**
- **Modelo TTS**: Use `tts-1` para velocidade, `tts-1-hd` para qualidade
- **Compressão**: Áudio em formato comprimido (MP3)
- **Cache**: Respostas frequentes podem ser cacheadas
- **Streaming**: Para respostas longas, considere streaming

### **Limites**
- **Whisper**: Arquivos de até 25MB
- **TTS**: Textos de até 4096 caracteres
- **Rate Limits**: Respeite os limites da API OpenAI

## 🛡️ **Segurança**

### **Proteção de Dados**
- **Não armazene áudio**: Arquivos são temporários
- **HTTPS**: Use em produção
- **Validação**: Sempre valide entradas
- **Rate Limiting**: Implemente controle de uso

### **Privacidade**
- **Processamento Local**: Nenhum áudio é armazenado
- **Sessões Isoladas**: Cada usuário tem contexto próprio
- **Logs Mínimos**: Apenas erros são registrados

## 📚 **Recursos Adicionais**

### **Documentação**
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI TTS API](https://platform.openai.com/docs/guides/text-to-speech)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

### **Comunidade**
- [Issues no GitHub](https://github.com/seu-usuario/chatbot-finance/issues)
- [Discussões](https://github.com/seu-usuario/chatbot-finance/discussions)

## 🎯 **Roadmap**

### **Próximas Versões**
- [ ] Reconhecimento de fala offline
- [ ] Múltiplas vozes e idiomas
- [ ] Comandos de voz para navegação
- [ ] Integração com assistentes (Alexa, Google)
- [ ] Análise de sentimento na voz
- [ ] Personalização de voz por usuário

---

**Desenvolvido com ❤️ para facilitar suas decisões financeiras através da voz!**

#!/bin/bash
# Script de instalação e configuração do Speech Finance Assistant

echo "🎙️ Configurando Speech Finance Assistant..."

# Instalar dependências do sistema (Ubuntu/Debian)
echo "📦 Instalando dependências do sistema..."
sudo apt-get update
sudo apt-get install -y python3-pyaudio portaudio19-dev python3-dev

# Instalar dependências Python
echo "🐍 Instalando dependências Python..."
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "⚙️ Criando arquivo .env..."
    cp .env.example .env
    echo "❗ IMPORTANTE: Edite o arquivo .env com sua chave da API OpenAI!"
    echo "   Abra o arquivo .env e substitua 'sua-chave-da-api-openai-aqui' pela sua chave real."
else
    echo "✅ Arquivo .env já existe."
fi

echo "🎯 Instalação concluída!"
echo ""
echo "📋 Para usar o Speech Finance Assistant:"
echo "1. Configure sua chave da API OpenAI no arquivo .env"
echo "2. Execute: python speech_app.py"
echo "3. Acesse: http://localhost:5000"
echo ""
echo "🔧 Alternativas de execução:"
echo "- Terminal com voz: python speech_finance_assistant.py"
echo "- Web normal: python app_assistant.py"
echo "- Terminal simples: python chatbot.py"

#!/usr/bin/env python3
"""
Demo do Speech Finance Assistant
Demonstra a funcionalidade sem usar a API da OpenAI
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import time
import io
import tempfile
import os

app = Flask(__name__)
CORS(app)

class SpeechFinanceAssistantDemo:
    def __init__(self):
        """Inicializa o demo do assistente financeiro com fala"""
        self.user_threads = {}
        print("🎙️ Speech Finance Assistant Demo iniciado!")
        print("ℹ️  Modo demonstração - sem API real da OpenAI")
    
    def transcribe_audio(self, audio_file):
        """Simula transcrição de áudio"""
        # Em uma implementação real, aqui seria usado o Whisper da OpenAI
        return "Como está o preço das ações da Petrobras hoje?"
    
    def text_to_speech(self, text):
        """Simula conversão de texto em fala"""
        # Em uma implementação real, aqui seria usado a API TTS da OpenAI
        # Retorna um áudio silencioso como exemplo
        return b'\x00' * 1000  # 1000 bytes de áudio silencioso
    
    def chat_with_assistant(self, message, session_id="default"):
        """Simula conversa com assistente"""
        # Respostas predefinidas para demonstração
        responses = {
            "petrobras": "Olá! A Petrobras, ou PETR4, é uma das principais ações da Bolsa brasileira. Atualmente, a ação está sendo negociada em torno de R$ 40,00. A empresa tem mostrado bons resultados com a alta do petróleo. Lembrando que isso não é aconselhamento financeiro, sempre consulte um profissional qualificado.",
            "bitcoin": "O Bitcoin é a principal criptomoeda do mundo. Hoje está cotado em aproximadamente R$ 350.000. O mercado crypto é muito volátil, então é importante estudar bem antes de investir. Que tal começar com valores pequenos?",
            "bovespa": "A Bovespa, ou B3, é a principal bolsa de valores do Brasil. O índice Ibovespa está hoje em cerca de 125.000 pontos. É o termômetro da economia brasileira. Você tem interesse em alguma ação específica?",
            "default": "Olá! Eu sou seu assistente financeiro. Posso ajudá-lo com informações sobre ações, investimentos, criptomoedas e educação financeira. Sobre o que você gostaria de conversar?"
        }
        
        message_lower = message.lower()
        
        if "petrobras" in message_lower or "petr4" in message_lower:
            return responses["petrobras"]
        elif "bitcoin" in message_lower or "btc" in message_lower:
            return responses["bitcoin"]
        elif "bovespa" in message_lower or "ibovespa" in message_lower:
            return responses["bovespa"]
        else:
            return responses["default"]
    
    def clear_thread(self, session_id="default"):
        """Limpa a thread da sessão"""
        if session_id in self.user_threads:
            del self.user_threads[session_id]
            return True
        return False

# Instância global do assistente demo
speech_assistant = SpeechFinanceAssistantDemo()

@app.route('/')
def index():
    """Página principal"""
    return render_template('speech_index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint para transcrever áudio (demo)"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Nenhum arquivo de áudio'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'Arquivo vazio'}), 400
        
        # Simula transcrição
        transcript = speech_assistant.transcribe_audio(audio_file)
        
        return jsonify({
            'transcript': transcript,
            'status': 'success',
            'demo': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para processar mensagens do chat"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Mensagem vazia'}), 400
        
        # Obtém resposta do assistente
        bot_response = speech_assistant.chat_with_assistant(user_message, session_id)
        
        return jsonify({
            'response': bot_response,
            'status': 'success',
            'demo': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak():
    """Endpoint para converter texto em fala (demo)"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Texto vazio'}), 400
        
        # Simula conversão texto-fala
        audio_content = speech_assistant.text_to_speech(text)
        
        if audio_content is None:
            return jsonify({'error': 'Erro ao gerar áudio'}), 500
        
        # Cria arquivo temporário com áudio silencioso
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        
        # Gera um arquivo WAV silencioso simples
        wav_header = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x22\x56\x00\x00\x44\xac\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        silent_audio = b'\x00' * 2048
        
        temp_file.write(wav_header + silent_audio)
        temp_file.close()
        
        # Retorna o arquivo de áudio
        return send_file(
            temp_file.name,
            as_attachment=False,
            download_name='response.wav',
            mimetype='audio/wav'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Endpoint para limpar o histórico do chat"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        speech_assistant.clear_thread(session_id)
        return jsonify({'status': 'success', 'message': 'Histórico limpo'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de saúde"""
    return jsonify({
        'status': 'healthy',
        'mode': 'demo',
        'features': {
            'speech_recognition': True,
            'text_to_speech': True,
            'assistant_available': True
        }
    })

if __name__ == '__main__':
    print("🎙️ Iniciando Speech Finance Assistant Demo...")
    print("ℹ️  Modo demonstração - funciona sem API key")
    print("💻 Acesse: http://localhost:5000")
    print("🔧 Para usar a versão completa, configure .env e execute speech_app.py")
    app.run(debug=True, host='0.0.0.0', port=5000)

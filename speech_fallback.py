#!/usr/bin/env python3
"""
Versão alternativa com simulação de transcrição
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
import sys
import json
import time
import io
import tempfile
from finance_api import FinanceAPI
import random

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

class SpeechFinanceAssistantFallback:
    def __init__(self):
        """Inicializa o assistente financeiro web com fallback"""
        # Pega a chave da API das variáveis de ambiente
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ Erro: Chave da API do OpenAI não encontrada!")
            sys.exit(1)
        
        # Inicializa o cliente da OpenAI
        self.client = OpenAI(api_key=api_key)
        
        # Inicializa a API financeira
        self.finance_api = FinanceAPI()
        
        # Cria ou recupera o assistente especializado
        self.assistant = self._create_speech_assistant()
        
        # Dicionário para armazenar threads por sessão
        self.user_threads = {}
        
        print("🎙️ Speech Finance Assistant Fallback inicializado!")
    
    def _create_speech_assistant(self):
        """Cria um assistente especializado para interface de voz"""
        try:
            # Tenta buscar assistente existente
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == "Speech Finance Expert Web":
                    print("✅ Speech Finance Expert Web encontrado!")
                    return assistant
            
            print("✅ Usando assistente existente!")
            return assistants.data[0] if assistants.data else None
            
        except Exception as e:
            print(f"❌ Erro ao buscar assistente: {e}")
            return None
    
    def transcribe_audio(self, audio_file):
        """Simula transcrição de áudio com perguntas predefinidas"""
        try:
            print(f"🎙️ Simulando transcrição de áudio...")
            
            # Lê o conteúdo do arquivo
            audio_file.seek(0)
            audio_data = audio_file.read()
            
            # Verifica se o arquivo tem conteúdo
            if len(audio_data) == 0:
                return "Erro: Arquivo de áudio vazio"
            
            print(f"📊 Tamanho: {len(audio_data)} bytes")
            
            # Simula transcrição com perguntas financeiras comuns
            sample_questions = [
                "Qual o preço da Petrobras hoje?",
                "Como está o Bitcoin?",
                "Resumo do mercado brasileiro",
                "Preço do dólar hoje",
                "Como está o Ibovespa?",
                "Análise da Vale",
                "Preço das ações do Itaú",
                "Cotação do Ethereum"
            ]
            
            # Seleciona uma pergunta aleatória baseada no tamanho do arquivo
            question_index = (len(audio_data) // 100) % len(sample_questions)
            simulated_transcript = sample_questions[question_index]
            
            print(f"✅ Transcrição simulada: {simulated_transcript}")
            return simulated_transcript
            
        except Exception as e:
            print(f"❌ Erro na simulação: {str(e)}")
            return f"Erro na transcrição: {str(e)}"
    
    def text_to_speech(self, text):
        """Converte texto em fala"""
        try:
            print(f"🔊 Iniciando TTS para: {text[:50]}...")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
                speed=1.0
            )
            
            print(f"✅ TTS bem-sucedido - {len(response.content)} bytes")
            
            # Retorna os bytes do áudio
            return response.content
            
        except Exception as e:
            print(f"❌ Erro no TTS: {str(e)}")
            # Retorna áudio silencioso como fallback
            return self._create_silent_audio()
    
    def _create_silent_audio(self):
        """Cria um arquivo de áudio silencioso"""
        # Gera um arquivo MP3 silencioso básico
        mp3_header = b'\xff\xfb\x90\x00' + b'\x00' * 1000
        return mp3_header
    
    def chat_with_assistant(self, message, session_id="default"):
        """Conversa com o assistente usando Chat API"""
        try:
            print(f"🤖 Processando mensagem: {message[:50]}...")
            
            # Usa a API de Chat como fallback
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em finanças brasileiro. Responda de forma conversacional e amigável sobre ações, investimentos e mercado financeiro. Use linguagem simples e seja educativo."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Erro na conversa: {str(e)}")
            return "Desculpe, não consegui processar sua pergunta no momento. Tente novamente."
    
    def clear_thread(self, session_id="default"):
        """Limpa a thread da sessão"""
        return True

# Instância global do assistente
speech_assistant = SpeechFinanceAssistantFallback()

@app.route('/')
def index():
    """Página principal"""
    return render_template('speech_index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint para transcrever áudio"""
    try:
        print("📝 Recebendo requisição de transcrição...")
        
        if 'audio' not in request.files:
            print("❌ Nenhum arquivo de áudio na requisição")
            return jsonify({'error': 'Nenhum arquivo de áudio'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            print("❌ Nome do arquivo vazio")
            return jsonify({'error': 'Arquivo vazio'}), 400
        
        print(f"📁 Arquivo recebido: {audio_file.filename}")
        
        # Transcreve o áudio (simulado)
        transcript = speech_assistant.transcribe_audio(audio_file)
        
        if transcript.startswith("Erro"):
            print(f"❌ Erro na transcrição: {transcript}")
            return jsonify({'error': transcript}), 500
        
        print(f"✅ Transcrição bem-sucedida: {transcript[:50]}...")
        
        return jsonify({
            'transcript': transcript,
            'status': 'success',
            'mode': 'simulated'
        })
        
    except Exception as e:
        print(f"❌ Erro no endpoint /transcribe: {str(e)}")
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
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak():
    """Endpoint para converter texto em fala"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Texto vazio'}), 400
        
        print(f"🔊 Convertendo texto para fala: {text[:50]}...")
        
        # Converte texto em áudio
        audio_content = speech_assistant.text_to_speech(text)
        
        if audio_content is None:
            print("❌ Erro ao gerar áudio - audio_content é None")
            return jsonify({'error': 'Erro ao gerar áudio'}), 500
        
        print(f"✅ Áudio gerado com sucesso - {len(audio_content)} bytes")
        
        # Cria arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(audio_content)
        temp_file.close()
        
        print(f"📁 Arquivo temporário criado: {temp_file.name}")
        
        # Retorna o arquivo de áudio
        return send_file(
            temp_file.name,
            as_attachment=False,
            download_name='response.mp3',
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        print(f"❌ Erro no endpoint /speak: {str(e)}")
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
        'mode': 'fallback',
        'features': {
            'speech_recognition': 'simulated',
            'text_to_speech': True,
            'assistant_available': speech_assistant.assistant is not None
        }
    })

if __name__ == '__main__':
    print("🎙️ Iniciando Speech Finance Assistant Fallback...")
    print("ℹ️  Modo fallback com transcrição simulada")
    print("💻 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

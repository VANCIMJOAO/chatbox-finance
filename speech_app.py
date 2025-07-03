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

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

class SpeechFinanceAssistantWeb:
    def __init__(self):
        """Inicializa o assistente financeiro web com fala"""
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
        
        print("🎙️ Speech Finance Assistant Web inicializado!")
    
    def _create_speech_assistant(self):
        """Cria um assistente especializado para interface de voz"""
        try:
            # Tenta buscar assistente existente
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == "Speech Finance Expert Web":
                    print("✅ Speech Finance Expert Web encontrado!")
                    return assistant
            
            # Cria novo assistente se não existir
            print("🔧 Criando Speech Finance Expert Web...")
            
            assistant = self.client.beta.assistants.create(
                name="Speech Finance Expert Web",
                instructions="""
                Você é um ESPECIALISTA EM FINANÇAS com interface WEB e VOZ.
                
                🎙️ OTIMIZADO PARA FALA:
                - Respostas CONVERSACIONAIS e NATURAIS
                - Frases curtas e objetivas
                - Linguagem informal e amigável
                - Evite formatação complexa
                - Use números por extenso quando apropriado
                
                📊 ESPECIALIDADES:
                - Ações brasileiras (B3/Bovespa)
                - Ações internacionais
                - Criptomoedas
                - Índices financeiros
                - Educação financeira simplificada
                
                💡 ESTILO CONVERSACIONAL:
                - "Olha", "Veja", "Então"
                - Explique como se fosse um amigo
                - Faça perguntas para engajar
                - Use analogias simples
                - Sempre mencione que não é aconselhamento
                
                🇧🇷 CONTEXTO BRASILEIRO:
                - Priorize mercado brasileiro
                - Use Reais como moeda padrão
                - Explique impostos nacionais
                - Contexto econômico do Brasil
                """,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_stock_info",
                            "description": "Obtém informações de ação",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "symbol": {
                                        "type": "string",
                                        "description": "Símbolo da ação"
                                    }
                                },
                                "required": ["symbol"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "get_market_summary",
                            "description": "Resumo do mercado",
                            "parameters": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "search_stocks",
                            "description": "Busca empresas",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Nome da empresa"
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    }
                ],
                model="gpt-3.5-turbo",
                temperature=0.4
            )
            
            print("✅ Speech Finance Expert Web criado!")
            return assistant
            
        except Exception as e:
            print(f"❌ Erro ao criar assistente: {e}")
            return None
    
    def transcribe_audio(self, audio_file):
        """Transcreve áudio usando Whisper"""
        try:
            print(f"🎙️ Iniciando transcrição de áudio...")
            
            # Verifica se o arquivo tem conteúdo
            audio_file.seek(0, 2)  # Vai para o final
            file_size = audio_file.tell()
            audio_file.seek(0)  # Volta para o início
            
            if file_size == 0:
                return "Erro: Arquivo de áudio vazio"
            
            print(f"📁 Arquivo: {audio_file.filename}")
            print(f"📊 Tamanho: {file_size} bytes")
            print(f"🎵 Tipo: {audio_file.content_type}")
            
            # Transcreve diretamente com o arquivo recebido
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pt"
            )
            
            result_text = transcript.text.strip()
            print(f"✅ Transcrição: {result_text}")
            return result_text
            
        except Exception as e:
            print(f"❌ Erro na transcrição: {str(e)}")
            raise e
    
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
            return None
    
    def _handle_function_call(self, tool_call):
        """Processa chamadas de função"""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        try:
            if function_name == "get_stock_info":
                result = self.finance_api.get_stock_info(arguments["symbol"])
            elif function_name == "get_market_summary":
                result = self.finance_api.get_market_summary()
            elif function_name == "search_stocks":
                result = self.finance_api.search_stocks(arguments["query"])
            else:
                result = {"error": "Função não encontrada"}
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    def get_or_create_thread(self, session_id):
        """Obtém ou cria uma thread para a sessão"""
        if session_id not in self.user_threads:
            self.user_threads[session_id] = self.client.beta.threads.create()
        return self.user_threads[session_id]
    
    def chat_with_assistant(self, message, session_id="default"):
        """Conversa com o assistente"""
        try:
            if not self.assistant:
                return "Assistente não disponível no momento."
            
            # Obtém a thread da sessão
            thread = self.get_or_create_thread(session_id)
            
            # Adiciona mensagem à thread
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )
            
            # Executa o assistente
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )
            
            # Aguarda conclusão
            max_wait = 30
            wait_time = 0
            
            while run.status in ["queued", "in_progress"] and wait_time < max_wait:
                time.sleep(1)
                wait_time += 1
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            if wait_time >= max_wait:
                return "A análise está demorando muito. Tente novamente."
            
            # Verifica se precisa executar funções
            if run.status == "requires_action":
                tool_outputs = []
                
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    output = self._handle_function_call(tool_call)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output
                    })
                
                # Submete os resultados das funções
                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                
                # Aguarda conclusão novamente
                wait_time = 0
                while run.status in ["queued", "in_progress"] and wait_time < max_wait:
                    time.sleep(1)
                    wait_time += 1
                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )
            
            # Obtém a resposta
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            if messages.data:
                return messages.data[0].content[0].text.value
            else:
                return "Não consegui gerar uma resposta."
                
        except Exception as e:
            return f"Erro na conversa: {str(e)}"
    
    def clear_thread(self, session_id="default"):
        """Limpa a thread da sessão"""
        if session_id in self.user_threads:
            del self.user_threads[session_id]
            return True
        return False

# Instância global do assistente
speech_assistant = SpeechFinanceAssistantWeb()

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
        print(f"📊 Tipo de conteúdo: {audio_file.content_type}")
        
        # Lê o conteúdo para verificar o tamanho real
        audio_file.seek(0)
        content = audio_file.read()
        audio_file.seek(0)  # Volta para o início para processar
        
        if len(content) == 0:
            print("❌ Arquivo sem conteúdo")
            return jsonify({'error': 'Arquivo de áudio vazio'}), 400
        
        print(f"📏 Tamanho do arquivo: {len(content)} bytes")
        
        # Transcreve o áudio
        try:
            transcript = speech_assistant.transcribe_audio(audio_file)
            
            print(f"✅ Transcrição bem-sucedida: {transcript[:50]}...")
            
            return jsonify({
                'transcript': transcript,
                'status': 'success'
            })
            
        except Exception as transcribe_error:
            print(f"❌ Erro na transcrição: {transcribe_error}")
            return jsonify({'error': f'Erro na transcrição: {str(transcribe_error)}'}), 500
        
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
        'features': {
            'speech_recognition': True,
            'text_to_speech': True,
            'assistant_available': speech_assistant.assistant is not None
        }
    })

if __name__ == '__main__':
    print("🎙️ Iniciando Speech Finance Assistant Web...")
    print("💻 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

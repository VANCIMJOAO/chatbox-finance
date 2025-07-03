from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
import sys
import json
import time
from finance_api import FinanceAPI

app = Flask(__name__)
CORS(app)

class FinanceAssistantWeb:
    def __init__(self):
        """Inicializa o assistente financeiro web"""
        # Pega a chave da API das variáveis de ambiente
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ Erro: Chave da API do OpenAI não encontrada!")
            print("Configure a variável de ambiente OPENAI_API_KEY")
            sys.exit(1)
        
        # Inicializa o cliente da OpenAI
        self.client = OpenAI(api_key=api_key)
        
        # Inicializa a API financeira
        self.finance_api = FinanceAPI()
        
        # Cria ou recupera o assistente especializado
        self.assistant = self._create_finance_assistant()
        
        # Dicionário para armazenar threads por sessão
        self.user_threads = {}
        
        print("💰 Finance Assistant Web inicializado!")
    
    def _create_finance_assistant(self):
        """Cria um assistente especializado em finanças"""
        try:
            # Tenta buscar assistente existente
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == "Finance Expert Web":
                    print("✅ Assistente Finance Expert Web encontrado!")
                    return assistant
            
            # Cria novo assistente se não existir
            print("🔧 Criando novo assistente Finance Expert Web...")
            
            assistant = self.client.beta.assistants.create(
                name="Finance Expert Web",
                instructions="""
                Você é um ESPECIALISTA EM FINANÇAS altamente qualificado para interface web. 
                
                📊 SUAS ESPECIALIDADES:
                - Análise de ações brasileiras e internacionais
                - Criptomoedas e índices financeiros
                - Educação financeira didática
                - Análise técnica e fundamentalista
                - Mercado brasileiro (B3, Bovespa)
                
                💡 COMO RESPONDER:
                - Use formatação HTML simples quando apropriado (<b>, <i>, <br>, <ul>, <li>)
                - Seja didático e explique termos técnicos
                - Use emojis para tornar respostas mais amigáveis
                - Sempre mencione que não é aconselhamento financeiro
                - Foque em educação e análise objetiva
                - Responda em português brasileiro
                
                📈 DADOS DISPONÍVEIS:
                - Preços em tempo real
                - Histórico de preços
                - Informações fundamentalistas
                - Resumos de mercado
                - Busca de empresas
                
                ⚠️ IMPORTANTE:
                - Sempre contextualize os dados
                - Explique os riscos envolvidos
                - Eduque sobre conceitos financeiros
                - Seja imparcial e objetivo
                """,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_stock_info",
                            "description": "Obtém informações completas de uma ação",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "symbol": {
                                        "type": "string",
                                        "description": "Símbolo da ação (ex: PETR4.SA, AAPL)"
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
                            "description": "Obtém resumo dos principais índices",
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
                            "description": "Busca ações por nome",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Nome da empresa para buscar"
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "get_trending_stocks",
                            "description": "Obtém ações em tendência",
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
                            "name": "get_stock_history",
                            "description": "Obtém histórico de preços",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "symbol": {
                                        "type": "string",
                                        "description": "Símbolo da ação"
                                    },
                                    "period": {
                                        "type": "string",
                                        "description": "Período (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
                                        "default": "1mo"
                                    }
                                },
                                "required": ["symbol"]
                            }
                        }
                    }
                ],
                model="gpt-3.5-turbo",
                temperature=0.3
            )
            
            print("✅ Assistente Finance Expert Web criado!")
            return assistant
            
        except Exception as e:
            print(f"❌ Erro ao criar assistente: {e}")
            # Fallback para o sistema anterior
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
            elif function_name == "get_trending_stocks":
                result = self.finance_api.get_trending_stocks()
            elif function_name == "get_stock_history":
                result = self.finance_api.get_stock_history(
                    arguments["symbol"], 
                    arguments.get("period", "1mo")
                )
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
                # Fallback para o sistema anterior
                return self._fallback_chat(message)
            
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
            max_wait = 30  # 30 segundos timeout
            wait_time = 0
            
            while run.status in ["queued", "in_progress"] and wait_time < max_wait:
                time.sleep(1)
                wait_time += 1
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            # Timeout protection
            if wait_time >= max_wait:
                return "⏱️ Timeout: A análise está demorando muito. Tente novamente."
            
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
                
                if wait_time >= max_wait:
                    return "⏱️ Timeout: A análise está demorando muito. Tente novamente."
            
            # Obtém a resposta
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            if messages.data:
                return messages.data[0].content[0].text.value
            else:
                return "❌ Não foi possível obter resposta do assistente."
                
        except Exception as e:
            return f"❌ Erro na conversa: {str(e)}"
    
    def _fallback_chat(self, message):
        """Sistema de fallback caso o Assistant não funcione"""
        try:
            # Usa o sistema anterior como backup
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente financeiro especializado. Responda de forma educativa e sempre mencione que não é aconselhamento financeiro."},
                    {"role": "user", "content": message}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ Erro no sistema de backup: {str(e)}"
    
    def clear_thread(self, session_id="default"):
        """Limpa a thread da sessão"""
        if session_id in self.user_threads:
            del self.user_threads[session_id]
            return True
        return False

# Instância global do assistente
finance_assistant = FinanceAssistantWeb()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

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
        bot_response = finance_assistant.chat_with_assistant(user_message, session_id)
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Endpoint para limpar o histórico do chat"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        finance_assistant.clear_thread(session_id)
        return jsonify({'status': 'success', 'message': 'Histórico limpo'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de saúde"""
    return jsonify({
        'status': 'healthy',
        'assistant_available': finance_assistant.assistant is not None
    })

if __name__ == '__main__':
    print("🚀 Iniciando Finance Assistant Web...")
    print("💻 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
import sys
import json
from finance_api import FinanceAPI

app = Flask(__name__)
CORS(app)

class FinanceChatBot:
    def __init__(self):
        """Inicializa o chatbot financeiro"""
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
        
        # Histórico da conversa com contexto financeiro
        self.conversation_history = [
            {"role": "system", "content": """Você é um assistente financeiro especializado chamado FinanceBot. 
            Você tem acesso a dados financeiros em tempo real através de ferramentas especiais.
            
            Suas especialidades incluem:
            - Análise de ações brasileiras e internacionais
            - Informações sobre criptomoedas
            - Dados de índices financeiros
            - Educação financeira
            - Análise de tendências de mercado
            
            Responda sempre em português de forma clara e educativa. Quando o usuário perguntar sobre:
            - Preços de ações: use get_stock_info
            - Histórico: use get_stock_history  
            - Buscar ações: use search_stocks
            - Resumo do mercado: use get_market_summary
            - Ações em alta: use get_trending_stocks
            
            Formate suas respostas de forma organizada e fácil de entender."""}
        ]
    
    def _execute_finance_function(self, function_name, **kwargs):
        """Executa funções da API financeira"""
        try:
            if function_name == "get_stock_info":
                return self.finance_api.get_stock_info(kwargs.get('symbol', ''))
            elif function_name == "get_stock_history":
                return self.finance_api.get_stock_history(
                    kwargs.get('symbol', ''), 
                    kwargs.get('period', '1mo')
                )
            elif function_name == "search_stocks":
                return self.finance_api.search_stocks(kwargs.get('query', ''))
            elif function_name == "get_market_summary":
                return self.finance_api.get_market_summary()
            elif function_name == "get_trending_stocks":
                return self.finance_api.get_trending_stocks()
            else:
                return {"error": "Função não encontrada"}
        except Exception as e:
            return {"error": f"Erro ao executar {function_name}: {str(e)}"}
    
    def get_response(self, user_message):
        """Envia mensagem para a API e retorna a resposta"""
        try:
            # Adiciona a mensagem do usuário ao histórico
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Definição das funções disponíveis para o ChatGPT
            functions = [
                {
                    "name": "get_stock_info",
                    "description": "Obtém informações detalhadas sobre uma ação, incluindo preço atual, variação, volume, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Símbolo da ação (ex: PETR4.SA, AAPL, BTC-USD)"
                            }
                        },
                        "required": ["symbol"]
                    }
                },
                {
                    "name": "get_stock_history",
                    "description": "Obtém histórico de preços de uma ação",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Símbolo da ação"
                            },
                            "period": {
                                "type": "string",
                                "description": "Período: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max",
                                "default": "1mo"
                            }
                        },
                        "required": ["symbol"]
                    }
                },
                {
                    "name": "search_stocks",
                    "description": "Busca ações por nome ou símbolo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Nome ou símbolo da empresa/ação para buscar"
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_market_summary",
                    "description": "Obtém resumo dos principais índices do mercado",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "get_trending_stocks",
                    "description": "Obtém lista de ações em alta/tendência",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
            
            # Chama a API do ChatGPT com function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                functions=functions,
                function_call="auto",
                max_tokens=800,
                temperature=0.7
            )
            
            message = response.choices[0].message
            
            # Verifica se o ChatGPT quer chamar uma função
            if message.function_call:
                function_name = message.function_call.name
                function_args = json.loads(message.function_call.arguments)
                
                # Executa a função
                function_result = self._execute_finance_function(function_name, **function_args)
                
                # Adiciona o resultado da função ao histórico
                self.conversation_history.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_result, ensure_ascii=False)
                })
                
                # Chama o ChatGPT novamente para formatar a resposta
                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation_history,
                    max_tokens=800,
                    temperature=0.7
                )
                
                bot_message = final_response.choices[0].message.content.strip()
            else:
                bot_message = message.content.strip()
            
            # Adiciona a resposta do bot ao histórico
            self.conversation_history.append({"role": "assistant", "content": bot_message})
            
            return bot_message
            
        except Exception as e:
            return f"❌ Erro ao processar solicitação: {str(e)}"
    
    def clear_history(self):
        """Limpa o histórico da conversa"""
        self.conversation_history = [
            {"role": "system", "content": """Você é um assistente financeiro especializado chamado FinanceBot. 
            Você tem acesso a dados financeiros em tempo real através de ferramentas especiais.
            
            Suas especialidades incluem:
            - Análise de ações brasileiras e internacionais
            - Informações sobre criptomoedas
            - Dados de índices financeiros
            - Educação financeira
            - Análise de tendências de mercado
            
            Responda sempre em português de forma clara e educativa."""}
        ]

# Instância global do chatbot
chatbot = FinanceChatBot()

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
        
        if not user_message:
            return jsonify({'error': 'Mensagem vazia'}), 400
        
        # Obtém resposta do chatbot
        bot_response = chatbot.get_response(user_message)
        
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
        chatbot.clear_history()
        return jsonify({'status': 'success', 'message': 'Histórico limpo'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando o Chatbot Web...")
    print("💻 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

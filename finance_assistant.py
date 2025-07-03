#!/usr/bin/env python3
"""
Finance Assistant - Especialista em Finanças usando OpenAI Assistant API
"""

import os
import json
import time
from openai import OpenAI
import yfinance as yf
from datetime import datetime, timedelta

class FinanceAssistant:
    def __init__(self):
        """Inicializa o assistente especializado em finanças"""
        # Configura a API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada!")
        
        self.client = OpenAI(api_key=api_key)
        
        # Cria ou recupera o assistente especializado
        self.assistant = self._create_finance_assistant()
        
        # Cria uma thread para a conversa
        self.thread = self.client.beta.threads.create()
        
        print("💰 Finance Assistant inicializado!")
        print("🤖 Sou um especialista em finanças. Como posso ajudá-lo?")
        print("=" * 60)
    
    def _create_finance_assistant(self):
        """Cria um assistente especializado em finanças"""
        try:
            # Tenta buscar assistente existente
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == "Finance Expert":
                    print("✅ Assistente Finance Expert encontrado!")
                    return assistant
            
            # Cria novo assistente se não existir
            print("🔧 Criando novo assistente Finance Expert...")
            
            assistant = self.client.beta.assistants.create(
                name="Finance Expert",
                instructions="""
                Você é um ESPECIALISTA EM FINANÇAS altamente qualificado. Suas responsabilidades incluem:
                
                📊 ANÁLISE DE MERCADO:
                - Analisar ações, criptomoedas, índices e commodities
                - Explicar movimentos de preços e tendências
                - Fornecer contexto macroeconômico
                
                📈 EDUCAÇÃO FINANCEIRA:
                - Ensinar conceitos financeiros de forma didática
                - Explicar indicadores como P/E, ROE, EBITDA
                - Orientar sobre tipos de investimentos
                
                🎯 ANÁLISE TÉCNICA:
                - Interpretar gráficos e padrões
                - Explicar indicadores técnicos
                - Identificar suportes e resistências
                
                💡 RECOMENDAÇÕES:
                - Dar sugestões baseadas em análise fundamentalista
                - Orientar sobre diversificação de portfólio
                - Alertar sobre riscos
                
                🌍 MERCADO BRASILEIRO:
                - Especialista em B3, Bovespa, ações brasileiras
                - Conhecimento de economia brasileira
                - Impostos e regulamentações nacionais
                
                IMPORTANTE:
                - Sempre forneça dados atualizados quando possível
                - Seja didático e explique termos técnicos
                - Mencione riscos e que não é aconselhamento financeiro
                - Use emojis para tornar as respostas mais amigáveis
                - Responda em português brasileiro
                """,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_stock_price",
                            "description": "Obtém preço atual e informações de uma ação",
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
                            "description": "Obtém resumo dos principais índices do mercado",
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
                            "name": "search_stock",
                            "description": "Busca ações por nome da empresa",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "company_name": {
                                        "type": "string",
                                        "description": "Nome da empresa para buscar"
                                    }
                                },
                                "required": ["company_name"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "get_historical_data",
                            "description": "Obtém dados históricos de preços",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "symbol": {
                                        "type": "string",
                                        "description": "Símbolo da ação"
                                    },
                                    "period": {
                                        "type": "string",
                                        "description": "Período (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
                                    }
                                },
                                "required": ["symbol", "period"]
                            }
                        }
                    }
                ],
                model="gpt-3.5-turbo",  # Modelo disponível
                temperature=0.3  # Mais conservador para análises financeiras
            )
            
            print("✅ Assistente Finance Expert criado com sucesso!")
            return assistant
            
        except Exception as e:
            print(f"❌ Erro ao criar assistente: {e}")
            raise
    
    def get_stock_price(self, symbol):
        """Obtém preço atual de uma ação"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return f"❌ Não foi possível obter dados para {symbol}"
            
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
            
            result = {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                "company_name": info.get('longName', 'N/A'),
                "market_cap": info.get('marketCap', 'N/A'),
                "pe_ratio": info.get('trailingPE', 'N/A'),
                "dividend_yield": info.get('dividendYield', 'N/A'),
                "day_high": round(hist['High'].iloc[-1], 2),
                "day_low": round(hist['Low'].iloc[-1], 2),
                "currency": info.get('currency', 'BRL')
            }
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            return f"❌ Erro ao obter dados: {str(e)}"
    
    def get_market_summary(self):
        """Obtém resumo do mercado"""
        try:
            indices = {
                "IBOVESPA": "^BVSP",      # Bovespa
                "S&P 500": "^GSPC",       # S&P 500
                "NASDAQ": "^IXIC",        # NASDAQ
                "DOW JONES": "^DJI",      # Dow Jones
                "IFIX": "IFIX.SA",        # Índice de FIIs
                "DOLAR": "BRL=X"          # USD/BRL
            }
            
            summary = {}
            for name, symbol in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    
                    if not hist.empty:
                        current = hist['Close'].iloc[-1]
                        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                        change = current - previous
                        change_percent = (change / previous) * 100 if previous != 0 else 0
                        
                        summary[name] = {
                            "price": round(current, 2),
                            "change": round(change, 2),
                            "change_percent": round(change_percent, 2),
                            "symbol": symbol
                        }
                except:
                    continue
            
            return json.dumps(summary, ensure_ascii=False)
            
        except Exception as e:
            return f"❌ Erro ao obter resumo: {str(e)}"
    
    def search_stock(self, company_name):
        """Busca ações por nome da empresa"""
        try:
            # Lista expandida de principais ações brasileiras
            br_stocks = {
                "petrobras": "PETR4.SA",
                "vale": "VALE3.SA",
                "itau": "ITUB4.SA",
                "bradesco": "BBDC4.SA",
                "ambev": "ABEV3.SA",
                "magazine luiza": "MGLU3.SA",
                "banco do brasil": "BBAS3.SA",
                "nubank": "NUBR33.SA",
                "via": "VIIA3.SA",
                "b3": "B3SA3.SA",
                "weg": "WEGE3.SA",
                "suzano": "SUZB3.SA",
                "locaweb": "LWSA3.SA",
                "santander": "SANB11.SA",
                "engie": "EGIE3.SA",
                "cosan": "CSAN3.SA",
                "carrefour": "CRFB3.SA",
                "jbs": "JBSS3.SA",
                "embraer": "EMBR3.SA",
                "localiza": "RENT3.SA"
            }
            
            # Busca por nome (case insensitive)
            company_lower = company_name.lower()
            found_stocks = []
            
            for name, symbol in br_stocks.items():
                if company_lower in name.lower() or name.lower() in company_lower:
                    found_stocks.append({"symbol": symbol, "company": name})
            
            if found_stocks:
                return json.dumps(found_stocks, ensure_ascii=False)
            else:
                return json.dumps({"error": "Empresa não encontrada na base de dados brasileira"})
            
        except Exception as e:
            return f"❌ Erro na busca: {str(e)}"
    
    def get_historical_data(self, symbol, period):
        """Obtém dados históricos"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return f"❌ Sem dados históricos para {symbol}"
            
            # Estatísticas principais
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            max_price = hist['High'].max()
            min_price = hist['Low'].min()
            avg_volume = hist['Volume'].mean() if 'Volume' in hist.columns else 0
            
            total_return = ((end_price - start_price) / start_price) * 100
            volatility = hist['Close'].pct_change().std() * 100
            
            # Últimos 5 dias de dados
            recent_data = []
            for i in range(min(5, len(hist))):
                idx = -(i+1)
                date = hist.index[idx].strftime('%Y-%m-%d')
                recent_data.append({
                    "date": date,
                    "close": round(hist['Close'].iloc[idx], 2),
                    "volume": int(hist['Volume'].iloc[idx]) if 'Volume' in hist.columns else 0
                })
            
            result = {
                "symbol": symbol,
                "period": period,
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "max_price": round(max_price, 2),
                "min_price": round(min_price, 2),
                "total_return": round(total_return, 2),
                "volatility": round(volatility, 2),
                "avg_volume": int(avg_volume),
                "data_points": len(hist),
                "recent_data": recent_data
            }
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            return f"❌ Erro ao obter histórico: {str(e)}"
    
    def _handle_function_call(self, tool_call):
        """Processa chamadas de função"""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "get_stock_price":
            return self.get_stock_price(arguments["symbol"])
        elif function_name == "get_market_summary":
            return self.get_market_summary()
        elif function_name == "search_stock":
            return self.search_stock(arguments["company_name"])
        elif function_name == "get_historical_data":
            return self.get_historical_data(arguments["symbol"], arguments["period"])
        else:
            return "❌ Função não encontrada"
    
    def chat(self, message):
        """Envia mensagem para o assistente"""
        try:
            # Adiciona mensagem à thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=message
            )
            
            # Executa o assistente
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # Aguarda conclusão
            while run.status in ["queued", "in_progress"]:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
            
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
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                
                # Aguarda conclusão novamente
                while run.status in ["queued", "in_progress"]:
                    time.sleep(1)
                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread.id,
                        run_id=run.id
                    )
            
            # Obtém a resposta
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            return messages.data[0].content[0].text.value
            
        except Exception as e:
            return f"❌ Erro na conversa: {str(e)}"
    
    def run(self):
        """Loop principal do assistente"""
        while True:
            try:
                user_input = input("\n💰 Você: ").strip()
                
                if user_input.lower() in ['sair', 'exit', 'quit', 'bye']:
                    print("\n🤖 Finance Assistant: Até logo! Bons investimentos! 📈")
                    break
                
                if not user_input:
                    print("⚠️ Por favor, digite uma pergunta sobre finanças!")
                    continue
                
                print("\n🤖 Finance Assistant: Analisando...", end="", flush=True)
                
                response = self.chat(user_input)
                print(f"\r🤖 Finance Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Finance Assistant: Até logo! 📈")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {str(e)}")

def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Finance Assistant...")
        assistant = FinanceAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")

if __name__ == "__main__":
    main()

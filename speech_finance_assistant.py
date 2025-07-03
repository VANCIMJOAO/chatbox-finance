#!/usr/bin/env python3
"""
Speech Recognition Finance Assistant
Assistente Financeiro com Reconhecimento de Fala usando OpenAI Whisper
"""

import os
import json
import time
import io
import wave
import threading
from openai import OpenAI
import yfinance as yf
from datetime import datetime, timedelta
import speech_recognition as sr
import pyaudio

class SpeechFinanceAssistant:
    def __init__(self):
        """Inicializa o assistente com reconhecimento de fala"""
        # Configura a API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada!")
        
        self.client = OpenAI(api_key=api_key)
        
        # Inicializa o reconhecedor de fala
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibra o microfone para ruído ambiente
        print("🎤 Calibrando microfone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        # Cria ou recupera o assistente especializado
        self.assistant = self._create_finance_assistant()
        
        # Cria uma thread para a conversa
        self.thread = self.client.beta.threads.create()
        
        print("🎙️ Speech Finance Assistant inicializado!")
        print("🤖 Agora você pode falar comigo! Pressione ENTER para começar a gravar.")
        print("=" * 70)
    
    def _create_finance_assistant(self):
        """Cria um assistente especializado em finanças"""
        try:
            # Tenta buscar assistente existente
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == "Speech Finance Expert":
                    print("✅ Assistente Speech Finance Expert encontrado!")
                    return assistant
            
            # Cria novo assistente se não existir
            print("🔧 Criando novo assistente Speech Finance Expert...")
            
            assistant = self.client.beta.assistants.create(
                name="Speech Finance Expert",
                instructions="""
                Você é um ESPECIALISTA EM FINANÇAS com interface de VOZ.
                
                🎙️ CONSIDERAÇÕES PARA FALA:
                - Responda de forma CONVERSACIONAL e NATURAL
                - Use frases mais curtas e diretas
                - Evite formatação complexa (HTML, markdown)
                - Seja mais informal e amigável
                - Use expressões como "olha", "veja", "então"
                
                📊 ESPECIALIDADES:
                - Análise de ações brasileiras e internacionais
                - Criptomoedas e índices financeiros
                - Educação financeira simplificada
                - Explicação de conceitos de forma oral
                - Mercado brasileiro (B3, Bovespa)
                
                💡 ESTILO DE RESPOSTA:
                - Conversacional e natural para áudio
                - Explique números de forma clara ("quinze vírgula vinte")
                - Use analogias simples
                - Perguntas para engajar o usuário
                - Sempre mencione que não é aconselhamento
                
                🇧🇷 FOCO BRASILEIRO:
                - Priorize ações da B3
                - Explique impostos brasileiros
                - Use reais como moeda padrão
                - Contexto econômico nacional
                """,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_stock_price",
                            "description": "Obtém preço atual de uma ação",
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
                            "name": "search_stock",
                            "description": "Busca ações por nome",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "company_name": {
                                        "type": "string",
                                        "description": "Nome da empresa"
                                    }
                                },
                                "required": ["company_name"]
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
                    }
                ],
                model="gpt-3.5-turbo",
                temperature=0.4  # Pouco mais criativo para conversação
            )
            
            print("✅ Assistente Speech Finance Expert criado!")
            return assistant
            
        except Exception as e:
            print(f"❌ Erro ao criar assistente: {e}")
            raise
    
    def record_audio(self, duration=5):
        """Grava áudio do microfone"""
        try:
            print("🔴 Gravando... (Fale agora)")
            
            with self.microphone as source:
                # Grava por um tempo determinado ou até silêncio
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=10)
            
            print("⏹️ Gravação finalizada!")
            return audio
            
        except sr.WaitTimeoutError:
            print("⏰ Timeout - nenhum áudio detectado")
            return None
        except Exception as e:
            print(f"❌ Erro na gravação: {e}")
            return None
    
    def transcribe_audio_whisper(self, audio):
        """Transcreve áudio usando OpenAI Whisper"""
        try:
            # Converte o áudio para formato compatível
            wav_data = io.BytesIO()
            wav_data.write(audio.get_wav_data())
            wav_data.seek(0)
            
            # Cria um arquivo temporário em memória
            wav_data.name = "audio.wav"
            
            # Usa a API Whisper da OpenAI
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=wav_data,
                language="pt"  # Português
            )
            
            return transcript.text.strip()
            
        except Exception as e:
            print(f"❌ Erro na transcrição Whisper: {e}")
            return None
    
    def text_to_speech_openai(self, text):
        """Converte texto em fala usando OpenAI TTS"""
        try:
            print("🔊 Gerando áudio da resposta...")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # Voz neutra
                input=text,
                speed=1.0
            )
            
            # Salva temporariamente e reproduz
            audio_file = "temp_response.mp3"
            response.stream_to_file(audio_file)
            
            # Reproduz o áudio (depende do sistema)
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Linux":
                subprocess.run(["mpg123", audio_file], capture_output=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_file])
            elif system == "Windows":
                subprocess.run(["start", audio_file], shell=True)
            
            # Remove arquivo temporário
            os.remove(audio_file)
            
        except Exception as e:
            print(f"❌ Erro no TTS: {e}")
            print(f"📝 Resposta (texto): {text}")
    
    def get_stock_price(self, symbol):
        """Obtém preço atual de uma ação"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return f"Não consegui obter dados para {symbol}"
            
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
            
            # Formato mais conversacional para fala
            result = {
                "symbol": symbol,
                "company": info.get('longName', symbol),
                "price": f"R$ {current_price:.2f}",
                "change": f"{change:+.2f}",
                "change_percent": f"{change_percent:+.2f}%",
                "status": "alta" if change > 0 else "baixa" if change < 0 else "estável"
            }
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            return f"Erro ao buscar dados de {symbol}: {str(e)}"
    
    def get_market_summary(self):
        """Obtém resumo do mercado"""
        try:
            indices = {
                "Ibovespa": "^BVSP",
                "S&P 500": "^GSPC",
                "NASDAQ": "^IXIC",
                "Dólar": "BRL=X"
            }
            
            summary = {}
            for name, symbol in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    
                    if not hist.empty:
                        current = hist['Close'].iloc[-1]
                        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                        change_percent = ((current - previous) / previous) * 100 if previous != 0 else 0
                        
                        summary[name] = {
                            "price": round(current, 2),
                            "change_percent": round(change_percent, 2),
                            "trend": "subindo" if change_percent > 0 else "caindo" if change_percent < 0 else "estável"
                        }
                except:
                    continue
            
            return json.dumps(summary, ensure_ascii=False)
            
        except Exception as e:
            return f"Erro ao obter resumo: {str(e)}"
    
    def search_stock(self, company_name):
        """Busca ações por nome"""
        try:
            br_stocks = {
                "petrobras": "PETR4.SA",
                "vale": "VALE3.SA", 
                "itau": "ITUB4.SA",
                "bradesco": "BBDC4.SA",
                "ambev": "ABEV3.SA",
                "magazine luiza": "MGLU3.SA"
            }
            
            company_lower = company_name.lower()
            for name, symbol in br_stocks.items():
                if company_lower in name:
                    return json.dumps({"found": True, "symbol": symbol, "company": name})
            
            return json.dumps({"found": False, "message": "Empresa não encontrada"})
            
        except Exception as e:
            return f"Erro na busca: {str(e)}"
    
    def get_trending_stocks(self):
        """Obtém ações em tendência"""
        trending = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA"]
        results = []
        
        for symbol in trending:
            try:
                data = self.get_stock_price(symbol)
                if "Erro" not in data:
                    results.append(json.loads(data))
            except:
                continue
        
        return json.dumps(results, ensure_ascii=False)
    
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
        elif function_name == "get_trending_stocks":
            return self.get_trending_stocks()
        else:
            return "Função não encontrada"
    
    def chat_with_assistant(self, message):
        """Conversa com o assistente"""
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
            max_wait = 30
            wait_time = 0
            
            while run.status in ["queued", "in_progress"] and wait_time < max_wait:
                time.sleep(1)
                wait_time += 1
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
            
            if wait_time >= max_wait:
                return "Desculpe, a análise está demorando muito. Tente novamente."
            
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
                wait_time = 0
                while run.status in ["queued", "in_progress"] and wait_time < max_wait:
                    time.sleep(1)
                    wait_time += 1
                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread.id,
                        run_id=run.id
                    )
            
            # Obtém a resposta
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            if messages.data:
                return messages.data[0].content[0].text.value
            else:
                return "Não consegui gerar uma resposta."
                
        except Exception as e:
            return f"Erro na conversa: {str(e)}"
    
    def run(self):
        """Loop principal do assistente com fala"""
        print("\n🎙️ COMANDOS:")
        print("• ENTER - Começar gravação")
        print("• 'sair' - Encerrar")
        print("• 'texto' - Modo texto")
        print("=" * 50)
        
        while True:
            try:
                # Aguarda comando do usuário
                command = input("\n💬 Pressione ENTER para falar (ou digite comando): ").strip().lower()
                
                if command in ['sair', 'exit', 'quit']:
                    print("\n🤖 Até logo! Bons investimentos! 📈")
                    break
                
                if command == 'texto':
                    # Modo texto
                    text_input = input("💬 Digite sua pergunta: ").strip()
                    if text_input:
                        print("\n🤖 Analisando...")
                        response = self.chat_with_assistant(text_input)
                        print(f"\n🤖 Resposta: {response}")
                        
                        # Opção de áudio
                        audio_choice = input("\n🔊 Quer ouvir a resposta? (s/n): ").strip().lower()
                        if audio_choice in ['s', 'sim', 'y', 'yes']:
                            self.text_to_speech_openai(response)
                    continue
                
                # Modo de fala (padrão)
                print("\n🎤 Modo de Fala Ativado!")
                audio = self.record_audio()
                
                if audio is None:
                    print("❌ Nenhum áudio capturado. Tente novamente.")
                    continue
                
                # Transcreve usando Whisper
                print("🔄 Transcrevendo com Whisper...")
                user_text = self.transcribe_audio_whisper(audio)
                
                if not user_text:
                    print("❌ Não consegui entender o áudio. Tente novamente.")
                    continue
                
                print(f"📝 Você disse: '{user_text}'")
                
                if user_text.lower() in ['sair', 'tchau', 'até logo']:
                    print("\n🤖 Até logo! Bons investimentos! 📈")
                    break
                
                # Processa com o assistente
                print("🤖 Analisando sua pergunta...")
                response = self.chat_with_assistant(user_text)
                
                print(f"\n🤖 Resposta: {response}")
                
                # Converte resposta em áudio
                self.text_to_speech_openai(response)
                
            except KeyboardInterrupt:
                print("\n\n🤖 Até logo! 📈")
                break
            except Exception as e:
                print(f"\n❌ Erro: {str(e)}")

def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Speech Finance Assistant...")
        assistant = SpeechFinanceAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")

if __name__ == "__main__":
    main()

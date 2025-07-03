#!/usr/bin/env python3
"""
Chatbot simples usando a API do OpenAI ChatGPT
Para aprendizado - executa no terminal
"""

import os
import openai
from openai import OpenAI
import sys

class ChatBot:
    def __init__(self):
        """Inicializa o chatbot com a configuração da API"""
        # Pega a chave da API das variáveis de ambiente
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ Erro: Chave da API do OpenAI não encontrada!")
            print("Por favor, configure a variável de ambiente OPENAI_API_KEY")
            print("Exemplo: export OPENAI_API_KEY='sua-chave-aqui'")
            sys.exit(1)
        
        # Inicializa o cliente da OpenAI
        self.client = OpenAI(api_key=api_key)
        
        # Histórico da conversa
        self.conversation_history = [
            {"role": "system", "content": "Você é um assistente útil e amigável. Responda de forma clara e concisa."}
        ]
        
        print("🤖 Chatbot iniciado! Digite 'sair' para encerrar.")
        print("=" * 50)
    
    def get_response(self, user_message):
        """Envia mensagem para a API e retorna a resposta"""
        try:
            # Adiciona a mensagem do usuário ao histórico
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Chama a API do ChatGPT
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Modelo mais barato para testes
                messages=self.conversation_history,
                max_tokens=500,
                temperature=0.7
            )
            
            # Extrai a resposta
            bot_message = response.choices[0].message.content.strip()
            
            # Adiciona a resposta do bot ao histórico
            self.conversation_history.append({"role": "assistant", "content": bot_message})
            
            return bot_message
            
        except Exception as e:
            return f"❌ Erro ao comunicar com a API: {str(e)}"
    
    def run(self):
        """Loop principal do chatbot"""
        while True:
            try:
                # Pega a entrada do usuário
                user_input = input("\n👤 Você: ").strip()
                
                # Verifica se o usuário quer sair
                if user_input.lower() in ['sair', 'exit', 'quit', 'bye']:
                    print("\n🤖 Bot: Até logo! Foi um prazer conversar com você! 👋")
                    break
                
                # Verifica se a entrada não está vazia
                if not user_input:
                    print("⚠️  Por favor, digite uma mensagem!")
                    continue
                
                # Mostra que está processando
                print("\n🤖 Bot: Pensando...", end="", flush=True)
                
                # Obtém e exibe a resposta
                response = self.get_response(user_input)
                print(f"\r🤖 Bot: {response}")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Bot: Até logo! 👋")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {str(e)}")

def main():
    """Função principal"""
    print("🚀 Iniciando o Chatbot...")
    chatbot = ChatBot()
    chatbot.run()

if __name__ == "__main__":
    main()

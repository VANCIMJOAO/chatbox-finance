#!/usr/bin/env python3
"""
Teste da API Whisper
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import tempfile

# Carrega variáveis de ambiente
load_dotenv()

def test_whisper_api():
    """Testa se a API Whisper está funcionando"""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Cria um arquivo de áudio de teste (silêncio)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            # Cria um arquivo WAV mínimo com 1 segundo de silêncio
            wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x22\x56\x00\x00\x44\xac\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
            temp_file.write(wav_header)
            temp_file_path = temp_file.name
        
        # Testa a API
        with open(temp_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pt"
            )
            
        os.unlink(temp_file_path)
        print("✅ API Whisper funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na API Whisper: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando API Whisper...")
    test_whisper_api()

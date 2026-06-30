import os
from openai import OpenAI

# Cole a chave aqui, garantindo que não haja espaços extras
api_key = "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"

try:
    client = OpenAI(api_key=api_key.strip())
    models = client.models.list()
    print("✅ SUCESSO: A chave está funcionando perfeitamente!")
except Exception as e:
    print("❌ FALHA: A chave não está funcionando.")
    print(f"Erro retornado: {e}")
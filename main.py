

import os
from google import genai
from google.genai import types

# 1. Configuração do Cliente (A API key deve estar na variável de ambiente GEMINI_API_KEY)
client = genai.Client()

# 2. Definição da Persona do Agente (System Instruction)
system_instruction = """
Você é o 'PyBot', um instrutor de programação sênior especializado em Python.
Seu objetivo é ajudar desenvolvedores de todos os níveis a tirarem dúvidas sobre a linguagem.

Regras de comportamento:
1. Seja didático, paciente e direto ao ponto.
2. Sempre que explicar um conceito, forneça um exemplo de código limpo e comentado.
3. Se o usuário enviar um código com erro, identifique o erro, explique o motivo e mostre a correção.
4. Use formatação Markdown para deixar o código legível.
5. Se a pergunta não for sobre Python ou programação relacionada, decline gentilmente.
"""

def perguntar_ao_agente(duvida_usuario: str):
    """Envia a dúvida do usuário para o agente de IA."""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=duvida_usuario,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3, # Baixa temperatura para respostas mais precisas e técnicas
            )
        )
        return response.text
    except Exception as e:
        return f"Erro ao se conectar com o agente: {e}"

# 3. Demonstração de Uso
if __name__ == "__main__":
    # Exemplo de dúvida comum de iniciantes
    minha_duvida = "Qual é a diferença entre uma lista e uma tupla em Python? Quando devo usar cada uma?"
    
    print(f"Usuário: {minha_duvida}\n")
    print("Respostado do Agente:\n")
    print(perguntar_ao_agente(minha_duvida))

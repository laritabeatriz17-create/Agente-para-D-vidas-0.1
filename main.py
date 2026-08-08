import os
import streamlit as st
from groq import Groq

# Configuração da chave de API (Busca da variável de ambiente ou string)
# Recomendado: st.secrets["GROQ_API_KEY"] ou os.environ.get("GROQ_API_KEY")
API_KEY = os.environ.get("GROQ_API_KEY", "SUA_CHAVE_AQUI")

# Inicializa o cliente Groq
client = Groq(api_key=API_KEY)

# Título do aplicativo
st.title("Agente para tirar Dúvidas 🤖")

# Campo de entrada de texto
pergunta = st.text_input('Digite sua pergunta:')

# Botão de envio
if st.button('Enviar'):
    # Valida se o usuário digitou algo (descomentado para segurança)
    if pergunta.strip():
        with st.spinner('Pensando...'):
            try:
                # Chamada para a API do Groq
                resposta = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            'role': 'system',
                            'content': "Você é um amigo prestativo para tirar dúvidas."
                        },
                        {
                            'role': 'user',
                            'content': pergunta
                        }
                    ]
                )
                
                # Exibe o resultado de forma formatada (Markdown aceita quebras de linha e negrito)
                st.markdown("### Resposta:")
                st.write(resposta.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Erro ao consultar a API: {e}")
    else:
        st.warning("Por favor, digite uma pergunta antes de enviar.")



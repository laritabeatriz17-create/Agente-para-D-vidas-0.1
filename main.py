import os
import streamlit as st
from groq import Groq

# pip install groq streamlit

st.title("Agente para tirar Dúvidas")

# --- Chave da API ---
# Busca a chave nas variáveis de ambiente ou usa st.secrets no Streamlit Cloud
API_KEY = os.getenv("GROQ_API_KEY", "")

# Caso prefira inserir manualmente para testes locais, descomente a linha abaixo:
# API_KEY = "gsk_sua_chave_aqui"

if not API_KEY or API_KEY == "api_key":
    st.error("Defina sua chave da API da Groq na variável de ambiente GROQ_API_KEY ou no código.")
    st.stop()

client = Groq(api_key=API_KEY)

# Mantém o histórico da conversa para dar mais contexto e continuidade
if "historico" not in st.session_state:
    st.session_state.historico = []

pergunta = st.text_input("pergunta:")

if st.button("enviar"):
    if pergunta.strip():
        mensagens = [
            {
                "role": "system",
                "content": (
                    "Você é um amigo animado e curioso que adora tirar dúvidas. "
                    "Explique de forma clara e simples, com exemplos quando fizer sentido. "
                    "Ao final de cada resposta, incentive a pessoa a continuar aprendendo: "
                    "faça uma pergunta de acompanhamento, sugira um tema relacionado "
                    "ou proponha um pequeno desafio para manter a conversa interessante "
                    "e a pessoa engajada em fazer mais perguntas."
                ),
            }
        ]

        # Adiciona histórico anterior para dar continuidade à conversa
        mensagens.extend(st.session_state.historico)
        mensagens.append({"role": "user", "content": pergunta})

        try:
            with st.spinner("Pensando..."):
                resposta = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    messages=mensagens,
                )

            texto_resposta = resposta.choices[0].message.content

            if not texto_resposta:
                st.warning("O agente não retornou nenhuma resposta. Tente novamente.")
            else:
                # Guarda no histórico
                st.session_state.historico.append({"role": "user", "content": pergunta})
                st.session_state.historico.append(
                    {"role": "assistant", "content": texto_resposta}
                )
                st.write(texto_resposta)

        except Exception as e:
            st.error(f"Ocorreu um erro ao consultar a API da Groq: {e}")

    else:
        st.warning("Digite uma pergunta antes de enviar.")

# Mostra o histórico da conversa na tela
if st.session_state.historico:
    st.divider()
    st.subheader("Histórico da conversa")
    for msg in st.session_state.historico:
        autor = "Você" if msg["role"] == "user" else "Agente"
        st.markdown(f"**{autor}:** {msg['content']}")

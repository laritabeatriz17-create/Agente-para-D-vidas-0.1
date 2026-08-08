import os
import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Agente de Dúvidas", page_icon="💡")
st.title("Agente para tirar Dúvidas")

# --- Chave da API ---
API_KEY = os.getenv("GROQ_API_KEY", "")

# Se não encontrar no ambiente, você pode colar sua chave diretamente aqui para testes locais:
# API_KEY = "gsk_sua_chave_aqui"

if not API_KEY or API_KEY == "api_key":
    st.error("Defina sua chave da API da Groq na variável GROQ_API_KEY ou no arquivo do código.")
    st.stop()

client = Groq(api_key=API_KEY)

# Mantém o histórico da conversa na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Campo de formulário para permitir envio ao apertar Enter
with st.form(key="form_pergunta", clear_on_submit=True):
    pergunta = st.text_input("Sua pergunta:")
    botao_enviar = st.form_submit_button("Enviar")

if botao_enviar:
    if pergunta.strip():
        # 1. Prepara a estrutura enviada à Groq (System Prompt fixo na primeira posição)
        mensagens_api = [
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

        # 2. Adiciona o histórico existente + a nova pergunta
        mensagens_api.extend(st.session_state.historico)
        mensagens_api.append({"role": "user", "content": pergunta})

        try:
            with st.spinner("Pensando..."):
                resposta = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    messages=mensagens_api,
                )

            texto_resposta = resposta.choices[0].message.content

            if not texto_resposta:
                st.warning("O agente não retornou nenhuma resposta. Tente novamente.")
            else:
                # 3. Salva no histórico somente APÓS a confirmação de sucesso da API
                st.session_state.historico.append({"role": "user", "content": pergunta})
                st.session_state.historico.append({"role": "assistant", "content": texto_resposta})

        except Exception as e:
            st.error(f"Ocorreu um erro ao consultar a API da Groq: {e}")

    else:
        st.warning("Digite uma pergunta antes de enviar.")

# --- Exibição do Histórico na Tela ---
if st.session_state.historico:
    st.divider()
    st.subheader("Histórico da conversa")
    for msg in st.session_state.historico:
        autor = "Você" if msg["role"] == "user" else "Agente"
        st.markdown(f"**{autor}:** {msg['content']}")

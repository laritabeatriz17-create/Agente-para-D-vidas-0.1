


from dotenv import load_dotenv
load_dotenv()

from groq import Groq
import streamlit as st 
import time
import os



# pip install groq 



client = Groq(
    api_key="API_KEY",
)
st.title("Agente para tirar Dúvidas") 
pergunta  = st.text_input('pergunta:')

if st.button('enviar'):
     if pergunta.strip():
        reposta =  client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        # temperature=0.7,

        messages=[
        {
        'role':'system',
        'content':"Você é um piloto"
        },
        {
            'role':'user',
            'content': pergunta
            
        }
        ]
        )

        st.text(reposta.choices[0].message.content)
        time.sleep(0)
       

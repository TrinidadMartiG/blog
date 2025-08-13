import streamlit as st

META = {
    "title": "Mi primer post: ¿Por qué crear este blog?",
    "date": "2025-07-17",
    "tags": ["reflexiones", "inicio"],
}

def show_post():
    st.markdown("""
    ### La motivación detrás de este blog
    
    Forzarme un poquito a escribir, pensar más profundo y compartir mis ideas, reflexiones y descubrimientos.
    En una era de IA, me revelo ante la inmediatez del contenido basura e intento llevar un ritmo más íntimo y personal, pausado, humano. 
    
    Espero encontrar de esta manera expertiz, dominio, ideas, o solo anécdotas divertidas de mis éxitos o fallos :).
    
    **¿Qué puedes esperar?**
    - Entradas detalladas, entradas simples, ideas.
    - Apuntes de mis estudios, dicen que no hay mejor forma de aprender que enseñando, gracias señor Feynman.
    - Reflexiones sobre tecnología y desarrollo
    - Experiencias con diferentes herramientas y frameworks
    """)

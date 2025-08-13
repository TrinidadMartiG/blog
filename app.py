import streamlit as st
import datetime
from pathlib import Path
import time
from posts import posts

# Configuración de la página
st.set_page_config(
    page_title="Blog",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session state para auto-refresh
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Auto-refresh cada 30 segundos (opcional)
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)
if auto_refresh:
    time.sleep(30)
    st.rerun()

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .post-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .post-date {
        color: #6c757d;
        font-size: 0.9rem;
    }
    .sidebar-section {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .refresh-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Indicador de última actualización
current_time = datetime.datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div class="refresh-indicator">
    Última actualización: {current_time}
</div>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>👩🏻‍💻</h1>
    <h2>...</h2>
</div>
""", unsafe_allow_html=True)

# Sidebar con información personal
with st.sidebar:
    # Controles de refresh
    st.markdown("### 🔄 Controles")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refrescar"):
            st.rerun()
    with col2:
        if st.button("⚡ Limpiar Cache"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("""
    <div class="sidebar-section">
        <h3>👋 Sobre mí</h3>
        <p>Desarrollo en python, a veces react. También analizo datos y he construido modelos de ML :).<p/>
        <p>Apasionada por la tecnología, la ciencia y los libros.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3>🛠️ Tech Stack</h3>
        <ul>
            <li>Python</li>
            <li>React</li>
            <li>Pandas</li>
            <li>GCP</li>
            <li>Streamlit</li>
            <li>Docker</li>
            <li>Git</li>
            <li>Linux</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3>🔗 Conecta conmigo</h3>
        <p>📧 trinidad.martig@gmail.com<br>
        💼 <a href="https://www.linkedin.com/in/trinidad-mart%C3%AD-guti%C3%A9rrez-a9b872244/">LinkedIn</a><br>
        🐙 <a href="https://github.com/TrinidadMartiG">GitHub</a><br>
        👾 Freelanceo en : <a href="https://nebulabs.dev/">Nebulabs</a></p>
    </div> 
    """, unsafe_allow_html=True)

# Función para mostrar posts
def mostrar_post(post_module):
    meta = getattr(post_module, "META", {})
    title = meta.get("title", "Post sin título")
    date = meta.get("date", "")
    tags = meta.get("tags", [])
    
    st.markdown(f"""
    <div class="post-card">
        <h2>{title}</h2>
        <p class="post-date">📅 {date}</p>
    """, unsafe_allow_html=True)
    
    if tags:
        tags_html = " ".join([f"<span style='background:#e3f2fd; padding:0.2rem 0.5rem; border-radius:15px; font-size:0.8rem; margin-right:0.5rem; display:inline-block;'>{tag}</span>" for tag in tags])
        st.markdown(f"<div style='margin-top:0.5rem;'>{tags_html}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Ejecutar la función show_post del módulo
    if hasattr(post_module, "show_post"):
        post_module.show_post()
    
    st.markdown("---")

# Navegación principal
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Inicio", "📝 Posts", "🚀 Proyectos", "📚 Recursos"])

with tab1:
    st.header("¡Bienvenid@ a mi blog!")
    
    st.markdown("""
    ### 👋 ¡Hola! Soy Trinidad :)
    Hola hola, aquí encontrarás:
    
    - 🔍 **Mis apuntes y reflexiones** a cerca de tecnologías, problemas y soluciones que he encontrado en el camino
    - 🛠️ **Proyectos** que he desarrollado  
    - 📖 **Recursos** útiles para otros desarrolladores
    
    Mi objetivo es documentar mi aprendizaje continuo y ayudar a otros que estén 
    en un camino similar al mío.
    """)

with tab2:
    st.header("📝 Posts")
    
    # Mostrar todos los posts en orden inverso (último primero)
    for post in reversed(posts):
        mostrar_post(post)
with tab3:
    st.header("🚀 Proyectos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Calculadora Clínica
        **Tech Stack:** Python, Pandas, Streamlit, Git
                    
        **Que hace?:**
        - Calcula dosis de antibióticos para pacientes, según metricas antropométricas.
        - Calcula dosis seguras de fármacos según funcionamiento renal.
                    
        **Objetivo:**
        - Facilitar la toma de decisiones clínicas.
        - Ahorrar tiempo del equipo al centralizar calculos en una sola herramienta.
                    
        [Vela en acción](https://nebulacalculator-djwfefdgbt2gwixd7ffkst.streamlit.app/)
        """)

with tab4:
    st.header("📚 Recursos Útiles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
                    
        ### Libros que recomiendo:
        * Crónicas marcianas - Ray Bradbury
        * Kafka en la orilla - Haruki Murakami (El único libro que he leido multiples veces)
        * La trilogía de Nueva York - Paul Auster
        * El palacio de la luna - Paul Auster
        * Los detectives salvajes - Roberto Bolaño
        
        """)
    
    
    st.markdown("""
    ### 🔗 Personas y comunidades
    - **LinkedIn:** [Paulo Villaroel](https://www.linkedin.com/in/paulovillarroel/), enfermero y data scientist que ha compartido mucho sobre machine learning y data science aplicado a salud.
    - **LinkedIn:** [Nicolás Gómez](https://www.linkedin.com/in/codewithnico/), otro seco, tiene muchos datos sobre como trabajar para el extranjero, calcular sueldos en USD, escribe harto también :).

    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 2rem 0;'>
    <p>Hecho con ❤️ por Trixxie 👽 usando Streamlit | © 2025 Mi Blog Tech</p>
</div>
""", unsafe_allow_html=True)
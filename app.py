import streamlit as st
from pathlib import Path
from posts import posts

# Configuración de la página
st.set_page_config(
    page_title="Blog",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para elementos específicos (usando config.toml para el tema base)
st.markdown("""
<style>
    /* Header principal con gradiente rosa */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #ec4899 0%, #be185d 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(236, 72, 153, 0.2);
    }
    
    /* Estilos para post cards */
    .post-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #ec4899;
        border: 1px solid #f3e8ff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .post-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(236, 72, 153, 0.1);
    }
    
    /* Estilos para tags */
    .tag {
        background: #fce7f3;
        color: #ec4899;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.3rem;
        display: inline-block;
        border: 1px solid #ec4899;
        opacity: 0.9;
        transition: all 0.2s ease;
    }
    
    .tag:hover {
        opacity: 1;
        transform: translateY(-1px);
        background: #ec4899;
        color: white;
    }
    
    
    /* Estilos para sidebar sections */
    .sidebar-section {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #f3e8ff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .sidebar-section a {
        color: #ec4899;
        text-decoration: none;
        font-weight: 500;
    }
    
    .sidebar-section a:hover {
        color: #be185d;
        text-decoration: underline;
    }

</style>
""", unsafe_allow_html=True)



# Header principal
st.markdown("""
<div class="main-header">
    <h2>Trixxie en el mundo tech 👽</h2>
    <p style='margin-top: 1rem; font-size: 1.1rem; opacity: 0.9;'> Desarrollo • Data • Reflexiones</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información personal
with st.sidebar:

    st.markdown("""
    <div class="sidebar-section">
        <h3>👋 Sobre mí</h3>
        <p>Desarrollo en python, a veces react, a veces analizo datos, y he modelado uno que otro modelo de ML :).<p/>
        <p>Apasionada por la tecnología, la ciencia y los libros.</p>
        <p>Buscando mi especialidad? 🤔</p>
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
        tags_html = " ".join([f"<span class='tag'>{tag}</span>" for tag in tags])
        st.markdown(f"<div style='margin-top:0.5rem;'>{tags_html}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Ejecutar la función show_post del módulo
    if hasattr(post_module, "show_post"):
        post_module.show_post()
    
    st.markdown("---")

# Navegación principal
tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "📝 Posts", "📚 Recursos"])

with tab1:
    st.header("¡Bienvenid@ a mi blog!")
    
    st.markdown("""
    ### 👋 ¡Hola! Soy Trinidad :)
    aquí encontrarás:
    
    - 🔍 **Mis apuntes y reflexiones** a cerca de tecnologías, soluciones, y cosas que he encontrado en el camino.
    - 📖 **Libros, ñoñerias, personas bacanes que sigo** 
    
    Mi objetivo es documentar mi aprendizaje y quizas motivar o ayudar a otros que estén en la misma.
    """)

with tab2:
    st.header("📝 Posts")
    
    # Mostrar todos los posts en orden inverso (último primero)
    for post in reversed(posts):
        mostrar_post(post)

with tab3:
    st.header("📚 Recursos que me vuelan la cabeza")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📖 Libros que recomiendo:
        🔥 **Kafka en la orilla** - Haruki Murakami *(El único que he leído múltiples veces)*
        
        **Otros que me marcaron:**
        - Crónicas marcianas - Ray Bradbury
        - La trilogía de Nueva York - Paul Auster  
        - El palacio de la luna - Paul Auster
        - Los detectives salvajes - Roberto Bolaño
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 Personas bacanes que sigo:
        **Data Science + Salud:**
        - [Paulo Villaroel](https://www.linkedin.com/in/paulovillarroel/) - Enfermero y data scientist, comparte mucho sobre ML aplicado a salud, un crack.
        
        **Tech + Carrera:**
        - [Nicolás Gómez](https://www.linkedin.com/in/codewithnico/) - Tips sobre trabajar para el extranjero, escribe harto por linkedin y me hace pensar.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 2rem 0;'>
    <p>Hecho con ❤️ por Trixxie 👽 usando Streamlit | © 2025 Mi Blog Tech</p>
</div>
""", unsafe_allow_html=True)
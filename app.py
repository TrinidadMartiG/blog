import streamlit as st
import json
import datetime
from pathlib import Path
from posts import posts

# Configuración de la página
st.set_page_config(
    page_title="Blog",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Sistema de comentarios
def cargar_comentarios(post_id):
    """Cargar comentarios desde archivo JSON"""
    comments_dir = Path("comments")
    comments_dir.mkdir(exist_ok=True)
    comments_file = comments_dir / f"{post_id}.json"
    
    if comments_file.exists():
        try:
            with open(comments_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_comentarios(post_id, comentarios):
    """Guardar comentarios en archivo JSON"""
    comments_dir = Path("comments")
    comments_dir.mkdir(exist_ok=True)
    comments_file = comments_dir / f"{post_id}.json"
    
    with open(comments_file, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=2)

def mostrar_comentarios(post_id):
    """Mostrar sistema de comentarios para un post"""
    # Cargar comentarios existentes
    comentarios = cargar_comentarios(post_id)
    
    # Header de comentarios con contador
    if comentarios:
        st.markdown(f"### 💬 Comentarios ({len(comentarios)})")
    else:
        st.markdown("### 💬 Comentarios")
    
    # Botón para mostrar/ocultar formulario de comentarios
    key_mostrar_form = f"mostrar_form_{post_id}"
    if key_mostrar_form not in st.session_state:
        st.session_state[key_mostrar_form] = False
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state[key_mostrar_form]:
            if st.button("✍️ Escribir comentario", use_container_width=True, key=f"btn_escribir_{post_id}"):
                st.session_state[key_mostrar_form] = True
                st.rerun()
        else:
            if st.button("❌ Cancelar", use_container_width=True, key=f"btn_cancelar_{post_id}"):
                st.session_state[key_mostrar_form] = False
                st.rerun()
    
    # Mostrar formulario solo si está activado
    if st.session_state[key_mostrar_form]:
        st.markdown("---")
        with st.form(f"comment_form_{post_id}", clear_on_submit=True):
            st.markdown("**💭 Comparte tu opinión:**")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                nombre = st.text_input("Tu nombre:", placeholder="¿Cómo te llamas?")
            with col2:
                email = st.text_input("Email (opcional):", placeholder="tu@email.com")
            
            comentario = st.text_area(
                "Tu comentario:", 
                placeholder="¿Qué opinas de este post? ¿Tienes alguna experiencia similar?",
                height=100
            )
            
            col_submit1, col_submit2 = st.columns(2)
            with col_submit1:
                submitted = st.form_submit_button("💬 Enviar comentario", use_container_width=True)
            with col_submit2:
                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                    st.session_state[key_mostrar_form] = False
                    st.rerun()
            
            if submitted:
                if nombre.strip() and comentario.strip():
                    nuevo_comentario = {
                        "id": len(comentarios) + 1,
                        "nombre": nombre.strip(),
                        "email": email.strip() if email.strip() else None,
                        "comentario": comentario.strip(),
                        "fecha": datetime.datetime.now().isoformat(),
                        "fecha_display": datetime.datetime.now().strftime("%d/%m/%Y a las %H:%M")
                    }
                    comentarios.append(nuevo_comentario)
                    guardar_comentarios(post_id, comentarios)
                    st.session_state[key_mostrar_form] = False  # Ocultar formulario después de enviar
                    st.success("¡Gracias por tu comentario! 🎉")
                    st.rerun()
                else:
                    st.error("Por favor completa tu nombre y comentario 😊")
    
    # Mostrar comentarios existentes
    if comentarios:
        st.markdown("---")
        for comment in reversed(comentarios):  # Más recientes primero
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 1.2rem; 
                border-radius: 12px; 
                margin: 1rem 0; 
                border-left: 4px solid #667eea;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            '>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;'>
                    <strong style='color: #2c3e50; font-size: 1.1rem;'>👤 {comment['nombre']}</strong>
                    <small style='color: #6c757d; font-size: 0.9rem;'>📅 {comment['fecha_display']}</small>
                </div>
                <div style='color: #495057; line-height: 1.6; font-size: 1rem;'>
                    {comment['comentario']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("---")
        st.markdown("*Sé el primero en comentar! 🚀*")

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
    
    # Agregar sistema de comentarios
    st.markdown("---")
    post_id = getattr(post_module, "__name__", "unknown").replace("posts.", "")
    mostrar_comentarios(post_id)
    
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
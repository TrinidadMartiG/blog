# 🌸 Blog - Trixxie en el mundo tech

Blog minimalista desarrollado con Streamlit, enfocado en tecnología, desarrollo y reflexiones personales.

## 🚀 Demo en vivo

**[👉 Ver el blog en acción](https://tu-blog.streamlit.app](https://trixie-blog.streamlit.app/)**

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Styling:** CSS personalizado + config.toml
- **Hosting:** Streamlit Community Cloud
- **Version Control:** Git + GitHub

## 📋 Estructura del proyecto

```markdown
blog/
├── 🐍 app.py                    # Aplicación principal de Streamlit
├── ⚙️  .streamlit/
│   └── config.toml              # Configuración personalizada de CSS
├── 📚 posts/
│   ├── __init__.py              # Registro y lista de posts disponibles
│   ├── p1.py                    # Post: "¿Por qué crear este blog?"
│   └── p2.py                    # Post: "Mi primer cliente y Streamlit"
├── 🖼️  media/                    # Imágenes y recursos multimedia
└── 📦 requirements.txt          # Dependencias del proyecto
```

## 📝 Agregar nuevos posts

1. Crea un nuevo archivo en `/posts/` (ej: `p3.py`)
2. Sigue la estructura:

```python
import streamlit as st

META = {
    "title": "Título de tu post",
    "date": "2025-01-16",
    "tags": ["tag1", "tag2", "tag3"],
}

def show_post():
    st.markdown("""
    ### Tu contenido aquí
    
    Escribe tu post en markdown...
    """)
```

3. Agrega el post a `/posts/__init__.py`:

```python
from . import p1, p2, p3  # Agregar p3

posts = [p1, p2, p3]  # Agregar a la lista
```
## 🚀 Deploy rápido de streamlit

### Opción 1: Streamlit Community Cloud

1. Sube tu código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio y deployea

### Opción 2: Local

```bash
# Clonar el repositorio
git clone https://github.com/TrinidadMartiG/blog.git
cd blog

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
streamlit run app.py
```

**Hecho con ❤️ y ☕ usando Streamlit**

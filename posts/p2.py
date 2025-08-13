import streamlit as st

META = {
    "title": "Levantando una mini App con Streamlit",
    "date": "2025-08-13",
    "tags": ["streamlit", "data", "python"],
}
def show_post():
    st.image("./media/screen1.png", width=500)
    st.markdown(
        """
        ### ¿Conocias Streamlit (https://streamlit.io/)?
        Streamlit es una librería de python, open source, para crear aplicaciones de una manera súper sencilla y tiene una particularidad genial, puede autohostearse.
        Es solo python, markdown, y conocer los componentes de la librería. Te permite levantar rapidamente un entorno de desarrollo, local, testear y desplegar desde
        texto hasta renderizaciones de dashboards corriendo pandas o cualquier libreria de python.

        Conocí esta librería hace 1 año cuando me pidieron ayuda para simplificar el proceso de evaluación de dosis farmaceuticas en un hospital del pais.
        La idea era uníficar en un solo lugar herramientas que estaban distribuidas entre app webs que calculaban solo una métrica, pasar estos resultados a formularios en excel internos
        para continuar pingponeando los valores entre diferentes formularios.
    
        No había mucho presupuesto para una arquitectura compleja, ni pagar un servidor, la idea era que fuese lo más ligéro posible, al fin de cuentas, surgia como motivación del equipo y se pagaba del bolsillo de ellos.
        Streamlit en ese sentido fue una solución increible. Github pages era otra opción, y podría  haber sido útil de haber requerido algo mucho más robusto,
        sin embargo requería mayor desarrollo en todo sentido, por lo que fue descartada.
        
        Todo con una estetica muy Notion-esque, a la que estamos ya tan acostumbrados en estos días jajaja :), pero también soporta css custom si lo deseas.

        Como se conecta directamente con tu github, se actualiza y deployea automaticamente en cosa de minutos, lo que lo hace genial para crear un mvp, crear visualizaciones o simplemente escribir un blog de lo que se te pase por la cabeza.

        
        """
    )
    
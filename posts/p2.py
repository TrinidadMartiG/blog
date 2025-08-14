import streamlit as st

META = {
    "title": "Mi primer cliente y una mini App con Streamlit",
    "date": "2025-08-13",
    "tags": ["streamlit", "data", "python"],
}
def show_post():
    st.markdown(
        """
        **Así por azar me refirieron un cliente. Nunca me había enfrentado a un cliente real, fuera de los que tengo en la pega. Bien nerviosa fuí nomás, algo en limpio podría sacar.**

        Me pidieron ayuda para simplificar el proceso de evaluación de dosis farmacéuticas para un equipo de farmacéuticos clínicos de un hospital público. 

        **El problema era súper claro:** el proceso estaba fragmentado y saltaban de una solución a otra - una app web para un valor, pasar el resultado a su excel interno, contrastar con otras calculadoras en línea, así pingponeando entre varios recursos. El excel lo tenían en físico en distintos computadores, ni hablar de cuando cambiaban a la versión_final_estasiquesi. Funcionaba bien, pero era engorroso.

        La idea era unificar en un solo lugar las herramientas necesarias.

        **Los requisitos eran claros pero limitantes:** no había mucho presupuesto para una arquitectura compleja, no querían pagar un servidor, y necesitaba ser lo más ligero posible. Al fin de cuentas, surgía como motivación del equipo y se pagaba del bolsillo de ellos. Eso sí, que estuviera en línea y fuese accesible desde cualquier dispositivo.**
        
        #### Streamlit al rescate

        Conocí esta librería poco tiempo antes que apareciera este proyecto, y fue la oportunidad perfecta para ver qué onda.
        Streamlit es una librería de Python, open source, para crear aplicaciones de una manera súper sencilla. Su particularidad genial: puede autohostearse.

        Es solo Python. Te permite levantar rápidamente 
        un entorno de desarrollo, te ofrece un front minimalista pero funcional, 
        puedes correr pandas o cualquier librería de python, crear graficos interactivos, dashboards completos, etc.
        
        GitHub Pages era otra opción (recordemos que no había presupuesto y buscaban un mvp), que es más customizable pero requería mayor desarrollo en general.
        Con Streamlit podía enfocarme 100% en la lógica de los cálculos. No es revolucionario ni nada,
        pero es una herramienta que me resultó muy útil para este proyecto.
        
        Todo con una estética muy Notion-esque, a la que estamos ya tan acostumbrados en estos días jajaja :), pero también soporta css custom si lo deseas.
        Como se conecta directamente con tu github, se actualiza y deployea automáticamente en cosa de minutos, lo que lo hace genial para crear un mvp, crear visualizaciones o simplemente escribir un blog de lo que se te pase por la cabeza.

        #### ¿En qué quedó todo?

        **Tech Stack:** Python, Pandas, Streamlit, Git
        - Calcula dosis de antibióticos para pacientes, según métricas antropométricas.
        - Calcula dosis seguras de fármacos según funcionamiento renal.
        - Calcula el área bajo la curva de concentración plasmática al ser administrado en múltiples dosis.
                    
        **Objetivo:**
        - Facilitar la toma de decisiones clínicas.
        - Ahorrar tiempo del equipo al centralizar cálculos en una sola herramienta.
        - Crear una app sencilla, rápida, responsive, que se pueda usar en cualquier dispositivo.

        **Resultado:**
        - Una mini app sumamente sencilla, pero de gran utilidad para el equipo.
        - Cálculos más que requete contra validados por el equipo para asegurar la precisión y confiabilidad de los cálculos.
        - Una Trixita emocionada y feliz por haber resuelto un problema a mi primer client freelance.

        **Problemas:**
        - Las apps hosteadas por streamlit en plan gratuito se bajan a las 48hrs sin tráfico, 
        por lo que cada lunes debia levantarla de nuevo. Solución sencilla? Crear un github para ellos, forkear mi repo,
        así en caso que se cayera pueden levantarla con tan solo un clic, simple, sencillo, feo jajajaja, pero eficaz.
                    
        #### Y que tal?

        Genial. Cliente feliz, yo feliz. Ver cómo una herramienta que hice les ahorraba tiempo real fue súper gratificante. Y yo aprendí que a veces la solución más simple es la que funciona.

        [Puedes verla acá](https://nebulacalculator-djwfefdgbt2gwixd7ffkst.streamlit.app/) (Pero recuerda es solo una mini app, no es nada para presumir)

        Saluditos :D
        """
    )

    
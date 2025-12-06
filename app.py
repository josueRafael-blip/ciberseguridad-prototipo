# archivo: app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# --- 🎨 Configuraciones de Página y Estilo ---
st.set_page_config(
    page_title="Detector de Enlaces Peligrosos - Seguridad Digital",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para aumentar la legibilidad
st.markdown("""
<style>
    /* Estilo general del cuerpo para mejor contraste y tamaño de letra */
    body {
        font-family: sans-serif;
    }
    .stApp {
        background-color: #f0f2f6; /* Un color de fondo suave */
    }
    /* Aumentar el tamaño de letra de los títulos y textos */
    h1, h2, h3, .stMarkdown {
        font-size: 1.5em !important;
    }
    /* Ajuste para el título principal */
    .stTitle {
        font-size: 2.2em !important; 
        color: #0072b5; /* Azul que inspira confianza */
        text-align: center;
        padding-bottom: 10px;
    }
    /* Estilo para la entrada de texto y el botón */
    .stTextInput>div>div>input, .stButton>button {
        font-size: 1.2em !important;
        padding: 10px !important;
    }
    /* Estilo específico para el botón principal */
    .stButton>button {
        background-color: #4CAF50; /* Verde amigable */
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    /* Mejorar la tabla de datos */
    .stDataFrame {
        font-size: 1.1em !important;
    }
</style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------

# --- 🛡️ Sección Principal y Explicativa ---
st.title("🚨 Detector de Enlaces Peligrosos: ¡Navega Seguro!")
st.markdown("---")

st.info("**¡Bienvenido!** Esta herramienta te ayuda a verificar si un enlace (dirección de internet) es seguro antes de hacer clic. **Tu seguridad es nuestra prioridad.**")

st.subheader("❓ ¿Cómo usarlo?")
st.markdown(
    """
    1. **Copia** el enlace sospechoso (ej: `https://...`).
    2. **Pégalo** en la caja de abajo.
    3. Presiona el botón **'Analizar Enlace'**.
    """
)

# --- Entrada y Lógica de Análisis ---
st.subheader("🔗 1. Pegue el Enlace Aquí:")
url = st.text_input("Ejemplo: https://www.enlace-sospechoso.com/login", key="url_input", label_visibility="collapsed")

# Función simple de análisis (puede reemplazarse por tu modelo real)
def analizar_enlace(link):
    # Palabras comunes usadas en phishing para engañar (ej: pedir datos urgentes)
    palabras_sospechosas = ["free", "login", "secure", "banking", "verify", "update", "password", "urgente"]
    alerta = any(palabra in link.lower() for palabra in palabras_sospechosas)
    
    # También revisamos si el enlace es muy corto o tiene muchos números (común en acortadores maliciosos)
    if len(link) < 25 or any(char.isdigit() for char in link):
         alerta = True 
         
    return alerta

# Almacenar resultados en dataframe
if "reportes" not in st.session_state:
    # Ajustamos los nombres de las columnas para ser más claros
    st.session_state.reportes = pd.DataFrame(columns=["Enlace Revisado", "Resultado de Alerta", "Fecha y Hora"])

# Botón de análisis
if st.button("🔍 Analizar Enlace Ahora", use_container_width=True):
    if url:
        with st.spinner('Analizando... por favor, espere un momento.'):
            peligro = analizar_enlace(url)
            
            if peligro:
                mensaje = "⚠️ ¡ATENCIÓN, PELIGROSO! - No haga clic."
                # Usamos una estructura de alerta más grande y roja para el peligro
                st.error(
                    f"## {mensaje}"
                )
                st.markdown(
                    """
                    **Recomendación:** Este enlace tiene características sospechosas. **¡No lo abra!** Podría ser un intento de robo de información (Phishing).
                    """
                )
            else:
                mensaje = "✅ ¡ENLACE SEGURO! - Puede hacer clic con confianza."
                # Usamos una estructura de éxito amigable y verde para la seguridad
                st.success(
                    f"## {mensaje}"
                )
                st.markdown(
                    """
                    **¡Felicidades!** Este enlace parece ser seguro. Siempre navegue con precaución.
                    """
                )
            
            # Guardar en reporte
            nuevo_registro = {
                "Enlace Revisado": url,
                "Resultado de Alerta": mensaje,
                "Fecha y Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Usamos pd.concat con un nuevo DataFrame
            nuevo_df = pd.DataFrame([nuevo_registro])
            st.session_state.reportes = pd.concat([st.session_state.reportes, nuevo_df], ignore_index=True)
            
    else:
        st.warning("Por favor, **pegue el enlace** en la casilla de arriba para empezar el análisis.")

st.markdown("---")

# --- Reporte Histórico ---
st.subheader("📋 Historial de Enlaces Analizados")
if not st.session_state.reportes.empty:
    # Mostramos el reporte en orden inverso (lo más nuevo arriba)
    st.dataframe(st.session_state.reportes.sort_values(by="Fecha y Hora", ascending=False), use_container_width=True)
else:
    st.info("Aún no ha analizado ningún enlace. Su historial aparecerá aquí.")

# Botón para descargar reporte
csv = st.session_state.reportes.to_csv(index=False).encode('utf-8')
st.download_button(
    "⬇️ Descargar mi Reporte de Seguridad (CSV)", 
    data=csv, 
    file_name="reporte_seguridad_enlaces.csv", 
    mime="text/csv",
    key="download_button"
)

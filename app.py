# archivo: app.py (Versión 4.0: Solución de Contraste y Legibilidad)
import streamlit as st
import pandas as pd
from datetime import datetime

# --- ⚙️ CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Detector de Enlaces Seguros",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 🎨 ESTILO CSS CORREGIDO Y FINALIZADO ---
st.markdown("""
<style>
    /* 1. Fondo simple y limpio */
    .stApp {
        background-color: #ffffff; /* Fondo blanco puro */
        color: #333333; /* Color de texto base: Gris muy oscuro */
    }
    
    /* 2. Aumentar tamaño de texto general para mejor legibilidad */
    html, body, .stMarkdown, .stText, .stDataFrame, .stInfo {
        font-size: 1.1em !important; 
        color: #333333; /* Aseguramos que el texto normal sea oscuro */
    }
    
    /* 3. Estilo para el Título Principal (CORRECCIÓN CLAVE AQUÍ) */
    h1.st-emotion-cache-18x43rd { /* Selector del título principal */
        font-size: 2.5em !important; 
        color: #004d99 !important; /* Azul oscuro fuerte y visible */
        text-align: center;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    
    /* 4. Estilo para los Subtítulos (CORRECCIÓN CLAVE AQUÍ) */
    h2, h3 { 
        font-size: 1.8em !important; 
        color: #333333 !important; /* Color oscuro para todos los subtítulos */
    }

    /* 5. Entrada de Texto (URL) */
    .stTextInput>div>div>input {
        font-size: 1.2em !important;
        padding: 15px !important;
        border: 2px solid #ccc; 
        border-radius: 10px;
        background-color: #f7f7f7; 
        color: #111111; /* Aseguramos que el texto dentro del input sea muy oscuro */
    }
    
    /* 6. Estilo del Botón de Análisis */
    .stButton>button {
        background-color: #00a651; 
        color: white;
        border-radius: 10px;
        font-size: 1.3em !important;
        padding: 10px 20px !important;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* 7. Asegurar que las listas (instrucciones) se vean oscuras */
    li {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------

# --- 🎯 CABECERA Y GUÍA SIMPLE ---

# Logo/Icono Grande y Título
st.markdown("<h1 style='text-align: center; color: #cc0000;'>🛡️ Alerta de Seguridad Digital</h1>", unsafe_allow_html=True)
st.title("Verificador de Enlaces")

st.markdown("---")

st.info("✅ **Propósito:** Esta herramienta fue diseñada para ayudarte a **evitar fraudes** en Internet. Simplemente verifica aquí cualquier enlace que te parezca sospechoso o urgente.")

st.subheader("💡 1. ¿Cómo Usar el Verificador?")
st.markdown(
    """
    1. **Copie** el enlace (dirección web) que le hace dudar.
    2. **Péguelo** en la caja gris de abajo.
    3. Presione el botón **'Verificar Enlace Ahora'**.
    """
)

# --- ENTRADA Y LÓGICA DE ANÁLISIS ---

st.subheader("🔍 2. Pegue el Enlace Aquí:")
url = st.text_input("Ejemplo: https://www.banco-urgente.com/login", key="url_input", label_visibility="collapsed")

# Función simple de análisis (la dejamos igual)
def analizar_enlace(link):
    palabras_sospechosas = ["free", "login", "secure", "banking", "verify", "update", "password", "urgente"]
    alerta = any(palabra in link.lower() for palabra in palabras_sospechosas)
    
    if len(link) < 25 or any(char.isdigit() for char in link.split('/')[2]):
         alerta = True 
         
    return alerta

# Almacenar resultados en dataframe
if "reportes" not in st.session_state:
    st.session_state.reportes = pd.DataFrame(columns=["Enlace Revisado", "Resultado", "Fecha y Hora"])

# Botón de análisis
if st.button("Verificar Enlace Ahora", use_container_width=True):
    if url:
        with st.spinner('Analizando el enlace, espere un momento...'):
            peligro = analizar_enlace(url)
            
            if peligro:
                mensaje = "⚠️ ¡MUCHO CUIDADO, ES PELIGROSO! 🛑"
                st.error(
                    f"## {mensaje}"
                )
                st.markdown(
                    """
                    **🔴 RECOMENDACIÓN URGENTE:** **¡NO HAGA CLIC!** Este enlace presenta riesgos de fraude (Phishing). Cierre la ventana o elimine el mensaje donde lo recibió.
                    """
                )
            else:
                mensaje = "✅ ¡ENLACE SEGURO! 👍"
                st.success(
                    f"## {mensaje}"
                )
                st.markdown(
                    """
                    **🟢 Navegación Segura:** Este enlace parece confiable. **Puede hacer clic con tranquilidad.** (Recuerde siempre verificar quién le envió el enlace).
                    """
                )
            
            # Guardar en reporte
            nuevo_registro = {
                "Enlace Revisado": url,
                "Resultado": mensaje,
                "Fecha y Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            nuevo_df = pd.DataFrame([nuevo_registro])
            st.session_state.reportes = pd.concat([st.session_state.reportes, nuevo_df], ignore_index=True)
            
    else:
        st.warning("⚠️ **ATENCIÓN:** Por favor, pegue el enlace en la casilla antes de presionar el botón.")

st.markdown("---")

# --- REPORTE HISTÓRICO ---
st.subheader("🗓️ Historial de Mis Verificaciones")
if not st.session_state.reportes.empty:
    st.dataframe(
        st.session_state.reportes.sort_values(by="Fecha y Hora", ascending=False), 
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Su historial de enlaces revisados aparecerá aquí una vez que realice su primera verificación.")

# Botón de descarga
csv = st.session_state.reportes.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Descargar Reporte Completo (CSV)", 
    data=csv, 
    file_name="reporte_seguridad_digital.csv", 
    mime="text/csv",
    key="download_button"
)

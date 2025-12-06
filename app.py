# archivo: app.py (Versión 3.0: Limpia y de Alto Contraste)
import streamlit as st
import pandas as pd
from datetime import datetime

# --- ⚙️ CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Detector de Enlaces Seguros",
    page_icon="✅",
    layout="centered", # Centrado para enfocarse en el contenido principal
    initial_sidebar_state="collapsed"
)

# --- 🎨 ESTILO CSS MEJORADO Y SIMPLIFICADO ---
# Se eliminaron estilos complejos para centrarse en legibilidad (alto contraste)
st.markdown("""
<style>
    /* 1. Fondo simple y limpio */
    .stApp {
        background-color: #ffffff; /* Fondo blanco puro */
    }
    
    /* 2. Aumentar tamaño de texto general para mejor legibilidad */
    html, body, .stMarkdown, .stText, .stDataFrame {
        font-size: 1.1em !important; 
    }
    
    /* 3. Estilo para el Título Principal */
    .stTitle {
        font-size: 2.5em !important; 
        color: #004d99; /* Azul oscuro fuerte para autoridad y confianza */
        text-align: center;
        margin-bottom: 0px;
        padding-top: 10px;
    }

    /* 4. Entrada de Texto (URL) */
    .stTextInput>div>div>input {
        font-size: 1.2em !important;
        padding: 15px !important;
        border: 2px solid #ccc; /* Borde visible */
        border-radius: 10px;
        background-color: #f7f7f7; /* Gris claro para destacar el campo */
    }
    
    /* 5. Estilo del Botón de Análisis */
    .stButton>button {
        background-color: #00a651; /* Verde fuerte para acción positiva */
        color: white;
        border-radius: 10px;
        font-size: 1.3em !important;
        padding: 10px 20px !important;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Sombra para que destaque */
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #007f3d; /* Oscurecer al pasar el ratón */
    }
    
    /* 6. Mejorar la Apariencia de la Tabla (DataFrame) */
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 8px;
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

# Función simple de análisis (la dejaremos igual para el prototipo)
def analizar_enlace(link):
    palabras_sospechosas = ["free", "login", "secure", "banking", "verify", "update", "password", "urgente"]
    alerta = any(palabra in link.lower() for palabra in palabras_sospechosas)
    
    # Marcamos como peligroso si el enlace es muy corto (acortadores) o tiene palabras clave
    if len(link) < 25 or any(char.isdigit() for char in link.split('/')[2]): # Revisa números en el dominio
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
                # Alerta roja y grande con ícono de peligro
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
                # Alerta verde y grande con ícono de seguridad
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
        # Ocultar el índice por defecto para una tabla más limpia
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

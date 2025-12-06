# archivo: app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# Título
st.title("🛡️ Prototipo de Ciberseguridad - Analizador de Enlaces")

# Entrada de enlace
url = st.text_input("Ingresa el enlace que deseas analizar:")

# Función simple de análisis (puede reemplazarse por tu modelo real)
def analizar_enlace(link):
    palabras_sospechosas = ["free", "login", "secure", "banking", "verify"]
    alerta = any(palabra in link.lower() for palabra in palabras_sospechosas)
    return alerta

# Almacenar resultados en dataframe
if "reportes" not in st.session_state:
    st.session_state.reportes = pd.DataFrame(columns=["Enlace", "Alerta", "Fecha"])

# Botón de análisis
if st.button("Analizar Enlace"):
    if url:
        peligro = analizar_enlace(url)
        mensaje = "⚠️ Peligroso" if peligro else "✅ Seguro"
        st.warning(mensaje) if peligro else st.success(mensaje)
        
        # Guardar en reporte
        nuevo_registro = {
            "Enlace": url,
            "Alerta": mensaje,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.reportes = st.session_state.reportes.append(nuevo_registro, ignore_index=True)

# Mostrar reporte
st.subheader("📄 Reporte de Enlaces Analizados")
st.dataframe(st.session_state.reportes)

# Botón para descargar reporte
csv = st.session_state.reportes.to_csv(index=False).encode('utf-8')
st.download_button("Descargar Reporte CSV", data=csv, file_name="reporte_enlaces.csv", mime="text/csv")

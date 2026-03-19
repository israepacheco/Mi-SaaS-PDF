

import streamlit as st
import fitz  # PyMuPDF para extraer texto
from pdf2docx import Converter # Para convertir a Word
import os

# Configuración visual de la página
st.set_page_config(page_title="PDF Magic Converter", page_icon="📄", layout="centered")

st.title("📄 PDF a Word & Buscador Inteligente")
st.markdown("Sube tu archivo y conviértelo en segundos.")

# --- 1. CARGA DE ARCHIVO ---
archivo_pdf = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

if archivo_pdf is not None:
    # Guardar el PDF temporalmente para procesarlo
    nombre_pdf = "temporal.pdf"
    with open(nombre_pdf, "wb") as f:
        f.write(archivo_pdf.getbuffer())
    
    st.success("✅ PDF cargado correctamente.")

    # --- 2. BOTONES DE ACCIÓN ---
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Convertir a Word (.docx)"):
            with st.spinner("Convirtiendo..."):
                nombre_word = "documento_convertido.docx"
                cv = Converter(nombre_pdf)
                cv.convert(nombre_word, start=0, end=None)
                cv.close()
                
                with open(nombre_word, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar Word",
                        data=f,
                        file_name="Mi_Documento.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            st.balloons()

    with col2:
        if st.button("📝 Extraer Texto (.txt)"):
            doc = fitz.open(nombre_pdf)
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            
            # Guardamos el texto en la "memoria" de la sesión para el buscador
            st.session_state['texto_extraido'] = texto_completo
            
            st.download_button(
                label="⬇️ Descargar TXT",
                data=texto_completo,
                file_name="Mi_Texto.txt",
                mime="text/plain"
            )
            st.info("Texto extraído con éxito.")

    # --- 3. MOTOR DE BÚSQUEDA INTELIGENTE ---
    st.divider()
    st.subheader("🔍 Buscador en el Documento")
    
    if 'texto_extraido' in st.session_state:
        busqueda = st.text_input("¿Qué palabra o frase deseas encontrar?")
        
        if busqueda:
            texto = st.session_state['texto_extraido']
            if busqueda.lower() in texto.lower():
                # Buscamos las líneas donde aparece la palabra
                lineas = texto.split('\n')
                coincidencias = [l.strip() for l in lineas if busqueda.lower() in l.lower()]
                
                st.write(f"Se encontraron **{len(coincidencias)}** resultados:")
                for c in coincidencias[:10]: # Muestra los primeros 10 resultados
                    st.warning(f"... {c} ...")
            else:
                st.error("No se encontraron coincidencias en el documento.")
    else:
        st.caption("Primero haz clic en 'Extraer Texto' para activar el buscador.")
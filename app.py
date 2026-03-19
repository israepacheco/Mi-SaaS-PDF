

import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="PDF Smart Search", page_icon="📄")
st.title("📄 Buscador Inteligente en PDF")

archivo_pdf = st.file_uploader("Sube tu PDF aquí", type=["pdf"])

if archivo_pdf:
    with open("temp.pdf", "wb") as f:
        f.write(archivo_pdf.getbuffer())
    
    # Extraer texto
    doc = fitz.open("temp.pdf")
    texto = "".join([pagina.get_text() for pagina in doc])
    st.session_state['texto'] = texto
    st.success("✅ Texto extraído. Ya puedes buscar.")

    st.divider()
    busqueda = st.text_input("🔍 ¿Qué palabra buscas?")
    if busqueda and 'texto' in st.session_state:
        txt = st.session_state['texto']
        if busqueda.lower() in txt.lower():
            coincidencias = [linea for linea in txt.split('\n') if busqueda.lower() in linea.lower()]
            for c in coincidencias[:10]:
                st.info(f"... {c} ...")
        else:
            st.error("No se encontraron resultados.")

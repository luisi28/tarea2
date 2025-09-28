# streamlit_app.py
import streamlit as st
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Revista SQP - Scraper", layout="wide")

st.title("📚 Revista de la Sociedad Química del Perú")
st.write("Aplicación para explorar artículos usando el protocolo **OAI-PMH** de la revista SQP.")

# URL del endpoint OAI de la revista
OAI_URL = "https://revistas.sqp.org.pe/index.php/sqp/oai"

def get_records():
    """Obtiene registros de artículos usando OAI-PMH (ListRecords)."""
    params = {
        "verb": "ListRecords",
        "metadataPrefix": "oai_dc"
    }
    response = requests.get(OAI_URL, params=params, timeout=30)
    if response.status_code != 200:
        st.error("No se pudo conectar con el servidor OAI de la revista.")
        return []
    root = ET.fromstring(response.content)

    ns = {
        "oai": "http://www.openarchives.org/OAI/2.0/",
        "dc": "http://purl.org/dc/elements/1.1/"
    }

    records = []
    for record in root.findall(".//oai:record", ns):
        title = record.find(".//dc:title", ns)
        creators = record.findall(".//dc:creator", ns)
        description = record.find(".//dc:description", ns)
        identifier = record.findall(".//dc:identifier", ns)

        records.append({
            "title": title.text if title is not None else "Sin título",
            "authors": ", ".join([c.text for c in creators]) if creators else "Desconocidos",
            "abstract": description.text if description is not None else "Sin resumen",
            "link": identifier[-1].text if identifier else ""
        })

    return records

st.subheader("Artículos disponibles")

if st.button("📥 Cargar artículos"):
    with st.spinner("Obteniendo artículos de la revista..."):
        articles = get_records()

    if articles:
        for art in articles:
            with st.expander(art["title"]):
                st.write(f"👨‍🔬 **Autores:** {art['authors']}")
                st.write(f"📝 **Resumen:** {art['abstract']}")
                if art["link"]:
                    st.markdown(f"[🔗 Enlace al artículo]({art['link']})")
    else:
        st.warning("No se encontraron artículos o no se pudo acceder al servidor.")


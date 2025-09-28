import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="SQP Web Scraper", layout="wide")

st.title("📚 Web Scraping - Revista Sociedad Química del Perú (SQP)")

# URL de archivo de números de la revista
url = "https://revistas.sqp.org.pe/index.php/rsqp/issue/archive"

st.write("Extrayendo artículos de:", url)

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    issues = soup.find_all("div", class_="obj_issue_summary")

    data = []
    for issue in issues:
        title = issue.find("h2").get_text(strip=True)
        link = issue.find("a")["href"]
        data.append({"Número/Volumen": title, "Enlace": link})

    df = pd.DataFrame(data)
    st.dataframe(df)

    option = st.selectbox("Selecciona un número para ver artículos:", df["Número/Volumen"])

    if option:
        link = df[df["Número/Volumen"] == option]["Enlace"].values[0]
        st.write("📖 Cargando artículos de:", link)

        resp_issue = requests.get(link)
        if resp_issue.status_code == 200:
            soup_issue = BeautifulSoup(resp_issue.text, "html.parser")
            articles = soup_issue.find_all("div", class_="obj_article_summary")

            articles_data = []
            for art in articles:
                title = art.find("div", class_="title").get_text(strip=True)
                authors = art.find("div", class_="authors").get_text(strip=True) if art.find("div", class_="authors") else "N/A"
                link_article = art.find("a")["href"]
                articles_data.append({
                    "Título": title,
                    "Autores": authors,
                    "Link": link_article
                })

            df_articles = pd.DataFrame(articles_data)
            st.dataframe(df_articles)
else:
    st.error("❌ No se pudo acceder a la página de la revista.")

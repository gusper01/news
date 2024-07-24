import feedparser
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Función para obtener noticias del feed RSS de Reuters
def get_news_from_rss(url):
    print(f"Fetching news from: {url}")
    try:
        # Configurar headers para la solicitud
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/xml'
        }

        # Realizar la solicitud GET al feed RSS
        response = requests.get(url, headers=headers)

        # Verificar el estado de la respuesta HTTP
        if response.status_code == 200:
            # Parsear el contenido XML del feed RSS
            root = ET.fromstring(response.content)
            news_list = []

            # Iterar sobre cada item (noticia) en el feed RSS
            for item in root.findall('.//item'):
                title = item.find('title').text
                link = item.find('link').text
                published_date = item.find('pubDate').text
                summary = item.find('description').text

                # Imprimir detalles de la noticia
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Published Date: {published_date}")
                print(f"Summary: {summary}\n")

                # Guardar los datos de la noticia en una lista
                news_list.append({
                    'Title': title,
                    'Link': link,
                    'Published Date': published_date,
                    'Summary': summary
                })

            # Crear un DataFrame de Pandas con los datos de las noticias
            df = pd.DataFrame(news_list)
            return df

        else:
            print(f"Failed to fetch RSS feed, status code: {response.status_code}")

    except Exception as e:
        print(f"Failed to fetch RSS feed: {e}")

    return None

# URL del feed RSS de Reuters
url = 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best'

# Obtener noticias del feed RSS y almacenarlas en un DataFrame
news_df = get_news_from_rss(url)

# Mostrar el DataFrame si se obtuvieron noticias correctamente
if news_df is not None:
    print("\nDataFrame:")
    print(news_df.head())  # Mostrar las primeras filas del DataFrame
else:
    print("No se pudieron obtener datos del RSS feed.")

# Lista de feeds RSS (podemos agregar más feeds aquí)
rss_feeds = [
    ('https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best', 'Reuters'),
    # Añade más feeds RSS aquí si es necesario
]

# Obtener noticias de todos los feeds RSS
all_news = []
for url, source_name in rss_feeds:
    news_df, source = get_news_from_rss(url), source_name
    if news_df is not None:
        all_news.append((news_df, source))
    else:
        print(f"Failed to fetch data for {source_name}.")
# Obtener la fecha actual
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Generar la página HTML
html_content = "<html><head><title>RSS News</title></head><body>"
html_content += f"<h1>RSS News Feed</h1><h3>Generated on: {current_date}</h3>"
for news_df, source in all_news:
    html_content += f"<h2>{source}</h2>"
    if not news_df.empty:
        df_html = news_df.to_html(index=False, escape=False)
        html_content += f"<h3>Data for {source}</h3>"  # Añadir encabezado para identificar cada sección
        html_content += df_html
    else:
        html_content += f"<p>No data available for {source}</p>"
html_content += "</body></html>"

# Verificar el contenido del HTML antes de guardarlo
print("HTML Content Preview:")
print(html_content[:2000])  # Imprime los primeros 2000 caracteres del HTML

# Guardar la página HTML
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

import feedparser
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Función para obtener noticias del feed RSS
def get_news_from_rss(url, limit=10):
    print(f"Fetching news from: {url}")
    try:
        if url == 'https://www.census.gov/economic-indicators/indicator.xml':
            # Usar feedparser para este feed específico
            feed = feedparser.parse(url)
            if feed.entries:
                news_list = []
                for entry in feed.entries[:limit]:
                    news = {}
                    news['Title'] = entry.title if 'title' in entry else 'N/A'
                    news['Link'] = entry.link if 'link' in entry else 'No link available'
                    news['Published Date'] = entry.published if 'published' in entry else 'N/A'
                    news['Summary'] = entry.summary if 'summary' in entry else 'N/A'
                    
                    # Convertir el título en un enlace si el enlace está disponible
                    if news['Link'] != 'No link available':
                        news['Title'] = f'<a href="{news["Link"]}" target="_blank">{news["Title"]}</a>'
                    
                    news_list.append(news)
                df = pd.DataFrame(news_list)
                return df

        elif url == 'https://www.sec.gov/news/pressreleases.rss':
            # Usar feedparser para este feed específico
            feed = feedparser.parse(url)
            if feed.entries:
                news_list = []
                for entry in feed.entries[:limit]:
                    news = {}
                    news['Title'] = entry.title if 'title' in entry else 'N/A'
                    news['Link'] = entry.link if 'link' in entry else 'No link available'
                    news['Published Date'] = entry.published if 'published' in entry else 'N/A'
                    news['Summary'] = entry.summary if 'summary' in entry else 'N/A'
                    
                    # Convertir el título en un enlace si el enlace está disponible
                    if news['Link'] != 'No link available':
                        news['Title'] = f'<a href="{news["Link"]}" target="_blank">{news["Title"]}</a>'
                    
                    news_list.append(news)
                df = pd.DataFrame(news_list)
                return df

        else:
            # Configurar headers para la solicitud
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36',
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
                for item in root.findall('.//item')[:limit]:
                    news = {}
                    news['Title'] = item.find('title').text if item.find('title') is not None else 'N/A'
                    news['Link'] = item.find('link').text if item.find('link') is not None else 'No link available'
                    news['Published Date'] = item.find('pubDate').text if item.find('pubDate') is not None else 'N/A'
                    news['Summary'] = item.find('description').text if item.find('description') is not None else 'N/A'

                    # Limpiar el texto del resumen
                    news['Summary'] = news['Summary'].replace('\n', ' ').replace('  ', ' ')

                    # Formatear la fecha publicada si está disponible
                    if news['Published Date'] != 'N/A':
                        news['Published Date'] = ' '.join(news['Published Date'].split()[:4])

                    # Convertir el título en un enlace si el enlace está disponible
                    if news['Link'] != 'No link available':
                        news['Title'] = f'<a href="{news["Link"]}" target="_blank">{news["Title"]}</a>'

                    # Agregar la noticia a la lista
                    news_list.append(news)

                # Crear un DataFrame de Pandas con los datos de las noticias
                df = pd.DataFrame(news_list)
                return df

            else:
                print(f"Failed to fetch RSS feed, status code: {response.status_code}")

    except Exception as e:
        print(f"Failed to fetch RSS feed: {e}")

    return None

# Lista de feeds RSS (podemos agregar más feeds aquí)
rss_feeds = [
    ('https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best', 'Reuters - Business Finance'),
    ('https://www.reutersagency.com/feed/?best-topics=tech&post_type=best', 'Reuters - Tech'),
    ('https://www.census.gov/economic-indicators/indicator.xml', 'Census - Economic Indicators'),
    ('https://www.sec.gov/news/pressreleases.rss', 'SEC - Press Releases'),
    # Añade más feeds RSS aquí si es necesario
]

# Obtener noticias de todos los feeds RSS
all_news = []
for url, source_name in rss_feeds:
    news_df = get_news_from_rss(url, limit=10)
    if news_df is not None:
        all_news.append((news_df, source_name))
        print(f"\nDataFrame for {source_name}:")
        print(news_df.head())  # Mostrar las primeras filas del DataFrame
    else:
        print(f"Failed to fetch data for {source_name}.")

# Obtener la fecha actual
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Generar la página HTML con Bootstrap
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSS News</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
    <h1 class="mt-4 mb-4">RSS News Feed</h1>
    <h3>Generated on: {current_date}</h3>
""".format(current_date=current_date)

# Agregar noticias con estilo Bootstrap
for news_df, source in all_news:
    html_content += f"""
    <div class='card mb-4'>
        <div class='card-header'>
            <h2>{source}</h2>
        </div>
        <div class='card-body'>
    """
    if not news_df.empty:
        df_html = news_df.drop(columns=['Link']).to_html(index=False, escape=False, classes='table table-striped')
        html_content += f"<div class='table-responsive'>{df_html}</div>"
    else:
        html_content += f"<p>No data available for {source}</p>"
    html_content += "</div></div>"

html_content += """
</div>
</body>
</html>
"""

# Verificar el contenido del HTML antes de guardarlo
print("HTML Content Preview:")
print(html_content[:2000])  # Imprime los primeros 2000 caracteres del HTML

# Guardar la página HTML
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

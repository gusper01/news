import feedparser
import pandas as pd
from datetime import datetime
import requests

# Función para obtener noticias del feed RSS
def get_news_from_rss(url, limit=10):
    print(f"Fetching news from: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
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
            print(f"No entries found in the feed: {url}")
    except Exception as e:
        print(f"Failed to fetch RSS feed: {e}")

    return None

# Lista de feeds RSS (podemos agregar más feeds aquí)
rss_feeds = [
    ('https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best', 'Reuters - Business Finance'),
    ('https://www.reutersagency.com/feed/?best-topics=tech&post_type=best', 'Reuters - Tech'),
    ('https://www.census.gov/economic-indicators/indicator.xml', 'Census - Economic Indicators'),
    ('https://www.sec.gov/news/pressreleases.rss', 'SEC - Press Releases'),
    ('https://www.cbsnews.com/latest/rss/moneywatch', 'CBS News - MoneyWatch'),
    ('https://www.wired.com/feed/tag/ai/latest/rss', 'Wired - AI'),
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

# Generar la página HTML con Bootstrap y estilo de consola
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSS News</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #1e1e1e;
            color: #00ff00;
            font-family: monospace;
        }}
        a {{
            color: #00ff00;
        }}
        .card-header {{
            background-color: #00ff00;
            color: #000000;
        }}
        .table-responsive {{
            margin-top: 20px;
        }}
        .card {{
            background-color: #2b2b2b;
        }}
        h1, h2, h3 {{
            color: #00ff00;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        ul li {{
            margin-bottom: 10px;
            list-style-type: none;
        }}
        table {{
            width: 100%;
        }}
        td {{
            vertical-align: top;
            padding: 5px;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1 class="mt-4 mb-4">RSS News Feed</h1>
    <h3>Generated on: {current_date}</h3>
    <h2>Table of Contents</h2>
    <table>
"""

# Agregar enlaces a la tabla de contenidos en dos columnas
half = (len(all_news) + 1) // 2
left_column = all_news[:half]
right_column = all_news[half:]

html_content += "<tr><td>"
for _, source in left_column:
    html_content += f'<li><a href="#{source.replace(" ", "_").replace("-", "_")}"><i class="fas fa-newspaper"></i> {source}</a></li>\n'
html_content += "</td><td>"
for _, source in right_column:
    html_content += f'<li><a href="#{source.replace(" ", "_").replace("-", "_")}"><i class="fas fa-newspaper"></i> {source}</a></li>\n'
html_content += "</td></tr>"

html_content += """
    </table>
"""

# Agregar las tablas de noticias
for news_df, source in all_news:
    html_content += f"""
    <div class='card mb-4' id='{source.replace(" ", "_").replace("-", "_")}'>
        <div class='card-header'>
            <h2 style="color: #000000;">{source}</h2>
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
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.min.js"></script>
</body>
</html>
"""

# Verificar el contenido del HTML antes de guardarlo
print("HTML Content Preview:")
print(html_content[:2000])  # Imprime los primeros 2000 caracteres del HTML

# Guardar la página HTML
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML file has been generated successfully.")

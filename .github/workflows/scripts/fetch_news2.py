import feedparser
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Función para obtener noticias desde un feed RSS usando feedparser
def fetch_news_from_rss(url, source_name):
    feed = feedparser.parse(url)
    news_items = []

    for entry in feed.entries:
        news_items.append({
            "Title": entry.title,
            "Link": entry.link,
            "Published Date": entry.published,
            "Summary": entry.summary
        })

    df = pd.DataFrame(news_items)
    print(f"Data fetched for {source_name}:")
    print(df.head())  # Imprimir el DataFrame para depuración
    return df, source_name

# Lista de feeds RSS
rss_feeds = [
    ('https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best', 'Reuters'),
    # Añade más feeds RSS aquí si es necesario
]

# Obtener noticias de todos los feeds RSS
all_news = []
for url, source_name in rss_feeds:
    news_df, source = fetch_news_from_rss(url, source_name)
    print(f"Appended news data for {source} with {len(news_df)} entries")  # Confirmar que se han añadido datos
    all_news.append((news_df, source))

# Generar la página HTML
html_content = "<html><head><title>RSS News</title></head><body>"
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

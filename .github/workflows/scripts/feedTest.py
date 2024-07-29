import feedparser
import logging
import time

# Configurar el registro para ver posibles errores
logging.basicConfig(level=logging.DEBUG)

def fetch_feed(url):
    try:
        # Intentar obtener el feed con un tiempo de espera de 10 segundos
        logging.info(f"Fetching RSS feed: {url}")
        feed = feedparser.parse(url)
        if feed.bozo:
            logging.error(f"Failed to parse RSS feed: {feed.bozo_exception}")
            return None
        if not feed.entries:
            logging.warning(f"No entries found in the feed: {url}")
            return None
        return feed
    except Exception as e:
        logging.error(f"Error fetching the RSS feed: {e}")
        return None

# URL del feed RSS de la IMF
sec_rss_url = 'https://www.imf.org/en/News/RSS?Language=ESL'

# Obtener el feed
feed = fetch_feed(sec_rss_url)

# Verificar si hay entradas en el feed
if feed and feed.entries:
    # Iterar sobre todas las entradas
    for entry in feed.entries:
        print("\nNueva Entrada:")
        for field in entry.keys():
            print(f"{field}: {entry[field]}")
else:
    print("No se encontraron entradas en el feed.")

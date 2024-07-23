import sys
import os

# Agregar la ruta del script al PYTHONPATH
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.github/workflows/scripts'))
sys.path.insert(0, script_path)

from fetch_news import get_news_from_rss

def test_get_news_from_rss():
    url = 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best'
    df = get_news_from_rss(url)
    assert not df.empty  # Ejemplo de prueba simple

if __name__ == "__main__":
    test_get_news_from_rss()

import pytest
from src.main import get_news_from_rss

def test_get_news_from_rss():
    url = 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best'
    df = get_news_from_rss(url)
    assert df is not None
    assert not df.empty

import feedparser
import pandas as pd
from datetime import datetime
import requests
from dateutil import parser

def format_date(date_str):
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime('%a, %d %b %Y')
    except (ValueError, TypeError):
        return date_str

def get_news_from_rss(url, limit=10):
    print(f"Fetching news from: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    if "imf.org" in url:
        # Para IMF, utilizamos feedparser directamente sin requests
        feed = feedparser.parse(url)
    else:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except Exception as e:
            print(f"Failed to fetch RSS feed with requests: {e}")
            return None
    
    if feed.entries:
        news_list = []
        for entry in feed.entries[:limit]:
            news = {}
            news['Title'] = entry.title if 'title' in entry else 'N/A'
            news['Link'] = entry.link if 'link' in entry else 'No link available'
            if 'published' in entry:
                news['Published Date'] = format_date(entry.published)
            elif 'cb_publicationdate' in entry:
                news['Published Date'] = format_date(entry.cb_publicationdate)
            elif 'updated' in entry:
                news['Published Date'] = format_date(entry.updated)
            elif 'pubDate' in entry:
                news['Published Date'] = format_date(entry.pubDate)
            else:
                news['Published Date'] = 'N/A'
            
            news['Summary'] = entry.summary if 'summary' in entry else 'N/A'
            news['Summary'] = news['Summary'].replace('\n', ' ').replace('  ', ' ')

            if news['Published Date'] != 'N/A':
                news['Published Date'] = ' '.join(news['Published Date'].split()[:4])
            if news['Link'] != 'No link available':
                news['Title'] = f'<a href="{news["Link"]}" target="_blank">{news["Title"]}</a>'
            
            news_list.append(news)
        df = pd.DataFrame(news_list)
        return df
    else:
        print(f"No entries found in the feed: {url}")

    return None

rss_feeds = [
    ('https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best', 'Reuters - Business Finance', '💼'),
    ('https://www.reutersagency.com/feed/?best-topics=tech&post_type=best', 'Reuters - Tech', '💻'),
    ('https://www.census.gov/economic-indicators/indicator.xml', 'US Census Bureau - Economic Indicators', '📊'),
    ('https://www.sec.gov/news/pressreleases.rss', 'SEC - Press Releases', '📜'),
    ('https://www.bis.org/doclist/reshub_papers.rss', 'BIS - Central Bank Research Hub', '🏛️'),
    ('https://money.com/money/feed/', 'Money - Financial News', '💰'),
    ('https://www.cbsnews.com/latest/rss/moneywatch', 'CBS News - MoneyWatch', '💰'),
    ('https://www.wired.com/feed/tag/ai/latest/rss', 'Wired - AI', '🤖'),
    ('https://finance.yahoo.com/news/rssindex', 'Yahoo - Finance', '💹'),
    ('https://feeds.bloomberg.com/politics/news.rss', 'Bloomberg - Politics', '🏛️'),
    ('https://feeds.bloomberg.com/technology/news.rss', 'Bloomberg - Technology', '🔧'),
    ('https://feeds.bloomberg.com/bview/news.rss', 'Bloomberg - Business View', '📈'),
    ('https://feeds.bloomberg.com/markets/news.rss', 'Bloomberg - Markets', '📉'),
    ('https://fortune.com/feed/fortune-feeds/?id=3230629', 'Fortune - Feeds', '💰'),
    ('https://www.imf.org/en/News/RSS?Language=ENG', 'IMF - International Monetary Fund', '🏛️')
]

all_news = []
for url, source_name, _ in rss_feeds:
    news_df = get_news_from_rss(url, limit=10)
    if news_df is not None:
        all_news.append((news_df, source_name))
        print(f"\nDataFrame for {source_name}:")
        print(news_df.head())
    else:
        print(f"Failed to fetch data for {source_name}.")

current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSS News</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #1e1e1e;
            color: white;
            font-family: monospace;
        }}
        a {{
            color: yellow;
        }}
        .card-header {{
            background-color: white;
            color: #000000;
        }}
        .table-responsive {{
            margin-top: 20px;
        }}
        .card {{
            background-color: #2b2b2b;
        }}
        h1, h2, h3 {{
            color: white;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            font-size: 1.5em;
        }}
        ul li {{
            margin-bottom: 10px;
            list-style-type: none;
        }}
        table {{
            width: 50%;
            margin: auto;
        }}
        td {{
            vertical-align: top;
            padding: 5px;
        }}
        .icon {{
            font-size: 1.5em;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1 class="mt-4 mb-4">RSS News Feed</h1>
    <h3>Generated on: {current_date}</h3>
    <table>
"""

half = (len(all_news) + 1) // 2
left_column = rss_feeds[:half]
right_column = rss_feeds[half:]

html_content += '<tr><td><ul class="list-unstyled">'
for _, source, icon in left_column:
    html_content += f'<li><span class="icon">{icon}</span> <a href="#{source.replace(" ", "_").replace("-", "_")}">{source}</a></li>\n'
html_content += '</ul></td><td><ul class="list-unstyled">'
for _, source, icon in right_column:
    html_content += f'<li><span class="icon">{icon}</span> <a href="#{source.replace(" ", "_").replace("-", "_")}">{source}</a></li>\n'
html_content += '</ul></td></tr>'

html_content += """
    </table>
"""

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

print("HTML Content Preview:")
print(html_content[:2000])

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML file created successfully.")

import requests
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

def fetch_news_articles(page):
    payload = {
        "action": "getArticles",
        "keyword": "terror attack",
        "ignoreSourceGroupUri": "paywall/paywalled_sources",
        "articlesPage": page,
        "articlesCount": 5,
        "articlesSortBy": "socialScore",
        "articlesSortByAsc": False,
        "dataType": ["news", "pr"],
        "resultType": "articles",
        "apiKey": os.environ['NEWSAPI_KEY']
    }
    response = requests.post(os.environ['NEWSAPI_URL'], json=payload)
    return response.json()
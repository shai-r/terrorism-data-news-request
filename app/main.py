import json
import time
from datetime import datetime

from app.repositories.elastic_repository import save_to_elasticsearch
from app.repositories.mongo_repository import save_to_mongo
from app.services.coordinates_service import get_coordinates
from app.services.groq_service import classify_article
from app.services.news_service import fetch_news_articles

TIME_SLEEP = 120

def get_location_for_news(city, country) -> dict:
    lat, lng = None, None
    location_data = get_coordinates(city, country)
    if location_data.get('results'):
        location = location_data['results'][0]
        lat = location['geometry']['lat']
        lng = location['geometry']['lng']
    return {"lat": lat, "lng": lng}


def fetch_and_classify_articles(page):
    articles = fetch_news_articles(page)
    if not articles.get('articles'):
        return []
    print(articles)
    print(articles.get('articles').get('results', []))
    return [
        process_article(article) for article in articles.get('articles').get('results', [])
    ]

def process_article(article):
    print(article)
    title = article.get('title', '')
    body = article.get('body', '')
    answer_groq = classify_article(f"{title} {body}")

    location = get_location_for_news(answer_groq['city'], answer_groq['country'])

    return {
        "title": title,
        "body": body,
        "category": answer_groq['category'],
        "date": answer_groq["date"],
        "lat": location["lat"],
        "lng": location["lng"],
        "timestamp": datetime.now().isoformat()
    }

def save_article_data(news_data):
    try:
        save_to_mongo(news_data)
        json_data = {**{k: v for k, v in news_data.items() if k != '_id'}, 'news_id': str(news_data['_id'])}
        save_to_elasticsearch(json.dumps(json_data))
    except TypeError as e:
        print(f"Error: {e}")


def process_and_save_articles(page):
    articles = fetch_and_classify_articles(page)
    if not articles:
        return False

    for article in articles:
        save_article_data(article)

    return True

def main():
    page = 1
    while True:
        print(f"Processing page {page}...")
        has_articles = process_and_save_articles(page)

        if not has_articles:
            print("No more articles found. Stopping...")

        print(f"Waiting for {TIME_SLEEP} seconds before fetching the next page...")
        time.sleep(TIME_SLEEP)
        page += 1

if __name__ == "__main__":
    main()

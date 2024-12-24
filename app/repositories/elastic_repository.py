import os

from dotenv import load_dotenv

from app.db.elasticsearch.database_elastic import es_client

load_dotenv(verbose=True)

def save_to_elasticsearch(data):
    if es_client.ping():
        response = es_client.index(
            index=os.environ['ES_INDEX'],
            document=data
        )
        return response
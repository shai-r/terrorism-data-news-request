import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch


load_dotenv(verbose=True)

es_client = Elasticsearch(
        os.environ['ES_HOST'],
        basic_auth=(os.environ["ES_USERNAME"], os.environ["ES_PASSWORD"]),
        verify_certs=False
    )
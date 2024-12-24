from app.db.mongodb.database_mongo import news_collection

def save_to_mongo(data):
    news_collection.insert_one(data)
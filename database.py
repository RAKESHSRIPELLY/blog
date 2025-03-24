from pymongo import MongoClient
MONGO_URI = "mongodb+srv://rakeshchary:rakesh@blog.4c71m.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "Blog"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
posts_collection = db['posts']
comments_collection = db['comments']
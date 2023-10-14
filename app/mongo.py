import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')
# # Create a MongoClient with the connection string
# client = pymongo.MongoClient(connection_string)
# # Access your database
# db = client["ChallengersDB"]

def insert_details(user_name, event_hashtag, link):
    try:
        # Create a MongoClient with the connection string
        client = pymongo.MongoClient(connection_string)
        # Access your database
        db = client["ChallengersDB"]

        print(f"Inserting data: {user_name}, {event_hashtag}, {link}")
        # Insert data into a collection
        collection = db["user_participation"]
        data = {"user_id": user_name, "event_id": event_hashtag, "link": link}
        collection.insert_one(data)

        print('Inserted!')

    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection to MongoDB Atlas failed: {e}")

    finally:
        client.close()

def fetch_details():
    
    try:
        # Create a MongoClient with the connection string
        client = pymongo.MongoClient(connection_string)
        # Access your database
        db = client["ChallengersDB"]
        collection = db["ChallengersCollection"]
        
        # Query data from a collection
        result = collection.find({"user_id": "aimanasif27#5888"})
        for document in result:
            print(document)

    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection to MongoDB Atlas failed: {e}")

    finally:
        client.close()

insert_details("user123", "event456", "https://www.example.com/participation")
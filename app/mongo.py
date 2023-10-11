# import pymongo
# from pymongo import MongoClient

# cluster=MongoClient("mongodb+srv://root:root@cluster0.krtgnvy.mongodb.net/?retryWrites=true&w=majority")
# db=cluster["ChallengersX"]
# collection=db["students"]
# #post={"_id":0,"name":"Aiman"}
# collection.insert_many([{"name":"xyz"},{"name":"abc"},{"name":"pqr"}])

import pymongo

# Replace this with your MongoDB Atlas connection string
connection_string = "mongodb+srv://root:root@cluster0.krtgnvy.mongodb.net/?retryWrites=true&w=majority"

try:
    # Create a MongoClient with the connection string
    client = pymongo.MongoClient(connection_string)

    # Access your database (replace 'mydatabase' with your actual database name)
    db = client["students"]

    # You can now interact with your MongoDB Atlas cluster through 'db'
    # For example, you can access collections, insert, update, and query data.

    # Example: Insert data into a collection
    collection = db["ChallengersCollection"]
    data = {"name": "Alice", "age": 25}
    collection.insert_one(data)

    # Query data from a collection
    result = collection.find({"name": "Alice"})
    for document in result:
        print(document)

except pymongo.errors.ConnectionFailure as e:
    print(f"Connection to MongoDB Atlas failed: {e}")

finally:
    client.close()

import os
import pymongo
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')

def register_user(event, email, name, discord_id):
    try:
        # Create a MongoClient with the connection string
        client = pymongo.MongoClient(connection_string)
        # Access your database
        db = client["ChallengersDB"]

        print(f"Inserting data: ")
        # Insert data into a collection
        collection = db["user"]

        data = {"name": name, "email": email, "discord_id": discord_id, "event": event}
        
        print("Data: ", data)
        collection.insert_one(data)

        print('Inserted!')

    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection to MongoDB Atlas failed: {e}")

    finally:
        client.close()

def get_user_id_by_name(user_discord_id, db):
    # Function to fetch user_id from the "user" collection based on user_name
    user_collection = db["user"]
    user = user_collection.find_one({"discord_id": user_discord_id})
    if user:
        return user["_id"]
    else:
        return None

def get_event_id_by_hashtag(event_hashtag, db):
    # Function to fetch event_id from the "events" collection based on event_hashtag
    events_collection = db["events"]
    event = events_collection.find_one({"event_hashtag": event_hashtag})
    if event:
        return event["_id"]
    else:
        return None

def insert_details(user_discord_id, event_hashtag, link):
    try:
        # Create a MongoClient with the connection string
        client = pymongo.MongoClient(connection_string)

        # Access your database
        db = client["ChallengersDB"]
        
        user_id = get_user_id_by_name(user_discord_id, db)
        event_id = get_event_id_by_hashtag(event_hashtag, db)

        print(f"User_Id: {user_id}, Event_Id: {event_id}")

        if user_id is not None and event_id is not None:
            # Insert data into the "user_participation" collection
            collection = db["user_participation"]

            # Define the data to be inserted
            data = {
                "user_id": user_id,
                "event_id": event_id,
                "link": link.split('?')[0]  # Adjust the link format as needed
            }

            # Insert the data
            collection.insert_one(data)
            print('Inserted!')
            
            client.close()
            return True
        else:
            print("User or event not found.")
            client.close()
            return False

    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection to MongoDB Atlas failed: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.close()

def fetch_user_participation_and_create_pdf(event_hashtag):
    try:
        # Create a MongoClient with the connection string
        client = pymongo.MongoClient(connection_string)

        # Access your database
        db = client["ChallengersDB"]

        # Access the collections
        user_participation_collection = db["user_participation"]

        # First, find the corresponding event_id for the event_hashtag
        events_collection = db["events"]
        event = events_collection.find_one({"event_hashtag": event_hashtag})
        if not event:
            print(f"Event with hashtag '{event_hashtag}' not found.")
            return

        # Use the aggregation framework to join data from multiple collections
        pipeline = [
            {
                "$match": {"event_id": event['_id']}  
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_details"
                }
            },
            {
                "$unwind": "$user_details"
            },
            {
                "$lookup": {
                    "from": "events",
                    "localField": "event_id",
                    "foreignField": "_id",
                    "as": "event_details"
                }
            },
            {
                "$unwind": "$event_details"
            },
            {
                "$project": {
                    "User Name": "$user_details.name",
                    "Email": "$user_details.email",
                    "Discord ID": "$user_details.discord_id",
                    "Event Name": "$event_details.event_name",
                    "Link": "$link"
                }
            }
        ]

        participations = list(user_participation_collection.aggregate(pipeline))

        # Create a PDF file
        pdf_file = "user_participation_details.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        elements = []

        # Create styles for the table
        styles = getSampleStyleSheet()
        style_heading = styles["Heading1"]
        style_body = styles["Normal"]

        # Define participation table
        participation_data = [["User Name", "Email", "Discord ID", "Event Name", "Link"]]
        for participation in participations:
            participation_data.append([
                participation["User Name"],
                participation["Email"],
                participation["Discord ID"],
                participation["Event Name"],
                participation["Link"]
            ])
        participation_table = Table(participation_data, colWidths=[80, 120, 80, 80, 200], rowHeights=30)
        participation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(Paragraph("User Participation Details", style_heading))
        elements.append(participation_table)

        # Build the PDF document
        doc.build(elements)
        print(f"PDF file '{pdf_file}' created successfully!")

    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection to MongoDB Atlas failed: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.close()

    return pdf_file


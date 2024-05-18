from flask import Flask, request, jsonify
from google.cloud import storage
import json 
import base64
import functions_framework
from pub_sub.pub_sub import create_topic, publish_message, create_subscription

app = Flask(__name__)

project_id = "" # id of project
bucket_name = "" # name of bucket

client = storage.Client()
bucket = client.bucket(bucket_name) # name of bucket

listing_topic_id = "create/update_listing"
listing_subscription_id = "listing-service-subscription"

create_topic(project_id, listing_topic_id)
create_subscription(project_id, listing_topic_id, listing_subscription_id)

def publish_listing_event(project_id, listing_topic_id, listing_data): #####, Add information from bounded context, like listing_id, etc): #####
    '''
    This function is responsible for publishing listing information from the listing bounded context to the event bus. It should be 
    integrated into the listing bounded context service to publish listing events whenever a listing is initiated. 
    (Pub_Listing in Component Diagram)
    '''
    listing_event = {
        "type": "Listing",
        "data": listing_data ##### Add the variable which are initalized in the function here (see listing_doa.py) #####
    }
    publish_message(project_id, listing_topic_id, listing_event) # Pub_Listing
    print(f"Published listing event for listing ID {listing_data}")

@functions_framework.cloud_event
def handle_listing_event(cloud_event):
    '''
    This function is designed to subscribe to the create/update_listing topic and process listing information from the event bus. 
    It will be triggered whenever a new message is published to the create/update_listing topic.
    (Sub_Listing in Component Diagram)
    '''
    data = cloud_event.data
    message_data = json.loads(base64.b64decode(data["message"]["data"]).decode('utf-8')) #Sub_Listing
    print(f'Message data: {message_data}')

    if message_data['type'] == "Listing":
        ##### Get the same information that is stored in the event bus
        return "", 200

    return jsonify({'error': 'We apologize, but we are unable to get the listing information at this time.'})

@app.route('/pictures', methods=['POST', 'GET'])
def pictures():
    '''
    This function is designed to POST and GET images from a specified google cloud bucket
    '''
    if request.method == 'POST':
        picture = request.files.get('file')
        if picture:
            blob = bucket.blob(picture.filename)
            blob.upload_from_string(picture.read(), content_type=picture.content_type)
            return jsonify({"message": f"Uploaded {picture.filename} to {bucket.name}"}), 200
        return jsonify({"error": "No file uploaded"}), 400

    if request.method == 'GET':
        filename = request.args.get('filename')
        if filename:
            blob = bucket.blob(filename)
            url = blob.generate_signed_url(3600, version="v4") 
            return jsonify({"url": url}), 200
        return jsonify({"error": "No filename provided"}), 400

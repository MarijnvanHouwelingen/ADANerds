from flask import Flask, request, jsonify
from google.cloud import storage
import json 
import base64
import functions_framework
from pub_sub import create_topic, publish_message, create_subscription

app = Flask(__name__)

project_id = "emerald-diagram-413020"
bucket_name =  'picture_ass2' 

client = storage.Client()
bucket = client.bucket(bucket_name) 

listing_topic_id = 'update_listing'
listing_subscription_id = 'listing-service-subscription'

create_topic(project_id, listing_topic_id)
create_subscription(project_id, listing_topic_id, listing_subscription_id)

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
        listing_id = message_data['data']['id']
        return jsonify({'message': f'Listing with ID {listing_id} has been created/updated.'}), 200

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

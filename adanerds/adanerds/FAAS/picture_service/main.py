from flask import Flask, request, jsonify # noqa
from google.cloud import storage
import requests  # Import the requests library
import os
import logging
#from pub_sub import create_topic, create_subscription

app = Flask(__name__)

project_id = "emerald-diagram-413020"
bucket_name =  'picture_ass2' 

client = storage.Client()
bucket = client.bucket(bucket_name) 

# listing_topic_id = 'update_listing'
# listing_subscription_id = 'listing-service-subscription'

# Already created topic and subscription
#create_topic(project_id, listing_topic_id)
#create_subscription(project_id, listing_topic_id, listing_subscription_id)

# Authorization URL from environment variables
AUTH_URL = os.getenv('AUTH_URL')

# Set the logging level to INFO
logging.basicConfig(level=logging.INFO)

def verify_auth(request):
    
    auth_header = request.headers.get("Authorization")
    logging.info(f"the header is {auth_header}")
    if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            print(f"the token is: {token}")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{AUTH_URL}/verify', headers=headers)
    logging.info(f"the response status.code is {response.status_code}")
    return response.status_code == 200


@app.route('/v1.0/listings/pictures', methods=['POST', 'GET'])
def pictures(request):
    '''
    This function is designed to POST and GET images from a specified google cloud bucket
    '''
    logging.info(f"the request is {request}")
    verify_auth(request=request)
    if verify_auth(request=request):
        if request.method == 'POST':
            picture = request.files.get('file')
            if picture:
                blob = bucket.blob(picture.filename)
                blob.upload_from_string(picture.read(), content_type=picture.content_type)
                return jsonify({"message": f"Uploaded {picture.filename} to {bucket.name}"}), 200
            return jsonify({"error": "No file uploaded"}), 400

        # if request.method == 'GET':
        #     filename = request.args.get('filename')
        #     if filename:
        #         blob = bucket.blob(filename)
        #         url = blob.generate_signed_url(3600, version="v4") 
        #         return jsonify({"url": url}), 200
        #     return jsonify({"error": "No filename provided"}), 400
    return jsonify({"error": "Authorization header missing or invalid"}), 401

 
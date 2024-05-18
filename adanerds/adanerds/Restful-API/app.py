import logging
import os
import requests

import connexion
from connexion.resolver import RestyResolver
from resources.account import User,Profile,NotificationSettings
from resources.listing  import Listing
from resources.booking import Booking
from flask_cors import CORS
from db import Base, engine
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
Base.metadata.create_all(engine)
app.add_api('account-api.yaml')

# Initialize CORS
CORS(app.app)


def check_if_authorize(req):
    auth_header = req.headers['Authorization']
    if 'AUTH_URL' in os.environ:
        auth_url = os.environ['AUTH_URL']
    else:
        auth_url = 'http://authentication_service_ct:5000/verify'
    result = requests.post(auth_url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': auth_header})
    status_code = result.status_code
    
    logging.info(f"Authentication service returned status code: {status_code}")
    logging.info(f"Authentication service returned output: {result.json()}")

    return status_code


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
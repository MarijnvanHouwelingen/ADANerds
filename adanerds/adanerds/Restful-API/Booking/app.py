import os

import connexion
from flask_cors import CORS

from connexion.exceptions import OAuthProblem
import logging
import requests
from db import Base, engine
from booking import Booking # noqa
from authorization import check_if_authorize
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
Base.metadata.create_all(engine)
app.add_api('booking-api.yaml',auth_all_paths=True)

def check_if_authorize(token):
    """Check if the token is valid by querying the authorization service.
    Args:
        token: The authorization token.
    Returns:
        The response from the authentication service.
    Raises:
        OAuthProblem: If the token is invalid or authorization service is unreachable.
    """
    logging.info(f"Authorization token received: {token}")
    if not token:
        logging.error("No authorization token provided")
        raise OAuthProblem('No authorization token provided')

    auth_header = f"Bearer {token}"
    try:
        base_url = os.environ['AUTH_URL']
        endpoint = "/verify"
        auth_url = base_url + endpoint
    except KeyError:
        logging.error("AUTH_URL environment variable not set")
        raise OAuthProblem('AUTH_URL environment variable not set')

    try:
        logging.info(f"Sending request to auth service: {auth_url}")
        result = requests.post(auth_url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': auth_header})
        logging.info(f"Auth service response status code: {result.status_code}")
        logging.info(f"Auth service response: {result.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to auth service: {str(e)}")
        raise OAuthProblem('Error connecting to auth service')

    if result.status_code == 200:
        return result.json()  # Assuming the response contains user info
    else:
        logging.error("Invalid token")
        raise OAuthProblem('Invalid token')

def bearer_auth(token):
    """Extract and validate the Bearer token from the request."""
    if not token:
        logging.error("Authorization token is missing from the request")
        raise OAuthProblem('No authorization token provided')
    return check_if_authorize(token)

# Configure Connexion to use the authorization function
app.app.config['connexion_auth'] = {'BearerAuth': bearer_auth}

# Initialize CORS
CORS(app.app)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
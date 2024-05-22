
import os
import requests

import connexion
import logging
from flask_cors import CORS
from jose import JWTError, jwt
from connexion.exceptions import OAuthProblem


from db import Base, engine
from account import User,Profile,NotificationSettings # noqa

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
    
def bearer_info_func(token):
    print(f"Bearer token received: {token}")
    return check_if_authorize(token)

options = {
    "swagger_ui": True,
    "swagger_url": "/swagger",
    "pythonic_params": True,
    "securityHandlers": {
        "BearerAuth": bearer_info_func
    }
}

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
Base.metadata.create_all(engine)
app.add_api('account-api.yaml',auth_all_paths=True, options=options)


# Initialize CORS
CORS(app.app)

# get SECRET_KEY
if 'SECRET_KEY' in os.environ:
    key_file = os.environ['SECRET_KEY']
else:
    key_file = 'key.txt'
with open(key_file, 'r') as file:
    data = file.read().replace('\n', '')

# JWT secret
JWT_SECRET = data
JWT_ALGORITHM = "HS256"

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise OAuthProblem from e


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
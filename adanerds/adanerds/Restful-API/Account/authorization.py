import os
import requests
from flask import jsonify # noqa
from connexion.exceptions import OAuthProblem

def check_if_authorize(token):
    auth_header = f"Bearer {token}"
    try:
        auth_url = os.environ['AUTH_URL']
    except KeyError:
        raise OAuthProblem('AUTH_URL environment variable not set')

    result = requests.post(auth_url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': auth_header})

    if result.status_code == 200:
        return result.json()  # Assuming the response contains user info
    else:
        raise OAuthProblem('Invalid token')

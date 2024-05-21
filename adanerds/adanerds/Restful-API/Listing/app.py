import logging
import os

import connexion
from flask_cors import CORS

from db import Base, engine
from listing import Listing # noqa
from authorization import check_if_authorize
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
Base.metadata.create_all(engine)
app.add_api('listing-api.yaml',auth_all_paths=True)

# Add the authentication function to Connexion
app.app.config['connexion_auth'] = {'BearerAuth': check_if_authorize}

# Initialize CORS
CORS(app.app)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
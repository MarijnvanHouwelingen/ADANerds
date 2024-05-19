import logging
import os

import connexion
from connexion.resolver import RestyResolver
from listing  import Listing

from flask_cors import CORS

from db import Base, engine
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
Base.metadata.create_all(engine)
app.add_api('listing-api.yaml')

# Initialize CORS
CORS(app.app)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
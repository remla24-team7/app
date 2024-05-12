from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from backend.resources.predictor import Predictor
from dotenv import load_dotenv

def create_app():
    application = Flask(__name__)
    CORS(application)
    api = Api(application)

    # Add the api endpoints
    api.add_resource(Predictor, '/send-to-predict')

    return application


if __name__ == '__main__':
    load_dotenv()
    app = create_app()
    # Run on 8000 since 5000 is used by other service
    app.run(port=8000, debug=True)

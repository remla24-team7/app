from flask_restful import Resource
import requests
from flask import request
import os
from dotenv import load_dotenv


class Predictor(Resource):
    def post(self):
        load_dotenv()
        input_data = request.get_json(force=True)
        input_text = input_data.get('input', '')
        url_to_model_api = os.getenv('PREDICTION_URL')
        json_input = {'input': input_text}
        response = requests.post(url_to_model_api, json=json_input)

        if response.status_code == 200:
            return {'prediction': response.text}
        else:
            return {'error': 'Something went wrong with the model-service'}, response.status_code

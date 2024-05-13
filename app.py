import os
import requests
from flask import Flask, request, jsonify, send_from_directory

# from versioning.versioning import VersionUtil

model_service = os.environ["MODEL_SERVICE_URL"]


app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    model_response = requests.post(f"{model_service}/predict", json=request.json)
    prediction = model_response.json()
    return jsonify(prediction)


@app.route("/version")
def version():
    return jsonify("0.0.0?")
    # return VersionUtil().version


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)

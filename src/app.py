import os
import requests
from flask import Flask, request, jsonify, send_from_directory, Response
from versioning.versioning import VersionUtil
from prometheus_flask_exporter import PrometheusMetrics

model_service = os.environ["MODEL_SERVICE_URL"]
version_util = VersionUtil()

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_frontend_info', 'Application frontend info', version='1.0.0')


@app.route("/")
def index():
    return send_from_directory("./frontend", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    model_response = requests.post(f"{model_service}/predict", json=request.json)
    prediction = model_response.json()
    return jsonify(prediction)


@app.route("/version", methods=["GET"])
def version():
    return jsonify(version_util.version)


@app.route("/agree", methods=["POST"])
def agree():
    _ = requests.post(f"{model_service}/agree")
    return Response(status=204)


@app.route("/disagree", methods=["POST"])
def disagree():
    _ = requests.post(f"{model_service}/disagree")
    return Response(status=204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))

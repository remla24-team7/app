import os
import requests
from flask import Flask, request, jsonify, send_from_directory, Response
from versioning.versioning import VersionUtil
from prometheus_flask_exporter import PrometheusMetrics
import prometheus_client
import time

model_service = os.environ["MODEL_SERVICE_URL"]
version_util = VersionUtil()

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('appv2_frontend_info', 'Application frontend info', version='1.0.0')
app2_views_counter = prometheus_client.Counter('app2_views_counter', 'Number of times website has been loaded')
app2_requests_counter = prometheus_client.Counter('app2_requests_counter', 'Number of requests')
app2_agree_counter = prometheus_client.Counter('app2_agree_counter', 'Number of times users agree with the result')
app2_disagree_counter = prometheus_client.Counter('app2_disagree_counter', 'Number of times users disagree with the result')
app2_legitimate_counter = prometheus_client.Counter('app2_legitimate_counter', 'Number of legitimate URLs')
app2_phishing_counter = prometheus_client.Counter('app2_phishing_counter', 'Number of phishing URLs')
app2_predict_time_histogram = prometheus_client.Histogram('app2_predict_time_histogram', 'Time taken for prediction')


@app.route("/")
def index():
    return send_from_directory("./frontend", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    app2_requests_counter.inc()

    tic = time.perf_counter()
    model_response = requests.post(f"{model_service}/predict", json=request.json)
    toc = time.perf_counter()
    app2_predict_time_histogram.observe(toc - tic)

    prediction = model_response.json()
    return jsonify(prediction)


@app.route("/version", methods=["GET"])
def version():
    app2_views_counter.inc()
    return jsonify(version_util.version)


@app.route("/agree", methods=["POST"])
def agree():
    app2_agree_counter.inc()
    _ = requests.post(f"{model_service}/agree")
    return Response(status=204)


@app.route("/disagree", methods=["POST"])
def disagree():
    app2_disagree_counter.inc()
    _ = requests.post(f"{model_service}/disagree")
    return Response(status=204)

@app.route("/metrics", methods=["GET"])
def get_metrics():
    return Response(prometheus_client.generate_latest(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))

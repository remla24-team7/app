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
metrics.info('appv1_frontend_info', 'Application frontend info', version='1.0.0')
views_counter = prometheus_client.Counter('views_counter', 'Number of times website has been loaded',
                                          ['version1'])
requests_counter = prometheus_client.Counter('requests_counter', 'Number of requests', ['version1'])
agree_counter = prometheus_client.Counter('agree_counter', 'Number of times users agree with the result',
                                          ['version1'])
disagree_counter = prometheus_client.Counter('disagree_counter', 'Number of times users disagree with the result',
                                             ['version1'])
legitimate_counter = prometheus_client.Counter('legitimate_counter', 'Number of legitimate URLs',
                                               ['version1'])
phishing_counter = prometheus_client.Counter('phishing_counter', 'Number of phishing URLs',
                                             ['version1'])
predict_time_histogram = prometheus_client.Histogram('predict_time_histogram', 'Time taken for prediction',
                                                     ['version1'])


@app.route("/")
def index():
    return send_from_directory("./frontend", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    requests_counter.inc()

    tic = time.perf_counter()
    model_response = requests.post(f"{model_service}/predict", json=request.json)
    toc = time.perf_counter()
    predict_time_histogram.observe(toc - tic)

    prediction = model_response.json()
    return jsonify(prediction)


@app.route("/version", methods=["GET"])
def version():
    views_counter.inc()
    return jsonify(version_util.version)


@app.route("/agree", methods=["POST"])
def agree():
    agree_counter.inc()
    _ = requests.post(f"{model_service}/agree")
    return Response(status=204)


@app.route("/disagree", methods=["POST"])
def disagree():
    disagree_counter.inc()
    _ = requests.post(f"{model_service}/disagree")
    return Response(status=204)

@app.route("/metrics", methods=["GET"])
def get_metrics():
    return Response(prometheus_client.generate_latest(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))

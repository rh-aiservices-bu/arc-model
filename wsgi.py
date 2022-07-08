import json
from flask import Flask, jsonify, request
from prediction import find_objects_and_predict_discounts

application = Flask(__name__)


@application.route("/")
@application.route("/status")
def status():
    return jsonify({"status": "ok"})


@application.route("/predictions", methods=["POST"])
def create_prediction():
    data = request.data or "{}"
    body = json.loads(data)
    return jsonify(find_objects_and_predict_discounts(body))

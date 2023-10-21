import requests
from flask import Flask, request
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import base64
import json

from utils.firebase_utils import convert_string_to_dict

app = Flask(__name__)


@app.route('/budget-alert', methods=['POST'])
def budget_alert_endpoint():
    request_json = request.json
    headers = request.headers
    print(f"Data: {request_json}")
    print(f"Headers: {headers}")
    encoded_data = request_json["message"]["data"]
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    decoded_dict = convert_string_to_dict(decoded_data)
    print(f"Decoded data: {decoded_dict}")
    percentage_achieved = f"{decoded_dict['alertThresholdExceeded']*100}%"
    moneySpent = decoded_dict["costAmount"]
    return f"Percentage achieved: {percentage_achieved}, money spent: {moneySpent}", 200


def __main():
    app.run(port=5000)


if __name__ == '__main__':
    __main()

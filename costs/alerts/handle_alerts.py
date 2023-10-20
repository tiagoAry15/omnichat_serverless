import requests
from flask import Flask, request
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import base64
import json


app = Flask(__name__)


@app.route('/budget-alert', methods=['POST'])
def budget_alert_endpoint():
    request_json = request.json
    headers = request.headers
    print(f"Data: {request_json}")
    print(f"Headers: {headers}")
    encoded_data = request_json["message"]["data"]
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    print(f"Decoded data: {decoded_data}")
    return f"Data received!", 200


def __main():
    app.run(port=5000)


if __name__ == '__main__':
    __main()

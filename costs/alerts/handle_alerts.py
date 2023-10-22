import os

import requests
from flask import Flask, request
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import base64
import json

from costs.alerts.gmail_sender import send_gmail
from utils.firebase_utils import convert_string_to_dict
from utils.time_utils import convert_timestamp

app = Flask(__name__)


def decode_dict_from_google_cloud_request(request_json: dict):
    encoded_data = request_json["message"]["data"]
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    return convert_string_to_dict(decoded_data)


def extract_meaningful_info_from_decoded_dict(decoded_dict: dict):
    moneySpent = decoded_dict["costAmount"]
    costIntervalTime = convert_timestamp(decoded_dict["costIntervalStart"])
    percentage_achieved = f"{decoded_dict['alertThresholdExceeded'] * 100}%"
    return moneySpent, costIntervalTime, percentage_achieved


def send_cloud_warning_email(costIntervalTime, moneySpent, percentage_achieved):
    final_string = (f"• Money spent: R${moneySpent}\n"
                    f"• Percentage achieved: {percentage_achieved}\n"
                    f"• Timestamp: {costIntervalTime}."
                    f"\n"
                    f"Because of this, we decided to automatically shutdown firebase realtime database."
                    f"Please, check your cloud console for more details.")
    gmail_user = os.environ['SEND_GMAIL_USERNAME']
    gmail_password = os.environ['SEND_GMAIL_APP_PASSWORD']
    send_gmail(
        subject=f'Your cloud budget is running out! You have spent R${moneySpent} so far.',
        body=final_string,
        to_email='matbessa12@gmail.com',  # Replace with the recipient's email address
        gmail_user=gmail_user,
        gmail_password=gmail_password
    )
    return final_string


@app.route('/budget-alert', methods=['POST'])
def budget_alert_endpoint():
    request_json = request.json
    decoded_dict = decode_dict_from_google_cloud_request(request.json)
    moneySpent, costIntervalTime, percentage_achieved = extract_meaningful_info_from_decoded_dict(decoded_dict)
    final_string = send_cloud_warning_email(costIntervalTime, moneySpent, percentage_achieved)
    return final_string, 200


def __main():
    app.run(port=5000)


if __name__ == '__main__':
    __main()

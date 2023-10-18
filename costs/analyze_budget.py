import datetime
import os

import requests
from dotenv import load_dotenv
from google.cloud import billing_v1
from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from authentication.private_key_issue_solver import fix_private_key
from authentication.sdk_dict import getSdkDict


def get_cloud_credentials():
    load_dotenv()
    sdk_dict = getSdkDict()
    key = fix_private_key(sdk_dict["private_key"])
    sdk_dict["private_key"] = key
    return Credentials.from_service_account_info(
        sdk_dict,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )


def create_service():
    credentials = get_cloud_credentials()
    # Create a service client for the Cloud Billing API
    service = discovery.build('billingbudgets', 'v1beta1', credentials=credentials)
    return service


def get_billing_info(billing_id: str):
    credentials = get_cloud_credentials()
    client = billing_v1.CloudBillingClient(credentials=credentials)
    name = f'billingAccounts/{billing_id}'

    billing_account = client.get_billing_account(name=name)
    print(f"Billing Account Name: {billing_account.name}")
    print(f"Billing Account Display Name: {billing_account.display_name}")
    print(f"Open: {billing_account.open}")


def __main():
    load_dotenv()
    BILLING_ACCOUNT_ID = os.environ["GOOGLE_BILLING_ACCOUNT_ID"]

    service = create_service()
    get_billing_info(BILLING_ACCOUNT_ID)


if __name__ == '__main__':
    __main()

import json
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import billing_v1
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.cloud import bigquery


def get_oauth_credentials() -> dict:
    load_dotenv()
    json_raw_content = os.environ["OAUTH_JSON"]
    return json.loads(json_raw_content)


def get_authenticated_service():
    creds_data = get_oauth_credentials()
    creds = None

    # Check if we have a token stored
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token_file:
            creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(creds_data,
                                                       [
                                                           'https://www.googleapis.com/auth/cloud-platform'])  # Updated scope
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token_file:
                token_file.write(creds.to_json())

    cloud_billing_service = build('cloudbilling', 'v1', credentials=creds)
    big_query_service = build('bigquery', 'v2', credentials=creds)
    return cloud_billing_service, big_query_service, creds


def get_billing_accounts(service) -> List[dict]:
    results = service.billingAccounts().list().execute()
    return results.get('billingAccounts', [])


def list_projects_for_billing_account(service, billing_account_name) -> List[dict]:
    """List all projects linked to a billing account."""
    projects = []
    request = service.billingAccounts().projects().list(name=billing_account_name)
    while request is not None:
        response = request.execute()
        projects.extend(response.get('projectBillingInfo', []))
        request = service.billingAccounts().projects().list_next(previous_request=request, previous_response=response)
    return projects


def __main():
    cloud_billing_service, big_query_service, creds = get_authenticated_service()
    billing_accounts = get_billing_accounts(cloud_billing_service)
    projects = list_projects_for_billing_account(cloud_billing_service, billing_accounts[0]['name'])

    # Create BigQuery client
    client = bigquery.Client(credentials=creds, project='pizzadobill-rpin')

    print_expenses(cloud_billing_service, client, billing_accounts)


if __name__ == '__main__':
    __main()

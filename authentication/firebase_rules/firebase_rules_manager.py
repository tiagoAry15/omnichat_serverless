import google.auth
import requests
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials

from authentication.sdk_auth.private_key_issue_solver import fix_private_key
from authentication.sdk_auth.sdk_dict import getSdkDict
from utils.firebase_utils import convert_firebase_rule_to_dict


def get_service_account_access_token() -> str:
    # Define the required scopes
    scopes = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/firebase.database"
    ]

    sdk_dict = getSdkDict()
    sdk_dict["private_key"] = fix_private_key(sdk_dict["private_key"])

    # Authenticate a credential with the service account
    creds = Credentials.from_service_account_info(sdk_dict, scopes=scopes)

    # Use the credentials object to authenticate a Requests session.
    authed_session = AuthorizedSession(creds)
    response = authed_session.get(
        "https://pizzadobill-rpin-default-rtdb.firebaseio.com//users/ada/name.json")

    # Or, use the token directly, as described in the "Authenticate with an
    # access token" section below. (not recommended)
    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    return creds.token


def fetch_firebase_rules(access_token: str, database_url: str):
    """This function is a wrap-up python for the following command-line
    curl 'https://docs-examples.firebaseio.com/.settings/rules.json?access_token=<ACCESS_TOKEN>'"""
    url = f'{database_url}/.settings/rules.json?access_token={access_token}'
    response = requests.get(url)
    return convert_firebase_rule_to_dict(response.text)


def update_firebase_rules(access_token: str, new_rule: dict, database_url: str):
    """This function is a wrap-up python for the following command-line
    curl -X PUT -d '{ "rules": { ".read": false } }' 'https://docs-examples.firebaseio.com/.settings/rules.json?access_token=<ACCESS_TOKEN>'"""
    url = f'{database_url}.settings/rules.json?access_token={access_token}'
    response = requests.put(url, json=new_rule)
    return response.text


def __main():
    token = get_service_account_access_token()
    rules = fetch_firebase_rules(token)
    print(rules)
    # new_rule = {"rules": {".read": False, ".write": False}}
    # update_firebase_rules(token, new_rule)


if __name__ == '__main__':
    __main()

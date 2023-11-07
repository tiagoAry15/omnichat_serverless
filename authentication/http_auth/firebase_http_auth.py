import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIREBASE_API_KEY = os.environ["FIREBASE_API_KEY"]
FIREBASE_DATABASE_URL = os.environ["FIREBASE_DATABASE_URL"]
FIREBASE_EMAIL = os.environ["FIREBASE_USERNAME"]
FIREBASE_PASSWORD = os.environ["FIREBASE_PASSWORD"]


def get_id_token() -> str:
    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    auth_payload = {
        "email": FIREBASE_EMAIL,
        "password": FIREBASE_PASSWORD,
        "returnSecureToken": True
    }
    response = requests.post(auth_url, json=auth_payload)
    response_data = response.json()

    if "idToken" not in response_data:
        raise Exception("Failed to authenticate with Firebase.")
    return response_data["idToken"]


def get_data_from_firebase(id_token: str):
    response = requests.get(f"{FIREBASE_DATABASE_URL}/orders.json?auth={id_token}")
    return response.json()


def main():
    id_token = get_id_token()
    data = get_data_from_firebase(id_token)
    print(data)


if __name__ == '__main__':
    main()

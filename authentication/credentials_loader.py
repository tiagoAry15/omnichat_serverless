from dotenv import load_dotenv
from firebase_admin import credentials

from authentication.sdk_dict import getSdkDict


def getFirebaseCredentials():
    load_dotenv()
    firebase_credentials = getSdkDict()
    key = firebase_credentials["private_key"]
    key = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
    key = f"-----BEGIN PRIVATE KEY-----\n{key}\n-----END PRIVATE KEY-----"
    firebase_credentials["private_key"] = key
    return credentials.Certificate(firebase_credentials)
from authentication.http_auth.firebase_http_connection import FirebaseHTTPConnection
from authentication.sdk_auth.firebase_sdk_connection import FirebaseSDKConnection


class FirebaseConnectionFactory:
    @staticmethod
    def create_connection(connection_type: str):
        if connection_type == "SDK":
            return FirebaseSDKConnection()
        elif connection_type == "HTTP":
            return FirebaseHTTPConnection()
        else:
            raise ValueError("Unknown connection type")
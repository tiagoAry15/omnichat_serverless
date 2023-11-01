import os
import requests
from dotenv import load_dotenv
from authentication.abstraction.abstract_connection import AbstractFirebaseConnection
from authentication.http_auth.firebase_http_auth import get_id_token


class FirebaseHTTPConnection(AbstractFirebaseConnection):
    def __init__(self):
        load_dotenv()
        self.id_token = get_id_token()
        self.database_url = os.environ["FIREBASE_DATABASE_URL"]
        self.connection = ''

    def get_url(self, path: str) -> str:
        return f"{self.database_url}/{path}.json?auth={self.id_token}"

    def changeDatabaseConnection(self, path: str) -> None:
        self.connection = path

    def readData(self, path: str = None) -> dict:
        path = path or self.connection
        url = self.get_url(path)
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        return response.json()

    def getValue(self, path: str) -> dict:
        return self.readData(path)

    def setValue(self, path: str, value: dict) -> bool:
        url = self.get_url(path)
        response = requests.put(url, json=value)
        response.raise_for_status()
        return True

    def writeData(self, path: str = None, data: dict = None) -> bool:
        path = path or self.connection
        if data is None:
            data = {"dummyData": 5}
        url = self.get_url(path)
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['name']

    def writeDataWithoutUniqueId(self, path: str = None, data: dict = None) -> bool:
        path = path or self.connection
        if data is None:
            data = {"dummyData": 5}
        return self.setValue(path, data)

    def overWriteData(self, path: str = None, data: dict = None) -> bool:
        path = path or self.connection
        if data is None:
            data = {"dummyData": 5}
        return self.setValue(path, data)

    def deleteData(self, path: str, data: dict = None) -> bool:
        # If only path is provided, we assume it's the direct reference to the data to delete
        if data is None:
            url = self.get_url(path)
            response = requests.delete(url)
            response.raise_for_status()
            return True

        # If data is also provided, we need to find its unique ID first
        data_id = self.getUniqueIdByData(path, data)
        if data_id is None:
            raise ValueError("Cannot find unique ID for provided data")

        # Construct the URL with the unique ID and delete the data
        path_with_id = f"{path}/{data_id}"
        url = self.get_url(path_with_id)
        response = requests.delete(url)
        response.raise_for_status()
        return True

    def deleteAllData(self) -> bool:
        url = self.get_url('')
        response = requests.delete(url)
        response.raise_for_status()
        return True

    def getUniqueIdByData(self, path: str = None, data: dict = None) -> str:
        path = path or self.connection
        if data is None:
            raise ValueError("Data cannot be None")
        url = self.get_url(path)
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['name']  # Firebase returns the unique key as 'name'

    def getDatabaseRules(self) -> dict:
        """Retrieve Firebase Realtime Database Security Rules."""
        url = f"{self.database_url}/.settings/rules.json?auth={self.id_token}"
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        return response.json()

    def setDatabaseRules(self, rules: dict) -> bool:
        """Update Firebase Realtime Database Security Rules."""
        url = f"{self.database_url}/.settings/rules.json?auth={self.id_token}"
        response = requests.put(url, json=rules)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        return True


def main():
    fc = FirebaseHTTPConnection()
    data = fc.readData("users")
    print(data)
    rules = fc.getDatabaseRules()
    print(rules)
    return


if __name__ == '__main__':
    main()

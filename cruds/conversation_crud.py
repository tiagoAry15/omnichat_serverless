from typing import List

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.createDummyConversations import createDummyConversations
from utils.randomGenerators import generateRandomDummyConversation


class ConversationCrud:
    def __init__(self):
        self.fc = FirebaseConnection()
        self.fcm = FirebaseConversation(self.fc)

    def getAllConversations(self) -> dict:
        return self.fcm.getAllConversations()

    @staticmethod
    def insertDummyConversations(parameters: tuple):
        createDummyConversations(parameters)

    def createConversation(self, conversationPayload: dict):
        requiredKeys = {"from": str, "id": str, "lastMessage_timestamp": int, "messagePot": List, "name": str,
                        "phoneNumber": str, "status": str, "unreadMessages": int}
        for key, value in requiredKeys.items():
            if key not in conversationPayload.keys():
                raise KeyError(f"Key {key} not found in conversationPayload")
            if type(conversationPayload[key]) != value:
                raise TypeError(f"Key {key} should be of type {value} instead of {type(conversationPayload[key])}")
        if conversationPayload is None:
            conversationPayload = generateRandomDummyConversation()
        return self.fcm.createConversation(conversationPayload)


def __main():
    cc = ConversationCrud()
    aux = generateRandomDummyConversation()
    return


if __name__ == '__main__':
    __main()

import random
from typing import List

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.createDummyConversations import createDummyConversations
from utils.randomGenerators import createRandomIdString, generateRandomFloatInRange, generateRandomPhoneNumber, \
    generateRandomMessagePot


def _generateRandomDummyConversation():
    _from = random.choice(["whatsapp", "messenger", "facebook"])
    _id = createRandomIdString()
    timestamp = generateRandomFloatInRange(1691438953)
    name = random.choice(["John", "Maria", "Anthony", "Peter", "Paul", "Mary", "Joseph", "Max", "Jack", "Jill"])
    phoneNumber = generateRandomPhoneNumber()
    status = "active"
    unreadMessages = 0
    randomSize = random.randint(3, 9)
    messagePot = generateRandomMessagePot(size=randomSize, senderName=name, phoneNumber=phoneNumber, _from=_from)
    return {"from": _from, "id": _id, "lastMessage_timestamp": timestamp, "messagePot": messagePot, "name": name,
            "phoneNumber": phoneNumber, "status": status, "unreadMessages": unreadMessages}


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
            conversationPayload = _generateRandomDummyConversation()
        return self.fcm.createConversation(conversationPayload)


def __main():
    cc = ConversationCrud()
    aux = _generateRandomDummyConversation()
    return


if __name__ == '__main__':
    __main()

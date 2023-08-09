import datetime
import random
import uuid
from enum import Enum
from typing import List

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper

from utils.patterns import singleton


@singleton
class FirebaseConversation(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("conversations")

    def getAllConversations(self):
        return self.firebaseConnection.readData()

    def getUniqueIdByWhatsappNumber(self, whatsappNumber: str) -> str or None:
        # sourcery skip: use-next
        allConversations = self.getAllConversations()
        if allConversations is None:
            return None
        for uniqueId, conversationData in allConversations.items():
            phoneNumber = conversationData.get("phoneNumber", None)
            if phoneNumber == whatsappNumber:
                return uniqueId
        return None

    def appendMessageToWhatsappNumber(self, whatsappNumber: str, body: str, sender: str):
        if not body:
            return 400, "Body is empty."
        if not whatsappNumber:
            return 400, "Whatsapp number is empty."
        if not sender:
            return 400, "Sender is empty."
        messageData = {"body": body, "time": datetime.datetime.now().strftime("%H:%M"), "id": str(uuid.uuid4())}
        conversationUniqueId = self.getUniqueIdByWhatsappNumber(whatsappNumber)
        if not conversationUniqueId:
            return 400, f"Conversation not found for whatsappNumber: {whatsappNumber}"
        conversationData = self.firebaseConnection.readData(path=conversationUniqueId)
        messageData["phoneNumber"] = conversationData["phoneNumber"]
        senderName = "bot" if sender == "bot" else conversationData["name"]
        messageData["sender"] = senderName
        if "messagePot" not in conversationData:
            conversationData["messagePot"] = []
        conversationData["messagePot"].append(messageData)
        self.firebaseConnection.overWriteData(path=conversationUniqueId, data=conversationData)
        return 200, "Conversation updated successfully."

    def retrieveAllMessagesByWhatsappNumber(self, whatsappNumber: str) -> List[dict] or None:
        uniqueId = self.getUniqueIdByWhatsappNumber(whatsappNumber)
        if not uniqueId:
            return None
        conversationData = self.firebaseConnection.readData(path=uniqueId)
        if "messagePot" not in conversationData:
            return None
        return conversationData["messagePot"]

    def createFirstDummyConversationByWhatsappNumber(self, msgDict: dict):
        whatsappNumber = msgDict.get("phoneNumber", None)
        body = msgDict.get("body", None)
        name = msgDict.get("name", None)
        platform = msgDict.get("from", None)
        currentTime = datetime.datetime.now().strftime("%H:%M")
        conversationData = {"from": platform, "whatsappNumber": whatsappNumber, "id": 0, "name": name,
                            "status": "active", "unreadMessages": 1,
                            "msgPot": [{"body": body, "id": str(uuid.uuid4()), "phoneNumber": "+5585999171902",
                                        "sender": "User", "time": currentTime}]}
        self.firebaseConnection.writeData(data=conversationData)
        return "Dummy conversation created successfully."

    def existingConversation(self, inputConversationData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(inputConversationData["phoneNumber"])
        return uniqueId is not None

    def createConversation(self, conversationData: dict) -> bool:
        existingConversation = self.existingConversation(conversationData)
        return (
            False if existingConversation
            else self.firebaseConnection.writeData(data=conversationData)
        )

    def updateConversation(self, conversationData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(conversationData["phoneNumber"])
        return (
            self.firebaseConnection.overWriteData(path=uniqueId, data=conversationData)
            if uniqueId is not None
            else False
        )

    def updateConversationAddingUnreadMessages(self, messageData: dict) -> bool or None:
        uniqueId = self.getUniqueIdByWhatsappNumber(messageData["phoneNumber"])
        if not uniqueId:
            return None
        conversationData = self.firebaseConnection.readData(path=uniqueId)
        if 'unreadMessages' not in messageData:
            conversationData["unreadMessages"] = conversationData["unreadMessages"] + 1
        else:
            conversationData["unreadMessages"] = 0
        self.firebaseConnection.overWriteData(path=uniqueId, data=conversationData)
        return conversationData

    def deleteConversation(self, conversationData: dict) -> bool:
        uniqueId = self.getUniqueIdByWhatsappNumber(conversationData["phoneNumber"])
        return (
            self.firebaseConnection.deleteData(path=uniqueId)
            if uniqueId is not None
            else False
        )

    def deleteAllConversations(self):
        return self.firebaseConnection.deleteAllData()


def checkNewUser(whatsappNumber: str, numberPot: List[str],
                 conversationInstance: FirebaseConversation, msgDict: dict) -> bool:
    if whatsappNumber in numberPot:
        return False
    numberPot.append(whatsappNumber)
    conversationInstance.createFirstDummyConversationByWhatsappNumber(msgDict)
    return True


def __main():
    # __createDummyConversations()
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    randomUniqueId = str(uuid.uuid4())
    currentTime = datetime.datetime.now().strftime("%H:%M")
    msgDict = {"body": "Olá, tudo bem?", "id": str(uuid.uuid4()), "phoneNumber": "+5585999171902",
               "sender": "Mateus", "time": datetime.datetime.now().strftime("%H:%M")}
    fcm.appendMessageToWhatsappNumber(msgDict, "+558599663533")


if __name__ == "__main__":
    __main()

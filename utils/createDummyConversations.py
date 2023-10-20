import datetime
import random
from typing import Tuple

from firebaseFolder.firebase_sdk_connection import FirebaseSDKConnection
from firebaseFolder.firebase_conversation import FirebaseConversation


def getDummyConversationDicts(username: str = "John", phoneNumber: str = "+558599171902", _from: str = "whatsapp"):
    dummyBodyMessages = ["Olá, tudo bem?", "Sim estou bem, e você?", "Estou bem também, obrigado por perguntar!"]
    dummyMessagePot = []
    for index, body in enumerate(dummyBodyMessages):
        currentFormattedTimestamp = datetime.datetime.now().strftime("%H:%M")
        sender = "ChatBot" if index % 2 == 1 else username
        message = {"body": body, "id": random.randint(0, 10000000000), "phoneNumber": phoneNumber,
                   "sender": sender, "timestamp": currentFormattedTimestamp}
        dummyMessagePot.append(message)

    dummyPot = [{"from": _from, "id": 3, "name": username, "phoneNumber": phoneNumber, "status": "active",
                 "messagePot": dummyMessagePot, "lastMessage": dummyMessagePot[-1], "unreadMessages": 1}]
    return {"dummyMessagePot": dummyMessagePot, "dummyPot": dummyPot}


# def createDummyConversations(inputFcInstance: FirebaseConnection, inputFcmInstance: FirebaseConversation,
#                              dictParameters: Tuple):
#     inputFcmInstance.setConnectionInstance(inputFcInstance)
#     dictPot = []
#     for username, phoneNumber, _from in zip(dictParameters[::3], dictParameters[1::3], dictParameters[2::3]):
#         dicts = getDummyConversationDicts(username=username, phoneNumber=phoneNumber, _from=_from)
#         dictPot.append(dicts)
#     for _dict in dictPot:
#         for conversation in _dict["dummyPot"]:
#             inputFcmInstance.createConversation(conversation)



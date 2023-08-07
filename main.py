from flask import Flask

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.createDummyConversations import createDummyConversations

app = Flask(__name__)


def get_all_conversations(request=None):
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    conversations = fcm.getAllConversations()
    arrayOfConversations = list(conversations.values()) if conversations is not None else ["None"]
    return createResponseWithAntiCorsHeaders(arrayOfConversations)


def create_dummy_conversations(request=None):
    dictParameters = ("John", "+558599171902", "whatsapp",
                      "Maria", "+558599171903", "instagram",
                      "Anthony", "+558599171904", "messenger")
    createDummyConversations(dictParameters)
    return 200, "Dummy conversations created successfully."


def __main():
    aux = get_all_conversations()
    print(aux)
    return


if __name__ == '__main__':
    __main()

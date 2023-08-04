from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.createDummyConversations import createDummyConversations


def get_all_conversations(request=None):
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    conversations = fcm.getAllConversations()
    return createResponseWithAntiCorsHeaders(conversations)


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

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.createDummyConversations import createDummyConversations
from utils.mocks import MockRequest

fc = FirebaseConnection()
fcm = FirebaseConversation(fc)


def create_dummy_conversations(request=None):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    dictParameters = ("John", "+558599171902", "whatsapp",
                      "Maria", "+558599171903", "instagram",
                      "Anthony", "+558599171904", "messenger")
    createDummyConversations(inputFcInstance=fc, inputFcmInstance=fcm, dictParameters=dictParameters)
    return 200, "Dummy conversations created successfully."


def get_all_conversations(request=None):
    if request.method != 'GET':
        return 'Only GET requests are accepted', 405
    conversations = fcm.getAllConversations()
    arrayOfConversations = list(conversations.values()) if conversations is not None else ["None"]
    return createResponseWithAntiCorsHeaders(arrayOfConversations)


def update_conversation(request=None):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    headers = request.headers
    whatsappNumber = headers.get("whatsappNumber", None)
    body = headers.get("body", None)
    sender = headers.get("sender", None)
    return fcm.appendMessageToWhatsappNumber(whatsappNumber, body, sender)


def __main():
    return


if __name__ == '__main__':
    __main()

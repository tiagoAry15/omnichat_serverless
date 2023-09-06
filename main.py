from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.cloudFunctionsUtils import log_memory_usage
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.mocks import MockRequest

fc = FirebaseConnection()
fcm = FirebaseConversation(fc)


def get_all_conversations(request=None):
    if request.method != 'GET':
        return 'Only GET requests are accepted', 405
    conversations = fcm.getAllConversations()
    arrayOfConversations = list(conversations.values()) if conversations is not None else ["None"]
    log_memory_usage()
    return createResponseWithAntiCorsHeaders(arrayOfConversations)


def update_conversation(request=None):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    headers = request.headers
    whatsappNumber = headers.get("whatsappNumber", None)
    body = headers.get("body", None)
    sender = headers.get("sender", None)
    log_memory_usage()
    return fcm.appendMessageToWhatsappNumber(whatsappNumber, body, sender)


def __main():
    dummy_request = MockRequest(method="GET")
    aux = get_all_conversations(dummy_request)
    return


if __name__ == '__main__':
    __main()

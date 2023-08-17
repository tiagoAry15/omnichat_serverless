from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.createDummyConversations import getDummyConversationDicts
from utils.mocks import MockRequest
import psutil

fc = FirebaseConnection()
fcm = FirebaseConversation(fc)


def _log_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Memory in MB
    print(f"Function used approximately {memory_usage:.2f} MB")


def create_dummy_conversations(request=None):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    dictParameters = ("John", "+558599171902", "whatsapp",
                      "Maria", "+558599171903", "instagram",
                      "Anthony", "+558599171904", "messenger")
    dictPot = []
    for username, phoneNumber, _from in zip(dictParameters[::3], dictParameters[1::3], dictParameters[2::3]):
        dicts = getDummyConversationDicts(username=username, phoneNumber=phoneNumber, _from=_from)
        dictPot.append(dicts)
    for _dict in dictPot:
        for conversation in _dict["dummyPot"]:
            fcm.createConversation(conversation)
    _log_memory_usage()
    return 200, "Dummy conversations created successfully."


def get_all_conversations(request=None):
    if request.method != 'GET':
        return 'Only GET requests are accepted', 405
    conversations = fcm.getAllConversations()
    arrayOfConversations = list(conversations.values()) if conversations is not None else ["None"]
    _log_memory_usage()
    return createResponseWithAntiCorsHeaders(arrayOfConversations)


def update_conversation(request=None):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    headers = request.headers
    whatsappNumber = headers.get("whatsappNumber", None)
    body = headers.get("body", None)
    sender = headers.get("sender", None)
    _log_memory_usage()
    return fcm.appendMessageToWhatsappNumber(whatsappNumber, body, sender)


def __main():
    dummy_request = MockRequest(method="GET")
    aux = get_all_conversations(dummy_request)
    return


if __name__ == '__main__':
    __main()

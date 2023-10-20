from authentication.sdk_auth.firebase_sdk_connection import FirebaseSDKConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.cloudFunctionsUtils import log_memory_usage
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.createDummyConversations import getDummyConversationDicts

fc = FirebaseSDKConnection()
fcm = FirebaseConversation(fc)


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
    log_memory_usage()
    return 200, "Dummy conversations created successfully."


def get_conversation_by_whatsapp_number(request=None):
    request_json = request.get_json()
    whatsappNumber = request_json.get("whatsappNumber", None)
    conversationData = fcm.retrieveAllMessagesByWhatsappNumber(whatsappNumber)
    return createResponseWithAntiCorsHeaders(conversationData)

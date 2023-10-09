from deprecated_cloud_functions.old_functions import get_conversation_by_whatsapp_number
from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder
from utils.cloudFunctionsUtils import log_memory_usage
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.mocks import MockRequest

fc = FirebaseConnection()
fcm = FirebaseConversation(fc)
fo = FirebaseOrder(fc)


def get_all_conversations(request=None):
    if request.method != 'GET':
        return 'Only GET requests are accepted', 405
    conversations = fcm.getAllConversations()
    arrayOfConversations = list(conversations.values()) if conversations is not None else ["None"]
    log_memory_usage()
    return createResponseWithAntiCorsHeaders(arrayOfConversations)


def update_conversation(request=None):
    # Ensure it's a POST request
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    body = request.get_json()
    headers = request.headers

    # Retrieve sender from headers or body
    sender = headers.get("sender") or body.get("name")
    if not sender:
        return "Sender cannot be empty", 400

    # Ensure WhatsappNumber exists in headers
    whatsappNumber = headers.get("whatsappNumber")
    if not whatsappNumber:
        return "WhatsappNumber cannot be empty", 400

    log_memory_usage()

    return fcm.appendMessageToWhatsappNumber(whatsappNumber, body, sender)


def create_order(request=None):
    REQUIRED_HEADERS = ["whatsappNumber", "status", "details"]
    if request is None or request.method != 'POST':
        return 'Only POST requests are accepted', 405

    missing_headers = [header for header in REQUIRED_HEADERS if not request.headers.get(header)]
    if missing_headers:
        return f"{', '.join(missing_headers)} cannot be empty", 400

    log_memory_usage()

    whatsappNumber = request.headers["whatsappNumber"]
    status = request.headers["status"]
    details = request.headers["details"]

    return fo.createOrder(whatsappNumber, status, details)


def read_all_orders(request=None):
    if request is None or request.method != 'GET':
        return 'Only GET requests are accepted', 405
    log_memory_usage()
    return createResponseWithAntiCorsHeaders(fo.readAllOrders())


def __main():
    dummy_request = MockRequest(method="GET")
    # aux = get_all_conversations(dummy_request)
    aux = get_conversation_by_whatsapp_number("+558599663533")
    return


if __name__ == '__main__':
    __main()

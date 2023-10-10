import json

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
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, PUT",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return '', 204, headers

    if request.method != 'PUT':
        return 'Only PUT requests are accepted', 405

    body = request.get_json()
    log_memory_usage()

    response = 'conversation updated successfully' if fcm.updateConversation(
        body) else 'error updating conversation, conversation does not exist'
    headers = {"Access-Control-Allow-Origin": "*"}
    response_code = 200 if response else 500
    return json.dumps({'response': response}), response_code, headers


def create_order(request=None):
    REQUIRED_HEADERS = ["customerName", "pizzaName", "status", "address", "platform", "communication"]
    if request is None or request.method != 'POST':
        return 'Only POST requests are accepted', 405

    missing_headers = [header for header in REQUIRED_HEADERS if not request.headers.get(header)]
    if missing_headers:
        return f"{', '.join(missing_headers)} cannot be empty", 400

    log_memory_usage()

    customerName = request.headers["customerName"]
    pizzaName = request.headers["pizzaName"]
    status = request.headers["status"]
    address = request.headers["address"]
    platform = request.headers["platform"]
    communication = request.headers["communication"]
    observation = request.headers.get("observation", None)

    fo.createOrder(customerName=customerName, pizzaName=pizzaName, status=status, address=address,
                   platform=platform, communication=communication, observation=observation)

    response = 'order created successfully', 200
    return createResponseWithAntiCorsHeaders(response)


def read_all_orders(request=None):
    if request is None or request.method != 'GET':
        return 'Only GET requests are accepted', 405
    log_memory_usage()
    return createResponseWithAntiCorsHeaders(fo.readAllOrders())


def __main():
    json = {
        "from": "whatsapp",
        "isBotActive": True,
        "lastMessage_timestamp": "18/08/2023 02:34",
        "messagePot": [
            {
                "body": "oi",
                "id": "b3d9ff41-5219-4dba-9e7a-aa989b695d3f",
                "sender": "Tiago Ary",
                "time": "02:34"
            }
        ],
        "name": "Tiago Ary",
        "phoneNumber": "+558599663533",
        "status": "active",
        "unreadMessages": 4
    }
    dummy_request = MockRequest(method="GET")
    print(fcm.updateConversation(json))
    return


if __name__ == '__main__':
    __main()

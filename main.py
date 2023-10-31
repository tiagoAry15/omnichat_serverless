import datetime
import json
from json import JSONDecodeError

from authentication.auth_factory import FirebaseConnectionFactory
from authentication.firebase_rules.firebase_toggler import FirebaseToggler
from costs.alerts.handle_alerts import decode_dict_from_google_cloud_request, \
    extract_meaningful_info_from_decoded_dict, send_cloud_warning_email
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder
from utils.cloudFunctionsUtils import log_memory_usage
from utils.corsBlocker import createResponseWithAntiCorsHeaders
from utils.mocks import get_all_conversations_mock

factory = FirebaseConnectionFactory()
fc = factory.create_connection("HTTP")
fcm = FirebaseConversation(fc)
fo = FirebaseOrder(fc)
ft = FirebaseToggler()


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
        # header and caches preflight response for a 3600s
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
    final_response = json.dumps({'response': response}), response_code, headers
    return createResponseWithAntiCorsHeaders(final_response)


def update_multiple_conversations(request=None):
    try:
        payload = request.get_json()
        userMessage = payload["userMessage"]
        botAnswer = payload["botAnswer"]
        metaData = payload["metaData"]

        phoneNumber = metaData["phoneNumber"]
        userMessageDict = {"body": userMessage, "time": datetime.datetime.now().strftime('%H:%M'), **metaData}
        botMessageDict = {"body": botAnswer, "time": datetime.datetime.now().strftime('%H:%M'), **metaData,
                          "sender": "Bot"}
        messagePot = [userMessageDict, botMessageDict]

        result = fcm.appendMultipleMessagesToWhatsappNumber(messagesData=messagePot, whatsappNumber=phoneNumber)
        response_code = 200 if result is True else 500
        final_response = json.dumps({'response': 'messages appended successfully'}), response_code

        return createResponseWithAntiCorsHeaders(final_response)

    except Exception as e:
        return createResponseWithAntiCorsHeaders((json.dumps({'error': f"An error occurred: {str(e)}"}), 500))


def order_handler(request):
    # operation = request.headers.get('operation', None)
    operation = request.path.split('/')[-1]

    if request.method == 'POST' and operation == 'create':
        return create_order(request)
    elif request.method == 'GET' and operation == 'read':
        return read_all_orders(request)
    elif request.method == 'PUT' and operation == 'update':
        return update_order(request)
    elif request.method == 'DELETE' and operation == 'delete':
        return delete_order(request)
    else:
        return 'Invalid operation or HTTP method', 400


def create_order(request):
    if request is None or request.method != 'POST':
        return 'Only POST requests are accepted', 405

    try:
        data = request.get_json(force=True)
    except JSONDecodeError as e:
        return f'Invalid JSON payload: {e}', 400

    REQUIRED_FIELDS = ["customerName", "status", "address", "platform", "communication", "orderItems"]
    missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
    if missing_fields:
        return f"{', '.join(missing_fields)} cannot be empty", 400

    for item in data["orderItems"]:
        REQUIRED_ITEM_FIELDS = ["type", "flavors", "size", "quantity", "price"]
        missing_item_fields = [field for field in REQUIRED_ITEM_FIELDS if field not in item]
        if missing_item_fields:
            return f"In orderItems, {', '.join(missing_item_fields)} cannot be empty", 400

    unique_id = fo.createOrder(order_data=data)
    response = f'Order created successfully! UniqueID = {unique_id}', 200
    return createResponseWithAntiCorsHeaders(response)


def read_all_orders(request):
    if request is None or request.method != "GET":
        return "Only GET requests are accepted", 405
    result = fo.getAllOrders()
    return createResponseWithAntiCorsHeaders(result)


def update_order(request):
    if request is None or request.method != 'PUT':
        return 'Only PUT requests are accepted', 405
    if "order_id" not in request.headers:
        return "'order_id' header cannot be empty", 400
    try:
        data = request.get_json(force=True)
    except JSONDecodeError as e:
        return f'Invalid JSON payload: {e}', 400
    order_id = request.headers["order_id"]
    result: bool = fo.updateOrder(order_unique_id=order_id, order_data=data)
    response = "Order updated successfully" if result else f"Error updating order, order {order_id} does not exist"
    response_code = 200 if result else 500
    final_response = json.dumps({'response': response}), response_code
    return createResponseWithAntiCorsHeaders(final_response)


def delete_order(request):
    if request is None or request.method != 'DELETE':
        return 'Only DELETE requests are accepted', 405
    if "order_id" not in request.headers:
        return "'order_id' header cannot be empty", 400
    order_id = request.headers["order_id"]
    result: bool = fo.deleteOrder(order_unique_id=order_id)
    return createResponseWithAntiCorsHeaders(result)


def budget_alert_endpoint(request=None):
    request_content = request.json
    decoded_dict = decode_dict_from_google_cloud_request(request_content)
    moneySpent, costIntervalTime, percentage_achieved = extract_meaningful_info_from_decoded_dict(decoded_dict)
    final_string = send_cloud_warning_email(costIntervalTime, moneySpent, percentage_achieved)
    ft.disable_firebase()
    return final_string, 200


def __main():
    response = get_all_conversations(get_all_conversations_mock())
    response_json = json.loads(response[0])
    return


if __name__ == '__main__':
    __main()

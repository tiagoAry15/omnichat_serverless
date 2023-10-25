import datetime
import json

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
        userMessageDict = {"body": userMessage, "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), **metaData}
        botMessageDict = {"body": botAnswer, "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), **metaData,
                          "sender": "Bot"}
        messagePot = [userMessageDict, botMessageDict]

        result = fcm.appendMultipleMessagesToWhatsappNumber(messagesData=messagePot, whatsappNumber=phoneNumber)
        response_code = 200 if result is True else 500
        final_response = json.dumps({'response': 'messages appended successfully'}), response_code

        return createResponseWithAntiCorsHeaders(final_response)

    except Exception as e:
        return createResponseWithAntiCorsHeaders((json.dumps({'error': f"An error occurred: {str(e)}"}), 500))


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
    if request is None or request.method != "GET":
        return "Only GET requests are accepted", 405
    log_memory_usage()
    result = fo.readAllOrders()
    return createResponseWithAntiCorsHeaders(result)


def update_order(request=None):
    if request is None or request.method != 'PUT':
        return 'Only PUT requests are accepted', 405
    if "order_id" not in request.headers:
        return "'order_id' header cannot be empty", 400
    order_id = request.headers["order_id"]
    remaining_headers = [header for header in request.headers if header != "order_id"]
    result: bool = fo.updateOrder(uniqueOrderId=order_id,
                                  **{header: request.headers[header] for header in remaining_headers})
    response = "order updated successfully" if result else "error updating order, order does not exist"
    response_code = 200 if result else 500
    final_response = json.dumps({'response': response}), response_code
    return createResponseWithAntiCorsHeaders(final_response)


def budget_alert_endpoint(request=None):
    request_content = request.json
    decoded_dict = decode_dict_from_google_cloud_request(request_content)
    moneySpent, costIntervalTime, percentage_achieved = extract_meaningful_info_from_decoded_dict(decoded_dict)
    final_string = send_cloud_warning_email(costIntervalTime, moneySpent, percentage_achieved)
    ft.disable_firebase()
    return final_string, 200


def __main():
    mock = [{
        "body": "Oi",
        "time": "2021-08-01 20:00",
        "sender": "User",
        "from": "whatsapp",
        "phoneNumber": "558599663533"
    },
        {
            "body": "Olá tudo bem?",
            "time": "2021-08-01 20:00",
            "sender": "Bot",
            "from": "whatsapp",
            "phoneNumber": "558599663533"
        }]

    response = fcm.appendMultipleMessagesToWhatsappNumber(mock,"558599663533")
    print(response)
    return


if __name__ == '__main__':
    __main()

import datetime
import json

from factory.core_instantiations import fcm
from utils.cloudFunctionsUtils import log_memory_usage
from utils.corsBlocker import createResponseWithAntiCorsHeaders


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
        metaData.pop("userMessage")
        phoneNumber = metaData["phoneNumber"]
        userMessageDict = {"body": userMessage, "timestamp": datetime.datetime.now().strftime('%d-%b-%Y %H:%M'), **metaData}
        botMessageDict = {"body": botAnswer, "timestamp": datetime.datetime.now().strftime('%d-%b-%Y %H:%M'),**metaData,
                          "sender": "Bot"}
        messagePot = [userMessageDict, botMessageDict]

        result = fcm.appendMultipleMessagesToWhatsappNumber(messagesData=messagePot, whatsappNumber=phoneNumber)
        response_code = 200 if result is True else 500
        final_response = json.dumps({'response': 'messages appended successfully'}), response_code

        return createResponseWithAntiCorsHeaders(final_response)

    except Exception as e:
        return createResponseWithAntiCorsHeaders((json.dumps({'error': f"An error occurred: {str(e)}"}), 500))

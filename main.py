import json

from costs.alerts.handle_alerts import decode_dict_from_google_cloud_request, \
    extract_meaningful_info_from_decoded_dict, send_cloud_warning_email
from cruds.conversation_crud import get_all_conversations, update_conversation, update_multiple_conversations
from cruds.order_crud import delete_order, update_order, read_all_orders, create_order
from factory.core_instantiations import ft
from utils.mocks import get_all_conversations_mock


def __crud_function_redirect(operation_dict, request):
    operation = request.path.split('/')[-1]
    method = request.method

    if operation not in operation_dict:
        valid_operations = '\n → '.join(operation_dict.keys())
        return f'{operation} is an invalid operation. Valid operations are \n →{valid_operations}', 400

    required_method, operation_func = operation_dict[operation]
    if method != required_method:
        return f'Only {required_method} requests are accepted for the operation {operation}', 405

    return operation_func(request)


def conversation_handler(request):
    operation_dict = {
        "get_all_conversations": ("GET", get_all_conversations),
        "update_conversation": ("PUT", update_conversation),
        "update_multiple_conversations": ("PUT", update_multiple_conversations)
    }

    return __crud_function_redirect(operation_dict, request)


def order_handler(request):
    operation_dict = {
        "create": ("POST", create_order),
        "read": ("GET", read_all_orders),
        "update": ("PUT", update_order),
        "delete": ("DELETE", delete_order)
    }

    return __crud_function_redirect(operation_dict, request)


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

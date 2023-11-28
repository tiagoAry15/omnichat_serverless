import json

from costs.alerts.handle_alerts import (decode_dict_from_google_cloud_request,
                                        extract_meaningful_info_from_decoded_dict,
                                        send_cloud_warning_email)
from cruds.conversation_crud import get_all_conversations, update_conversation, update_multiple_conversations
from cruds.order_crud import delete_order, update_order, get_order_handler, create_order
from cruds.user_crud import create_user, get_all_users, update_user, delete_user
from factory.core_instantiations import ft
from utils.mocks import MockRequest, mock_order_1, mock_order_2, update_mult_conv_mock


def __crud_function_redirect(operation_dict, request):
    path_segments = request.path.split('/')
    operation = path_segments[-1]
    url_parameter = None
    if request.method == 'OPTIONS':
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return '', 204, headers
    if operation not in operation_dict:
        if len(path_segments) > 2 and path_segments[-2] in operation_dict:
            operation = path_segments[-2]
            url_parameter = path_segments[-1]
        else:
            valid_operations = '\n → '.join(operation_dict.keys())
            return f'{operation} is an invalid operation. Valid operations are \n →{valid_operations}', 400

    required_method, operation_func = operation_dict[operation]
    if request.method != required_method:
        return f'Only {required_method} requests are accepted for the operation {operation}', 405
    fake_headers = {'Content-Type': 'application/json', 'url_parameter': url_parameter}
    fake_headers.update(request.headers)
    if request.headers.get('Content-Type') == 'application/json':
        try:
            body = request.json
        except json.JSONDecodeError:
            body = {}
    else:
        body = {}
    fake_request_object = MockRequest(path=request.path, method=request.method, headers=fake_headers,
                                      json_data=body)
    return operation_func(fake_request_object)


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
        "read": ("GET", get_order_handler),
        "update": ("PUT", update_order),
        "delete": ("DELETE", delete_order)
    }

    return __crud_function_redirect(operation_dict, request)


def user_handler(request):
    operation_dict = {
        "create": ("POST", create_user),
        "read": ("GET", get_all_users),
        "update": ("PUT", update_user),
        "delete": ("DELETE", delete_user)
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
    # Mocked data for a read operation without a user_id.
    # mock_request1 = MockRequest(path="/user_handler/read", method="GET")
    # response1 = user_handler(mock_request1)
    # print(response1)

    headers = {
        "Content-Type": "application/json"}

    # Mocked data for a read operation with a user_id
    body = {"address": "Rua da Paz 4987", "cpf": "14568598577", "name": "Ednaldo Pereira",
            "phoneNumber": "558597648583"}
    mock_request2 = MockRequest(path="/user_handler/update/NkLuuUc5ArXd6utuICg", method="PUT", json_data=body, headers=headers)
    response2 = user_handler(mock_request2)
    print(response2)

    # mock_request3 = MockRequest(path="/order_handler/create", method="POST", headers=headers, json_data=mock_order_1)
    # response3 = order_handler(mock_request3)
    # print(response3)


    # mock_request4 = MockRequest(path="/order_handler/read/30_Oct_2023_10_54_31_583", method="GET")
    # response4 = order_handler(mock_request3)
    # print(response4)

    # mock_request5 = MockRequest(path="/order_handler/update/2", method="DELETE", json_data=mock_order_2, headers={'Content-Type': 'application/json'})
    # response5 = order_handler(mock_request5)
    # print(response5)




if __name__ == '__main__':
    __main()

import json
from json import JSONDecodeError

from cruds.crud_utils import get_url_param
from factory.core_instantiations import fo
from factory.core_instantiations import g as global_object
from utils.corsBlocker import createResponseWithAntiCorsHeaders


def create_order(request):
    if request is None or request.method != 'POST':
        return 'Only POST requests are accepted', 405
    try:
        data = request.json
    except JSONDecodeError as e:
        return f'Invalid JSON payload: {e}', 400

    REQUIRED_FIELDS = ["customerName", "status", "address", "platform", "communication", "orderItems"]
    field_statuses = {field: 'OK' for field in REQUIRED_FIELDS}

    for field in REQUIRED_FIELDS:
        if field not in data:
            field_statuses[field] = 'missing'

    order_items_status = []
    if "orderItems" in data:
        for item in data["orderItems"]:
            REQUIRED_ITEM_FIELDS = ["type", "flavors", "size", "quantity", "price"]
            item_status = {field: 'OK' for field in REQUIRED_ITEM_FIELDS}
            for field in REQUIRED_ITEM_FIELDS:
                if field not in item:
                    item_status[field] = 'missing'
            order_items_status.append(item_status)
    else:
        field_statuses["orderItems"] = 'missing'

    if any(status == 'missing' for status in field_statuses.values()):
        response = ' | '.join([f'{field} → {status}' for field, status in field_statuses.items()])
        if order_items_status:
            for index, item_status in enumerate(order_items_status):
                response += ' | ' + ' | '.join([f'orderItem {index+1} {field} → {status}'
                                                for field, status in item_status.items()])
        return response, 400

    result: bool = fo.createOrder(order_data=data)
    return createResponseWithAntiCorsHeaders(result)


def get_order_handler(request):
    if request is None or request.method != "GET":
        return "Only GET requests are accepted", 405
    unique_id = request.headers.get('url_parameter')
    if unique_id:
        return read_order_by_id(unique_id)
    else:
        return read_all_orders()


def read_all_orders():
    orders = fo.getAllOrders()
    arrayOfOrders = list(orders.values()) if orders is not None else []
    return createResponseWithAntiCorsHeaders(arrayOfOrders)


def read_order_by_id(order_id):
    if order_id is None:
        return "'url_parameter' cannot be empty. There was no url parameter in the request", 400
    order = fo.getOrder(order_unique_id=order_id)
    return createResponseWithAntiCorsHeaders(order)


def update_order(request):
    if request is None or request.method != 'PUT':
        return 'Only PUT requests are accepted', 405
    url_param = request.headers.get('url_parameter')
    if url_param is None:
        return "'url_parameter' cannot be empty. There was no url parameter in the request", 400
    try:
        data = request.get_json(force=True)
    except JSONDecodeError as e:
        return f'Invalid JSON payload: {e}', 400
    order_id = url_param
    result: bool = fo.updateOrder(order_unique_id=order_id, order_data=data)
    response = "Order updated successfully" if result else f"Error updating order, order {order_id} does not exist"
    response_code = 200 if result else 500
    final_response = json.dumps({'response': response}), response_code
    return createResponseWithAntiCorsHeaders(final_response)


def delete_order(request):
    if request is None or request.method != 'DELETE':
        return 'Only DELETE requests are accepted', 405
    url_param = request.headers.get('url_parameter')
    if url_param is None:
        return "'url_parameter' cannot be empty. There was no url parameter in the request", 400
    order_id = url_param
    result: bool = fo.deleteOrder(order_unique_id=order_id)
    return createResponseWithAntiCorsHeaders(result)

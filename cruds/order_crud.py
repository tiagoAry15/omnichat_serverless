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
    url_param = get_url_param()
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
    url_param = get_url_param()
    if url_param is None:
        return "'url_parameter' cannot be empty. There was no url parameter in the request", 400
    order_id = url_param
    result: bool = fo.deleteOrder(order_unique_id=order_id)
    return createResponseWithAntiCorsHeaders(result)

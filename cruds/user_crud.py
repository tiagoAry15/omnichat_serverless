from requests import JSONDecodeError

from cruds.crud_utils import get_url_param
from factory.core_instantiations import fu
from utils.corsBlocker import getAntiCorsHeaders


def validate_request(request, expected_method):
    if request is None or request.method != expected_method:
        return f'Only {expected_method} requests are accepted', 405
    return None


def get_json_from_request(request):
    try:
        data = request.get_json(force=True)
    except JSONDecodeError as e:
        return None, f'Invalid JSON payload: {e}', 400
    return data, None


def create_user(request=None):
    if request is None or request.method != 'POST':
        return 'Only POST requests are accepted', 405
    try:
        data = request.get_json(force=True)
    except JSONDecodeError as e:
        return f'Invalid JSON payload: {e}', 400
    unique_id = fu.createUser(userData=data)
    response = f'User created successfully! UniqueID = {unique_id}'
    headers = getAntiCorsHeaders()
    return response, 200, headers


def get_user(request=None):
    if request is None or request.method != 'GET':
        return 'Only GET requests are accepted', 405
    url_parameter = request.headers.get('url_parameter')
    if not url_parameter:
        return "'url_parameter' cannot be empty.", 400
    user_id = request.headers['url_parameter']
    user = str(fu.getUser(user_id))
    return user, 200


def update_user(request=None):
    if request is None or request.method != 'PUT':
        return 'Only PUT requests are accepted', 405
    url_param = get_url_param()
    if url_param is None:
        return "'url_parameter' cannot be empty. There was no url parameter in the request", 400
    try:
        data = request.get_json(force=True)
    except JSONDecodeError as e:
        return f'Invalid JSON payload: {e}', 400
    user_id = url_param
    result: bool = fu.updateUser(user_unique_id=user_id, userData=data)
    response = "User updated successfully" if result else f"Error updating user, user {user_id} does not exist"
    response_code = 200 if result else 500
    headers = getAntiCorsHeaders()
    return response, response_code, headers


def delete_user(request=None):
    if request is None or request.method != 'DELETE':
        return 'Only DELETE requests are accepted', 405
    url_param = get_url_param()
    if url_param is None:
        return "'url_parameter' cannot be empty. There was no url parameter in the request", 400
    user_id = url_param
    result: bool = fu.deleteUser(user_unique_id=user_id)
    response = "User deleted successfully" if result else f"Error deleting user, user {user_id} does not exist"
    response_code = 200 if result else 500
    headers = getAntiCorsHeaders()
    return response, response_code, headers

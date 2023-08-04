from django.http import JsonResponse


def createResponseWithAntiCorsHeaders(data):
    response = JsonResponse(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

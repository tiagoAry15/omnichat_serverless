from flask import jsonify


def createResponseWithAntiCorsHeaders(data):
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

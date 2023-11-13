import json

from flask import jsonify, Response


def createResponseWithAntiCorsHeaders(data, response_code=None):
    dump_response = json.dumps(data)
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*"
    }
    return Response(dump_response, status=response_code, headers=response_headers)


def getAntiCorsHeaders():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, PUT",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
    }

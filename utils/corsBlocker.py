import json

from flask import jsonify, Response


def createResponseWithAntiCorsHeaders(data):
    dump_response = json.dumps(data)
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*"
    }
    return Response(dump_response, headers=response_headers)


def getAntiCorsHeaders():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, PUT",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
    }

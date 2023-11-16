import json

from flask import jsonify, Response


def createResponseWithAntiCorsHeaders(data, response_code=200):
    # Converte os dados para JSON
    dump_response = json.dumps(data)

    # Define os cabeçalhos para permitir CORS
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*"
    }

    # Cria a resposta com os cabeçalhos e o código de status
    response = Response(dump_response, status=response_code, headers=response_headers)
    response.mimetype = "application/json"
    return response
def getAntiCorsHeaders():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, PUT",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
    }

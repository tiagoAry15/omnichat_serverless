from typing import List
from unittest.mock import Mock


class MockRequest:
    def __init__(self, path, method, headers=None, json_data=None):
        self.path = path
        self.method = method
        self.headers = headers or {}
        self.json = json_data

    def get_json(self, force=False, silent=False, cache=True):
        return self.json


def test_create_conversation_mock(phoneNumber: str = "+558599171902", body: str = "Olá!", sender: str = "John"):
    # Create a sample input dictionary simulating headers
    sample_headers = {
        "whatsappNumber": phoneNumber,
        "body": body,
        "sender": sender
    }

    # Create a mock request using the sample headers
    return MockRequest(sample_headers)


def get_all_conversations_mock():
    mock_request = Mock()
    mock_request.method = 'GET'
    return mock_request


def test_create_update_conversation_mock():
    test_json = {
        "from": "whatsapp",
        "isBotActive": True,
        "lastMessage_timestamp": "18/08/2023 02:34",
        "messagePot": [
            {
                "body": "oi",
                "id": "b3d9ff41-5219-4dba-9e7a-aa989b695d3f",
                "sender": "Tiago Ary",
                "time": "02:34"
            }
        ],
        "name": "Tiago Ary",
        "phoneNumber": "+558599663533",
        "status": "active",
        "unreadMessages": 4
    }

    return MockRequest(method="GET")


mock_order_1 = {
    "address": "Rua da Justiça 9584",
    "communication": "Janderson@bol.com.br",
    "customerName": "Janderson",
    "observation": "Tirar cebola",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Portuguesa"],
            "size": "Large",
            "quantity": 1,
            "price": 15.00
        },
        {
            "type": "drink",
            "flavors": ["Coca-Cola"],
            "size": "2L",
            "quantity": 1,
            "price": 2.50
        },
        {
            "type": "pizza",
            "flavors": ["Margarita", "Frango com Catupiry"],
            "size": "Large",
            "quantity": 1,
            "price": 17.00
        }
    ],
    "platform": "WhatsApp",
    "status": "Confirmado",

}

mock_order_2 = {
    "address": "Rua Marcos Macedo 700",
    "communication": "558599663533",
    "customerName": "Mateus",
    "observation": "None",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Portuguesa"],
            "size": "Large",
            "quantity": 1,
            "price": 15.00
        },
        {
            "type": "drink",
            "flavors": ["Guaraná"],
            "size": "2L",
            "quantity": 1,
            "price": 2.50
        },
        {
            "type": "pizza",
            "flavors": ["Margarita", "Frango com Catupiry"],
            "size": "Large",
            "quantity": 1,
            "price": 17.00
        }
    ],
    "platform": "WhatsApp",
    "status": "Em preparação",
}


def __main():
    conversation_mock = test_create_conversation_mock()
    return


if __name__ == '__main__':
    __main()

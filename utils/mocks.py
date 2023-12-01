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

mock_user_1 = {"address": "Rua da Paz 4987", "cpf": "14568598577", "name": "Ednaldo Pereira",
            "phoneNumber": "558597648583"}


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
            "price": 30.00
        },
        {
            "type": "drink",
            "flavors": ["Coca-Cola"],
            "size": "2L",
            "quantity": 1,
            "price": 12.50
        },
        {
            "type": "pizza",
            "flavors": ["Margarita", "Frango com Catupiry"],
            "size": "Large",
            "quantity": 1,
            "price": 34.00
        }
    ],
    "platform": "WhatsApp",
    "status": "Confirmado",

}
mock_order_2 = {
    "address": "Rua Marcos Macedo 700",
    "communication": "558599663533",
    "customerName": "Nestor",
    "observation": "Tirar azeitona",
    "orderItems": [

        {
            "type": "drink",
            "flavors": ["Coca-Cola"],
            "size": "2L",
            "quantity": 1,
            "price": 2.50
        },
        {
            "type": "pizza",
            "flavors": ["Marguerita", "Calabresa"],
            "size": "Large",
            "quantity": 1,
            "price": 17.00
        },
        {
            "type": "pizza",
            "flavors": ["Portuguesa", "4 Queijos"],
            "size": "Large",
            "quantity": 1,
            "price": 17.00
        }
    ],
    "totalPrice": 36.50,
    "platform": "Instagram",
    "status": "Cancelado",
}
mock_order_3 = {
    "address": "Avenida dos Pioneiros 123",
    "communication": "paula_insta@insta.com",
    "customerName": "Paula",
    "observation": "Adicionar mais queijo",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["4 Queijos"],
            "size": "Medium",
            "quantity": 2,
            "price": 28.00
        },
        {
            "type": "drink",
            "flavors": ["Guaraná"],
            "size": "1L",
            "quantity": 2,
            "price": 6.00
        },
        {
            "type": "pizza",
            "flavors": ["Calabresa"],
            "size": "Small",
            "quantity": 1,
            "price": 15.00
        }
    ],
    "totalPrice": 49.00,
    "platform": "Instagram",
    "status": "Confirmado",
}

mock_order_4 = {
    "address": "Travessa dos Artistas 456",
    "communication": "carlos@whatsapp.com",
    "customerName": "Carlos",
    "observation": "Sem pimentão",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Pepperoni"],
            "size": "Large",
            "quantity": 1,
            "price": 32.00
        },
        {
            "type": "drink",
            "flavors": ["Sprite"],
            "size": "2L",
            "quantity": 1,
            "price": 7.50
        },
        {
            "type": "pizza",
            "flavors": ["Vegetariana"],
            "size": "Medium",
            "quantity": 1,
            "price": 29.00
        }
    ],
    "totalPrice": 68.50,
    "platform": "WhatsApp",
    "status": "Em Preparação",
}

mock_order_5 = {
    "address": "Rua da Harmonia 789",
    "communication": "messenger_ana@messenger.com",
    "customerName": "Ana",
    "observation": "Cortar em quadrados",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Atum"],
            "size": "Large",
            "quantity": 1,
            "price": 29.50
        },
        {
            "type": "drink",
            "flavors": ["Fanta"],
            "size": "600ml",
            "quantity": 2,
            "price": 4.50
        }
    ],
    "totalPrice": 38.50 ,
    "platform": "Messenger",
    "status": "A caminho",
}
mock_order_6 = {
    "address": "Alameda dos Anjos 1010",
    "communication": "gabriel_ig@instagram.com",
    "customerName": "Gabriel",
    "observation": "Dobrar a borda",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Bacon"],
            "size": "Large",
            "quantity": 1,
            "price": 35.00
        },
        {
            "type": "drink",
            "flavors": ["Pepsi"],
            "size": "2L",
            "quantity": 1,
            "price": 8.00
        },
        {
            "type": "pizza",
            "flavors": ["Frango com Catupiry", "Marguerita"],
            "size": "Large",
            "quantity": 1,
            "price": 33.00
        }
    ],
    "totalPrice": 76.00,
    "platform": "Instagram",
    "status": "Finalizado",
}

mock_order_7 = {
    "address": "Avenida Central 1450",
    "communication": "lucas_messenger@messenger.com",
    "customerName": "Lucas",
    "observation": "Não colocar orégano",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Napolitana"],
            "size": "Medium",
            "quantity": 1,
            "price": 22.00
        },
        {
            "type": "drink",
            "flavors": ["Água Mineral"],
            "size": "500ml",
            "quantity": 1,
            "price": 2.00
        }
    ],
    "totalPrice": 24.00,
    "platform": "Messenger",
    "status": "Confirmado",
}

mock_order_8 = {
    "address": "Rua do Comércio 78",
    "communication": "vitoria_whatsapp@whatsapp.com",
    "customerName": "Vitória",
    "observation": "Extra bacon",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Pepperoni"],
            "size": "Large",
            "quantity": 1,
            "price": 32.00
        },
        {
            "type": "pizza",
            "flavors": ["Bacon"],
            "size": "Large",
            "quantity": 1,
            "price": 35.00
        }
    ],
    "totalPrice": 67.00,
    "platform": "WhatsApp",
    "status": "Em transporte",
}

mock_order_9 = {
    "address": "Praça da Liberdade 42",
    "communication": "joao_instagram@instagram.com",
    "customerName": "João",
    "observation": "Sem cebola",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Portuguesa"],
            "size": "Large",
            "quantity": 1,
            "price": 30.00
        },
        {
            "type": "drink",
            "flavors": ["Suco de Laranja"],
            "size": "1L",
            "quantity": 1,
            "price": 10.00
        }
    ],
    "totalPrice": 40.00,
    "platform": "Instagram",
    "status": "Preparando",
}

mock_order_10 = {
    "address": "Beco Diagonal 93",
    "communication": "helena_messenger@messenger.com",
    "customerName": "Helena",
    "observation": "Trocar azeitonas por milho",
    "orderItems": [
        {
            "type": "pizza",
            "flavors": ["Chocolate"],
            "size": "Small",
            "quantity": 1,
            "price": 18.00
        },
        {
            "type": "drink",
            "flavors": ["Chá Gelado"],
            "size": "300ml",
            "quantity": 2,
            "price": 5.00
        },
        {
            "type": "pizza",
            "flavors": ["Frango com Catupiry"],
            "size": "Medium",
            "quantity": 1,
            "price": 53.00
        }
    ],
    "totalPrice": 48.00,
    "platform": "Messenger",
    "status": "Aguardando confirmação",
}

mock_orders = [mock_order_1,
               mock_order_2,
               mock_order_3,
               mock_order_4,
               mock_order_5,
               mock_order_6,
                mock_order_7,
                mock_order_8,
                mock_order_9,
                mock_order_10
               ]

update_mult_conv_mock = {"userMessage": "vou querer um guaraná e dois sucos de laranja", "botAnswer": "Vou é um tipo de endereço inválido. Por favor, use um tipo válido por exemplo Rua, Avenida, Travessa, etc)", "metaData": {"sender": "Tiago", "from": ["whatsapp", "+558599663533"], "phoneNumber": "558599663533", "userMessage": "vou querer um guaraná e dois sucos de laranja", "ip": "127.0.0.1"}}


def __main():
    conversation_mock = test_create_conversation_mock()
    return


if __name__ == '__main__':
    __main()

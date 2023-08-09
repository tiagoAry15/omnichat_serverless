class MockRequest:
    def __init__(self, headers):
        self.headers = headers


def test_create_conversation_mock(phoneNumber: str = "+558599171902", body: str = "Olá!", sender: str = "John"):
    # Create a sample input dictionary simulating headers
    sample_headers = {
        "whatsappNumber": phoneNumber,
        "body": body,
        "sender": sender
    }

    # Create a mock request using the sample headers
    return MockRequest(sample_headers)

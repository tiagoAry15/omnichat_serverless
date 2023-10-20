import json
import requests


def getRequisitionMockup(url: str = 'https://5463-168-232-84-75.ngrok-free.app/budget-alert'):
    body = {
        "message": {
            "attributes": {
                "billingAccountId": "013C96-D972F4-E5734C",
                "budgetId": "e242921d-7a01-4bb0-b0c8-343a7d519e79",
                "schemaVersion": "1.0"
            },
            "data": "ewogICJidWRnZXREaXNwbGF5TmFtZSI6ICJMaW1pdGUiLAogICJhbGVydFRocmVzaG9sZEV4Y2VlZGVkIjogMC41LAogICJjb"
                    "3N0QW1vdW50IjogNjUuMzcsCiAgImNvc3RJbnRlcnZhbFN0YXJ0IjogIjIwMjMtMTAtMDFUMDc6MDA6MDBaIiwKICAiYnVk"
                    "Z2V0QW1vdW50IjogMTAwLjAsCiAgImJ1ZGdldEFtb3VudFR5cGUiOiAiU1BFQ0lGSUVEX0FNT1VOVCIsCiAgImN1cnJlbmN"
                    "5Q29kZSI6ICJCUkwiCn0=",
            "messageId": "8903375550464108",
            "message_id": "8903375550464108",
            "publishTime": "2023-10-19T14:46:29.698Z",
            "publish_time": "2023-10-19T14:46:29.698Z"
        },
        "subscription": "projects/pizzadobill-rpin/subscriptions/budget-alert-webhook"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, data=json.dumps(body), headers=headers)


def __main():
    response = getRequisitionMockup()
    print(response.text)


if __name__ == '__main__':
    __main()

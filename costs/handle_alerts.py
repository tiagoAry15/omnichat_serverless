from googleapiclient import discovery
from googleapiclient.errors import HttpError
import base64
import json


def handleBudgetAlert(data, context):
    pubsub_message = base64.b64decode(data['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)

    # Extract budget details from the message
    budget_name = message_data.get("budgetDisplayName")
    cost_amount = message_data.get("costAmount")
    # ... add other fields as required

    # Now, you can write logic to disable the API or take any other action based on the budget details
    # ... your logic here

    return f"Processed budget alert for {budget_name} with cost {cost_amount}"


def __main():
    mock_pubsub_message = {
        'data': base64.b64encode('Your test message here'.encode('utf-8')),
        'attributes': {}
    }
    handleBudgetAlert(mock_pubsub_message, None)


if __name__ == '__main__':
    __main()

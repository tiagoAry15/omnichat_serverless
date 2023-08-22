import html
import json
import requests
import xml.etree.ElementTree as ElementTree
from requestTests.requisitionBoilerPlate import getTwilioBoilerPlate, getDialogflowBoilerPlate


def sendTwilioRequest(url: str = "http://localhost:3000/twilioSandbox", body: str = "Oii"):
    # Define headers for the request

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/91.0.4472.124 Safari/537.36"
    }

    # Define the form data
    data = getTwilioBoilerPlate(body=body)
    return requests.post(url, headers=headers, data=data)


def sendDialogflowRequest(url: str = "http://localhost:3000/webhookForIntent", body_content: str = "Oii"):
    # Define headers for the request
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/91.0.4472.124 Safari/537.36"
    }
    # Body data as a JSON string
    body_content = getDialogflowBoilerPlate(body=body_content)
    # Send the request
    return requests.post(url, headers=headers, data=body_content)


def convertResponseToUtf8(response: requests.Response) -> str:
    responseXmlContent = response.text
    formatted = html.unescape(responseXmlContent)
    root = ElementTree.fromstring(formatted)
    return root.find(".//Body").text


def __main():
    response = sendTwilioRequest(body="Oii")
    print(convertResponseToUtf8(response))


if __name__ == "__main__":
    __main()
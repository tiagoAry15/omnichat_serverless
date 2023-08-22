import time
from typing import List

from requestTests.httpCalls import sendTwilioRequest, convertResponseToUtf8


def chainedHttpCalls(messageList: List[str], delay: int):
    botResponsePot = []
    for message in messageList:
        print("\u001b[32m" + f"User: {message}" + "\u001b[0m")
        rawResponse = sendTwilioRequest(body=message)
        textResponse = convertResponseToUtf8(rawResponse)
        print("\u001b[34m" + f"Bot: {textResponse}" + "\u001b[0m")
        botResponsePot.append(textResponse)
    return botResponsePot


def __getSignedInMessageList():
    return ["Oii", "Vou querer uma pizza meia calabresa meia margherita e uma pizza de frango", "sim",
            "vou querer um guaraná e dois sucos de laranja", "pix"]


def __getFullPathMessageList():
    return ["Oii", "Clark Kent", "Rua da Paz 2172", "17454565899", "Ok",
            "Vou querer uma pizza meia calabresa meia margherita e uma pizza de frango", "sim",
            "vou querer um guaraná e dois sucos de laranja", "pix"]


def __main():
    messageList = __getSignedInMessageList()
    results = chainedHttpCalls(messageList, 3500)
    return


if __name__ == "__main__":
    __main()
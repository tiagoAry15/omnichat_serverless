import random
import string
from datetime import datetime, timedelta
from typing import List


def createRandomIdString() -> str:
    random_string = ''.join(random.choice(string.hexdigits.upper()) for _ in range(32))
    formatted_string = '-'.join([
        random_string[:8], random_string[8:12], random_string[12:16],
        random_string[16:20], random_string[20:]
    ])
    return formatted_string


def generateRandomFloatInRange(number) -> float:
    lower_bound = number - (number * 0.1)
    upper_bound = number + (number * 0.1)
    random_float = random.uniform(lower_bound, upper_bound)
    return random_float


def generateRandomPhoneNumber() -> str:
    ddd = random.randint(10, 99)
    firstHalf = random.randint(1001, 9999)
    secondHalf = random.randint(1001, 9999)
    return f"+55 ({ddd}) 9{firstHalf}-{secondHalf}"


def __generateRandomTime():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    # Formatting the time as HH:MM
    return f"{hour:02d}:{minute:02d}"


def add_minutes_to_time(timeString: str, minutesToAdd: int) -> str:
    # Convert the input time string to a datetime object
    inputTime = datetime.strptime(timeString, "%H:%M")

    # Calculate the new time after adding minutes
    newTime = inputTime + timedelta(minutes=minutesToAdd)

    # Format the new time as HH:MM
    return newTime.strftime("%H:%M")


def generateRandomMessagePot(size: int, senderName: str, _from: str, phoneNumber: str) -> List:
    dummyMessages = ["Oi", "Olá! Eu sou o bot", "Como você vai bot?", "Vou muito bem, obrigado! E você?",
                     "Vou bem também, obrigado por perguntar!", "Como foi o seu dia hoje?", "Foi bom, e o seu?",
                     "Foi maravilhoso. Não fiz muita coisa, mas o dia foi bom!", "Que bom!"]
    pot = []
    startingTime = __generateRandomTime()
    currentIndex = 0
    while currentIndex != size:
        sender = senderName if currentIndex % 2 == 0 else "bot"
        nextMessage = dummyMessages.pop(0)
        conversationDict = {"body": nextMessage, "from": _from, "id": createRandomIdString(),
                            "phoneNumber": phoneNumber, "sender": sender, "timestamp": startingTime}
        pot.append(conversationDict)
        currentIndex += 1
        startingTime = add_minutes_to_time(startingTime, 1)
    return pot

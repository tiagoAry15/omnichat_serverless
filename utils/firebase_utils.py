import datetime
import json
import re
import uuid


def organizeSingleMessageData(messageData: list[dict], whatsappNumber: str, all_conversations: dict):
    uniqueId = searchUniqueIdAmongConversations(conversationData=all_conversations, userWhatsappNumber=whatsappNumber)
    newMessagePot = []
    for message in messageData:
        new_message = dict(message)
        new_message['id'] = str(uuid.uuid4())
        new_message.pop('from', None)
        new_message.pop('phoneNumber', None)
        newMessagePot.append(new_message)
    if uniqueId:
        conversationData = all_conversations[uniqueId]
        conversationData["messagePot"] += newMessagePot
        conversationData['lastMessage_timestamp'] = newMessagePot[-1]['timestamp']
        conversationData['unreadMessages'] += len(newMessagePot)
        return uniqueId, conversationData
    else:
        conversationData = {
            "name": messageData[0]['sender'],
            "status": "active",
            "phoneNumber": whatsappNumber,
            "from": messageData[0]['from'],
            "messagePot": newMessagePot,
            "unreadMessages": len(newMessagePot),
            "lastMessage_timestamp": newMessagePot[-1]['timestamp'],
            "isBotActive": True,
        }
        return None, conversationData


def searchUniqueIdAmongConversations(conversationData: dict, userWhatsappNumber: str) -> str or None:
    if conversationData is None:
        return None
    for uniqueId, conversation in conversationData.items():
        if 'phoneNumber' in conversation and conversation['phoneNumber'] == userWhatsappNumber:
            return uniqueId
    return None


def convert_string_to_dict(rules_str: str) -> dict:
    # Remove trailing commas
    cleaned_str = re.sub(r',\s*}', '}', rules_str)
    cleaned_str = re.sub(r',\s*\]', ']', cleaned_str)

    return json.loads(cleaned_str)

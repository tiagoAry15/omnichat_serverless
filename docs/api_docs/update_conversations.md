# Update Conversation Endpoint

**Endpoint:** `/update_conversation`

**Method:** `POST`

## Request Headers

- `whatsappNumber` (string, required): The phone number associated with the conversation.
- `body` (string, required): The body of the message to be appended to the conversation.
- `sender` (string, required): The name of the message sender.

## Response

HTTP status code 200: Conversation updated successfully.

## Description

This endpoint allows you to update a conversation by appending a new message to the conversation's message history.

### Request Example

```http
POST /update_conversation HTTP/1.1
Host: your-api-host.com
whatsappNumber: '+558599663533'
body: 'New message content'
sender: 'Your Name'
```

### Response Example
```http
HTTP/1.1 200 OK
"Conversation updated successfully."
````

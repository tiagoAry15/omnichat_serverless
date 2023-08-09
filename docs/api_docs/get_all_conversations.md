# Get All Conversations Endpoint

**Endpoint:** `/get_all_conversations`

**Method:** `GET`

**Response:** 

- A JSON object with the messages data
- HTTP status code 200

**Response Example:**
```json
{
   "from":"whatsapp",
   "id":"44b81003-9e4e-4164-909e-b3d6a437728d",
   "lastMessage_timestamp":"09:19",
   "messagePot":[
      {
         "body":"oi",
         "from":"whatsapp",
         "id":"06c8681b-b9d9-4daf-a458-a4f1c0e5a7c9",
         "phoneNumber":"+558599663533",
         "sender":"Tiago Ary",
         "time":"09:19"
      },
      {
         "body":"Por favor, ligue a API",
         "id":"695b995c-219e-40fd-819a-2366b81fe91f",
         "phoneNumber":"+558599663533",
         "sender":"ChatBot",
         "time":"09:19"
      },
      {
         "body":"oi",
         "from":"whatsapp",
         "id":"06c8681b-b9d9-4daf-a458-a4f1c0e5a7c9",
         "phoneNumber":"+558599663533",
         "sender":"Tiago Ary",
         "time":"09:19"
      }
   ],
   "name":"Tiago Ary",
   "phoneNumber":"+558599663533",
   "status":"active",
   "unreadMessages":0
}
````

**Response Description:**
- `from`: The platform from which the message was sent (e.g., WhatsApp)
- `id`: The conversation unique identifier
- `lastMessage_timestamp`: The timestamp indicating when the last message was received.
- `messagePot`: An array containing all the messages exchanged in the conversation.
- `messagePot.body`: The message body.
- `messagePot.from`: The platform from which the message was sent (e.g., WhatsApp)
- `messagePot.id`: The message unique identifier
- `messagePot.phoneNumber`: The phone number of the message sender.
- `messagePot.sender`: The name of the message sender.
- `messagePot.time`: The timestamp indicating when the message was received.
- `name`: The name of the conversation owner.
- `phoneNumber`: The phone number of the conversation owner.
- `status`: The conversation status (e.g., active).
- `unreadMessages`: The number of unread messages in the conversation.


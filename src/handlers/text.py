# src/handlers/text.py
import json



async def handle_text_message(message, client):

    response_text = await client.text_chat(text=message)

    return json.dumps({
        "type": "response",
        "data": response_text,
    })

# src/handlers/text.py
import json



async def handle_text_message(message, meet_key, client):

    response_text = await client.text_chat(text=message, session_id=meet_key)

    return json.dumps({
        "type": "response",
        "data": response_text,
        "session_id": meet_key
    })

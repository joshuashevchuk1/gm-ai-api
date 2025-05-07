# src/handlers/text.py
import json



async def handle_text_message(data, client):

    text = data.get("text")
    meet_key = data.get("meet_key")

    response_text = await client.text_chat(text=text, session_id=meet_key)

    return json.dumps({
        "type": "response",
        "data": response_text,
        "session_id": meet_key
    })

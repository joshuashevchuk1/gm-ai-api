# src/handlers/text.py
import json



async def handle_text_message(data, meet_key, client):

    text = data.get("text")

    response_text = await client.text_chat(text=text, session_id=meet_key)

    return json.dumps({
        "type": "response",
        "data": response_text,
        "session_id": meet_key
    })

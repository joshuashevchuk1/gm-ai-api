

async def handle_text_message(message: str, openai_client):
    response = openai_client.text_chat(message)
    return response

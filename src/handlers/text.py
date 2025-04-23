

async def handle_text_message(message: str, client):
    response = await client.text_chat(message)
    return  response


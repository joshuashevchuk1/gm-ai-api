import io

async def handle_audio_message(message, openai_client):
    # Case 1: message is a dict with a 'file' object (e.g., from multipart form upload)
    file = message.get("file")
    raw_audio = message.get("raw_audio")

    if file:
        audio_bytes = await file.read()
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = getattr(file, "filename", "upload.wav")

    # Case 2: Raw audio bytes (e.g., from WebSocket or HTTP body)
    elif raw_audio:
        audio_file = io.BytesIO(raw_audio)
        audio_file.name = "buffer.wav"

    else:
        return "No audio data found."

    response = await openai_client.audio_chat(audio_file)
    return response

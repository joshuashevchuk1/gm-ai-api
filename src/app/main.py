import asyncio
import json

import websockets
import logging

from src.clients.openai import OpenaiClient
from src.handlers.text import handle_text_message
from src.handlers.audio import handle_audio_message

logging.basicConfig(level=logging.INFO)

openai_client = OpenaiClient()

async def handle_message(websocket):
    async for raw in websocket:
        try:
            message = json.loads(raw)
            msg_type = message.get("type")
            data = message.get("data")

            if msg_type == "text":
                response = await handle_text_message(data, openai_client)
            elif msg_type == "audio-buffer":
                response = await handle_audio_message(data, openai_client)
            elif msg_type == "audio-file":
                response = await handle_audio_message(data, openai_client)
            else:
                response = "Unrecognized message type."

            await websocket.send(response)
        except Exception as e:
            await websocket.send(f"Error: {str(e)}")

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        logging.info("Server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

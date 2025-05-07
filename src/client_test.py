import asyncio
import websockets
import json
import base64

async def client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            msg_type = input("Enter message type (text/audio-buffer/audio-file): ").strip().lower()
            meet_key = "12345"

            if msg_type == "text":
                msg = input("You: ")
                message = json.dumps({"type": "text","meet_key": meet_key, "message": msg})
            elif msg_type == "audio-buffer":
                audio_data = input("Enter audio buffer data (base64 encoded): ").strip()
                message = json.dumps({"type": "audio-buffer", "data": audio_data})
            elif msg_type == "audio-file":
                file_path = input("Enter the file path for audio: ").strip()
                try:
                    with open(file_path, "rb") as audio_file:
                        audio_data = audio_file.read()
                        audio_data_base64 = base64.b64encode(audio_data).decode("utf-8")
                        message = json.dumps({"type": "audio-file", "data": audio_data_base64})
                except Exception as e:
                    print(f"Error reading audio file: {e}")
                    continue
            else:
                print("Invalid message type!")
                continue

            try:
                await websocket.send(message)
                print(f"> Sent: {message}")

                response = await websocket.recv()
                print(f"< Received: {response}")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")
                break

if __name__ == "__main__":
    asyncio.run(client())

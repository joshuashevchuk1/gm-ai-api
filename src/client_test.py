import asyncio
import websockets
import json
import base64

# Function to send messages to the WebSocket server
async def send_messages(websocket):
    while True:
        msg_type = input("Enter message type (text/audio-buffer/audio-file): ").strip().lower()

        # If the user wants to send a text message
        if msg_type == "text":
            msg = input("You: ")
            message = json.dumps({"type": "text", "data": msg})

        # If the user wants to send an audio buffer
        elif msg_type == "audio-buffer":
            audio_data = input("Enter audio buffer data (base64 encoded): ").strip()
            message = json.dumps({"type": "audio-buffer", "data": audio_data})

        # If the user wants to send an audio file
        elif msg_type == "audio-file":
            file_path = input("Enter the file path for audio: ").strip()
            try:
                with open(file_path, "rb") as audio_file:
                    audio_data = audio_file.read()  # Read the audio file as bytes
                    audio_data_base64 = base64.b64encode(audio_data).decode("utf-8")  # Convert bytes to base64
                    message = json.dumps({"type": "audio-file", "data": audio_data_base64})
            except Exception as e:
                print(f"Error reading audio file: {e}")
                continue
        else:
            print("Invalid message type! Choose between 'text', 'audio-buffer', or 'audio-file'.")
            continue

        try:
            await websocket.send(message)  # Send the message to the WebSocket server
            print(f"> Sent: {message}")

            # Wait for the server's response after sending the message
            response = await websocket.recv()  # Blocking call until a message is received
            print(f"< Received: {response}")

        except json.JSONDecodeError as e:
            print(f"Error encoding message: {e}")
            continue
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed with error: {e}")
            break

# Function to receive messages from the WebSocket server
async def receive_messages(websocket):
    while True:
        try:
            raw = await websocket.recv()  # Receive raw message from server
            message = json.loads(raw)  # Parse the incoming message
            print(f"< Received: {message}")
        except json.JSONDecodeError as e:
            print(f"Error decoding message: {e}")
            continue  # Skip this iteration if the message is invalid
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed while receiving: {e}")
            break

# Main function to connect to the WebSocket server
async def client():
    uri = "ws://localhost:8000/ws"  # Update to your FastAPI WebSocket URI
    async with websockets.connect(uri) as websocket:
        # Run both send and receive tasks concurrently
        send_task = asyncio.create_task(send_messages(websocket))
        receive_task = asyncio.create_task(receive_messages(websocket))

        # Await both tasks simultaneously
        await asyncio.gather(send_task, receive_task)

if __name__ == "__main__":
    asyncio.run(client())

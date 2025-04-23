import uvicorn
import json
import logging

from src.clients.openai import OpenaiClient
from fastapi import WebSocket, WebSocketDisconnect
from src.handlers.text import handle_text_message
from src.handlers.audio import handle_audio_message
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)


class GmAiApp:
    def __init__(self, port: int):
        self.port = port
        self.app = FastAPI(
            title="GM Base API",
            description="A modular FastAPI app with home, health check endpoints, and WebSocket support.",
            version="1.0.0",
        )
        self.include_routes()
        self.client = OpenaiClient()

    def include_routes(self):
        # Add WebSocket route for /ws
        self.app.add_websocket_route("/ws", self.websocket_handler)

    async def websocket_handler(self, websocket: WebSocket):
        await websocket.accept()  # Accept the WebSocket connection
        try:
            while True:
                try:
                    raw = await websocket.receive_text()  # Receive the message as a string
                    logging.info(f"Received message: {raw}")

                    message = json.loads(raw)  # Parse the incoming JSON message
                    msg_type = message.get("type")  # Get the message type
                    data = message.get("data")  # Get the data payload

                    # Handle different types of messages
                    if msg_type == "text":
                        response = await handle_text_message(data, self.client)  # Process text messages
                    elif msg_type in ("audio-buffer", "audio-file"):
                        response = await handle_audio_message(data, self.client)  # Process audio messages
                    else:
                        response = json.dumps({"error": "Unrecognized message type"})  # Handle unrecognized types

                    logging.info(f"Sending response: {response}")  # Log response for debugging
                    await websocket.send_text(response)  # Send the response back to the WebSocket client
                except json.JSONDecodeError:
                    logging.exception("Error decoding JSON")
                    await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))
                except Exception as e:
                    logging.exception(f"Error while processing WebSocket message: {e}")
                    await websocket.send_text(json.dumps({"error": str(e)}))

        except WebSocketDisconnect:
            logging.info("WebSocket disconnected")
        except Exception as e:
            logging.exception(f"Unexpected error: {e}")

    def run_server(self):
        # Run the server using Uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)


if __name__ == "__main__":
    app = GmAiApp(port=8000)
    app.run_server()

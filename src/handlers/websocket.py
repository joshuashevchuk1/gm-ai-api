# routes/websocket_route.py
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.handlers.text import handle_text_message
from src.clients.openai import OpenaiClient

router = APIRouter()

logging.basicConfig(level=logging.INFO)

client = OpenaiClient()

@router.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    try:
        while True:
            try:
                raw = await websocket.receive_text()  # Receive the message as a string
                logging.info(f"Received message: {raw}")

                message = json.loads(raw)  # Parse the incoming JSON message
                msg_type = message.get("type")  # Get the message type
                meet_key = message.get("meet_key")
                data = message.get("message")  # Get the data payload

                # Handle different types of messages
                if msg_type == "text":
                    response = await handle_text_message(data, meet_key, client)  # Process text messages
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

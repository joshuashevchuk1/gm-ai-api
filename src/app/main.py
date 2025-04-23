import uvicorn
import logging

from src.clients.openai import OpenaiClient
from src.handlers import routers,websocket_route

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)


class GmAiApp:
    def __init__(self, port: int):
        self.port = port
        self.app = FastAPI(
            title="GM Base API",
            description="A modular FastAPI app with home, health check endpoints, and WebSocket support.",
            version="1.0.0",
            ws_ping_interval=30,
            ws_ping_timeout=60
        )
        self.include_routes()
        self.client = OpenaiClient()

    def include_routes(self):
        for route in routers:
            self.app.include_router(route)

        self.app.add_websocket_route("/ws", websocket_route)

    def run_server(self):
        # Run the server using Uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)


if __name__ == "__main__":
    app = GmAiApp(port=8000)
    app.run_server()

# routes/__init__.py

from .home import router as home
from .health import router as health
from .websocket import router as websocket

routers = [home,health]
websocket_route = websocket

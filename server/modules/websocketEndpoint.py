from .serverInterface import Server
from fastapi import WebSocket

def addFunctionalityTo(server: Server):
    @server.app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        server.currentWebsocket = websocket
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
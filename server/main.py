from fastapi import FastAPI
import os
import asyncio


from .modules import serverInterface
from .modules.httpEndpoints import getDiagramDefinition
from .modules.httpEndpoints import getDiagram

from .modules import watchAndReloadDefinition
from .modules import websocketEndpoint

from fastapi.middleware.cors import CORSMiddleware

class Server(serverInterface.Server):

    def __init__(self):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3429","http://127.0.0.1:3429"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.queue = asyncio.Queue()

        # self.shouldProvide(watchAndReloadDefinition)
        self.shouldProvide(getDiagramDefinition)
        self.shouldProvide(getDiagram)
        self.shouldProvide(websocketEndpoint)

server = Server()
app = server.app
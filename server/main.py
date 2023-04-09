from fastapi import FastAPI
import os
import asyncio


from .modules import serverInterface
from .modules.httpEndpoints import getDiagramDefinition
from .modules.httpEndpoints import getFrontend
from .modules.httpEndpoints import getDiagram

from .modules import watchAndReloadDefinition
from .modules import websocketEndpoint

class Server(serverInterface.Server):

    def __init__(self):
        self.WATCH_REPOSITORY_PATH = os.environ["WATCH_REPOSITORY_PATH"]
        self.app = FastAPI()
        self.queue = asyncio.Queue()

        self.shouldProvide(watchAndReloadDefinition)
        self.shouldProvide(getDiagramDefinition)
        self.shouldProvide(getDiagram)
        self.shouldProvide(websocketEndpoint)
        # Frontend catch-all must be last
        self.shouldProvide(getFrontend)


server = Server()
app = server.app
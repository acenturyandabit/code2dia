from typing import Coroutine
from fastapi import FastAPI
import asyncio

class Server:
    app: FastAPI
    WATCH_REPOSITORY_PATH: str
    queue: asyncio.Queue
    generateObjectsAndStyle: Coroutine[None,None,str]

    def shouldProvide(self, module):
        module.addFunctionalityTo(self)

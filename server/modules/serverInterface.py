from typing import Coroutine
from fastapi import FastAPI
import asyncio

class Server:
    app: FastAPI
    queue: asyncio.Queue
    generateObjectsAndStyle: Coroutine[None,None,str]

    def shouldProvide(self, module):
        module.addFunctionalityTo(self)

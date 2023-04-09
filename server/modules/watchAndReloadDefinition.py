from .serverInterface import Server
import asyncio
from watchfiles import awatch, Change, DefaultFilter

def addFunctionalityTo(server: Server):
    @server.app.on_event("startup")
    async def startup_event():
        asyncio.create_task(watchFile(server))

async def watchFile(server: Server):
    async for changes in awatch(server.WATCH_REPOSITORY_PATH):
        for change in changes:
            if change[0] == Change.modified:
                server.queue.put("fileChange")


class ThreeFileWatcher():
    DefaultFilter
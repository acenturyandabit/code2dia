from ..serverInterface import Server
from fastapi.staticfiles import StaticFiles

def addFunctionalityTo(server: Server):
    server.app.mount("/", StaticFiles(directory="server/frontend",html = True), name="static")

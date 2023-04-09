from ..serverInterface import Server
from fastapi.responses import PlainTextResponse
from subprocess import PIPE
import subprocess


def addFunctionalityTo(server: Server):
    @server.app.post("/getDiagramDefinition")
    async def getDiagramDefinition():
        # Asyncio subprocess doesn't work on windows, must use regular subprocess and block :(
        cmd = ["python","diagramDefinition.py", 
            "--path", server.WATCH_REPOSITORY_PATH
        ]
        process = subprocess.run(cmd,stdout=PIPE)
        stdout = process.stdout.decode("utf-8")
        return PlainTextResponse(stdout)

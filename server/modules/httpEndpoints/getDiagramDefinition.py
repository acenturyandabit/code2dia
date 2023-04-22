from ..serverInterface import Server
from fastapi.responses import PlainTextResponse
from fastapi import Body
from subprocess import PIPE
import json
import subprocess


def addFunctionalityTo(server: Server):
    @server.app.post("/getDiagramDefinition")
    async def getDiagramDefinition(body=Body()):
        # Asyncio subprocess doesn't work on windows, must use regular subprocess and block :(
        bodyJson = json.loads(body.decode("utf-8"))
        cmd = ["python","diagramDefinition.py", 
            "--path", bodyJson.repoPath
        ]
        process = subprocess.run(cmd,stdout=PIPE)
        stdout = process.stdout.decode("utf-8")
        return PlainTextResponse(stdout)

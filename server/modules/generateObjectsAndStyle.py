from .serverInterface import Server
import os
import asyncio
from fastapi import Body
import json


def addFunctionalityTo(server: Server):
    async def generateObjectsAndStyle(body=Body()):
        diaDefPath = "diagramDefinition.py"
        bodyJson = json.loads(body.decode("utf-8"))
        inRepoDiaDefPath = bodyJson.repoPath + os.path.sep + diaDefPath
        if os.path.exists(inRepoDiaDefPath):
            diaDefPath = inRepoDiaDefPath
        proc = await asyncio.create_subprocess_shell(
            f"python {diaDefPath}"
        )
        (stdoutBytes ,_) = await proc.communicate()
        objectRelationsStyle = stdoutBytes.decode("utf-8")
        return objectRelationsStyle

    server.generateObjectsAndStyle = generateObjectsAndStyle

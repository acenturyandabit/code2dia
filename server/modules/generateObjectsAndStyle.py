from .serverInterface import Server
import os
import asyncio


def addFunctionalityTo(server: Server):
    async def generateObjectsAndStyle():
        diaDefPath = "diagramDefinition.py"
        inRepoDiaDefPath = server.WATCH_REPOSITORY_PATH + os.path.sep + diaDefPath
        if os.path.exists(inRepoDiaDefPath):
            diaDefPath = inRepoDiaDefPath
        proc = await asyncio.create_subprocess_shell(
            f"python {diaDefPath}"
        )
        (stdoutBytes ,_) = await proc.communicate()
        objectRelationsStyle = stdoutBytes.decode("utf-8")
        return objectRelationsStyle

    server.generateObjectsAndStyle = generateObjectsAndStyle

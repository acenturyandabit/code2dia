from ..serverInterface import Server
import code2dia
from fastapi import Body
from fastapi.responses import JSONResponse


def addFunctionalityTo(server: Server):
    @server.app.post("/getDiagram")
    async def getDiagram(body=Body()):
        plantuml, diagramSVG = await code2dia.convertDiagramToSvg(body.decode("utf-8"))
        return JSONResponse({
            "plantuml": plantuml,
            "svg": diagramSVG
        })
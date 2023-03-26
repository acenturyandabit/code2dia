from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, PlainTextResponse
import os
from pathlib import Path
from watchfiles import awatch, Change
import asyncio
import re
import code2dia
import logging


class Server:
    def __init__(self, DIAGRAM_DEFINITION_FILE):
        self.DIAGRAM_DEFINITION_FILE = DIAGRAM_DEFINITION_FILE
        self.DIAGRAM_OUTPUT_FILE = re.sub("\.py$", ".svg", DIAGRAM_DEFINITION_FILE)

        app = FastAPI()
        self.app = app

        self.websocket = None

        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>{DIAGRAM_DEFINITION_FILE}</title>
                <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
            </head>
            <body style="margin:0">
                <div id="container" style="width: 90vw; height: 90vh; border:1px solid black; ">
                </div>
                <script>
                    var ws = new WebSocket("ws://localhost:8000/ws");
                    ws.onmessage = function(event) {{
                        if (event.data=="reload"){{
                            reload();
                        }}
                    }};

                    const reload = async ()=>{{
                        const diagramResponse = await fetch("/diagram");
                        const diagramText = await diagramResponse.text()
                        const containerEl = document.querySelector("#container");
                        containerEl.innerHTML = diagramText;
                        const svgElement = containerEl.children[0];
                        svgElement.style.cssText="display: inline; width: inherit; min-width: inherit; max-width: inherit; height: inherit; min-height: inherit; max-height: inherit;";
                        svgPanZoom(svgElement, {{
                            zoomEnabled: true,
                            controlIconsEnabled: true,
                            fit: true,
                            center: true
                        }});
                    }}

                    reload();

                </script>
            </body>
        </html>
        """
        self.queue = asyncio.Queue()

        @app.on_event("startup")
        async def startup_event():
            asyncio.create_task(self.watchFile())

        @app.get("/")
        async def get():
            return HTMLResponse(html)

        @app.get("/diagram")
        async def get():
            diagramText = ""
            if not os.path.exists(self.DIAGRAM_OUTPUT_FILE):
                await self.generateSVG()
            with open(self.DIAGRAM_OUTPUT_FILE) as f:
                diagramText = f.read()
            return PlainTextResponse(diagramText)

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.websocket = websocket
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(data)

    async def generateSVG(self):
        # Reload the file
        DIAGRAM_PLANTUML_FILE = re.sub("\.py$", ".pu", self.DIAGRAM_DEFINITION_FILE)
        proc = await asyncio.create_subprocess_shell(
            f"python {self.DIAGRAM_DEFINITION_FILE}"
        )
        await proc.communicate()
        content = await code2dia.generator.generateSVG(DIAGRAM_PLANTUML_FILE)

        with open(self.DIAGRAM_OUTPUT_FILE, "wb") as f:
            f.write(content)

    async def watchFile(self):
        async for changes in awatch(self.DIAGRAM_DEFINITION_FILE):
            for change in changes:
                if change[0] == Change.modified:
                    await self.generateSVG()
                    if self.websocket is not None:
                        await self.websocket.send_text("reload")

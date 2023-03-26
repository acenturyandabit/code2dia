from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, PlainTextResponse
import os
from pathlib import Path
from asyncinotify import Inotify, Mask
import asyncio
import re

DIAGRAM_DEFINITION_FILE = os.environ["DIAGRAM_DEFINITION_FILE"]
DIAGRAM_OUTPUT_FILE = re.sub("\.py$", ".svg", DIAGRAM_DEFINITION_FILE)

app = FastAPI()

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{DIAGRAM_DEFINITION_FILE}</title>
        <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
    </head>
    <body>
        <div id="container" style="width: 800px; height: 500px; border:1px solid black; ">
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
                svgPanZoom(containerEl.children[0], {{
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

queue = asyncio.Queue()


async def watchFile():
    with Inotify() as inotify:
        inotify.add_watch(
            DIAGRAM_DEFINITION_FILE,
            Mask.ACCESS
            | Mask.MODIFY
            | Mask.OPEN
            | Mask.CREATE
            | Mask.DELETE
            | Mask.ATTRIB
            | Mask.CLOSE
            | Mask.MOVE,
        )
        async for event in inotify:
            # Reload the file
            proc = await asyncio.create_subprocess_shell(
                f"python {DIAGRAM_DEFINITION_FILE}"
            )
            await proc.communicate()
            await queue.put("reload")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(watchFile())


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.get("/diagram")
async def get():
    diagramText = ""
    with open(DIAGRAM_OUTPUT_FILE) as f:
        diagramText = f.read()
    return PlainTextResponse(diagramText)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        reload = await queue.get()
        await websocket.send_text(reload)

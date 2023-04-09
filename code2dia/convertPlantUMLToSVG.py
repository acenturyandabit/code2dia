import os
from jsonc_parser.parser import JsoncParser
import requests
from fastapi.responses import PlainTextResponse
import subprocess
from subprocess import PIPE

CONFIG_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/server/config.jsonc"

CONFIG = JsoncParser.parse_file(CONFIG_FILE)


async def convertPlantUMLToSVG(plantuml: str):
    if CONFIG["plantuml"]["executionType"] == "server":
        serverPost = requests.post(
            CONFIG["plantuml"]["serverType"] + "/svg", data=plantuml
        )
        output = serverPost.content
    else:
        # asyncio subprocess does not work on windows
        cmd = ["java","-jar",CONFIG['plantuml']['jarPath'], 
            "-pipe",
            "-svg"
        ]
        process = subprocess.run(cmd,input=plantuml.encode("utf-8"), capture_output=True)
        output = process.stdout.decode("utf-8")
    return output

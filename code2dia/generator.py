import requests
import inspect
import os
import re
import asyncio
from jsonc_parser.parser import JsoncParser


CONFIG_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/server/config.jsonc"
CONFIG=JsoncParser.parse_file(CONFIG_FILE)


def generatePlantUML(diagramString):
    callerAbsPath = os.path.abspath((inspect.stack()[1])[1])
    outputFilePlantUML = re.sub("\.py$", ".pu", callerAbsPath)
    with open(outputFilePlantUML, "w") as f:
        f.write(diagramString)


async def generateSVG(plantUMLPath):
    output = ""
    plantUMLContents = ""
    with open (plantUMLPath) as f:
        plantUMLContents = f.read()
    if CONFIG["plantuml"]["executionType"] == "server":
        serverPost = requests.post(CONFIG["plantuml"]["serverType"]+"/svg", data=plantUMLContents)
        output = serverPost.content
    else:
        proc = await asyncio.create_subprocess_shell(
            f"java -jar {CONFIG['plantuml']['jarPath']} \
                -pipe \
                -svg \
                {plantUMLPath}",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
        )
        output,_ = await proc.communicate(input=plantUMLContents.encode("utf-8"))
    return output
        

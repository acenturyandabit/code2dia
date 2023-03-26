import requests
import inspect
import os
import re

def generateSVG(diagramString):
    callerAbsPath = os.path.abspath((inspect.stack()[0])[1])
    outputFilePlantUML = re.sub("\.py$", ".pu", callerAbsPath)
    outputFileSVG = re.sub("\.py$", ".svg", callerAbsPath)

    with open(outputFilePlantUML, "w") as f:
        f.write(diagramString)

    serverPost = requests.post(f"http://localhost:8944/svg/", data=diagramString)
    with open(outputFileSVG, "wb") as f:
        f.write(serverPost.content)
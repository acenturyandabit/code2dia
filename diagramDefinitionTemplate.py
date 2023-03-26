import re
import requests

OUTPUT_FILE_SVG = re.sub("\.py$", ".svg", __file__)
OUTPUT_FILE_PLANTUML = re.sub("\.py$", ".pu", __file__)


def main():
    diagram_pu = makeDiagram()

    with open(OUTPUT_FILE_PLANTUML, "w") as f:
        f.write(diagram_pu)

    serverPost = requests.post(f"http://localhost:8944/svg/", data=diagram_pu)
    with open(OUTPUT_FILE_SVG, "wb") as f:
        f.write(serverPost.content)


def makeDiagram():
    return """
@startuml main
alice -> bob : no
@enduml
"""


main()

import re
import code2dia


def main():
    # allFiles = code2dia.enumerateFiles()
    diagram = code2dia.plantuml.wrapDiagram(
        "hey -> you"
    )
    code2dia.generator.generatePlantUML(diagram)

main()
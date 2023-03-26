import os
import code2dia


def main():
    srcRoot = os.path.dirname(__file__)
    allFiles = code2dia.symbolCollector.collectSymbols(srcRoot, [".c"])
    diagram = code2dia.plantuml.wrapDiagram(allFiles)
    code2dia.generator.generatePlantUML(diagram)


main()

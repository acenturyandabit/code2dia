from .DiagramDefinition import DiagramDefinition
from .convertPlantUMLToSVG import convertPlantUMLToSVG
from .convertDiagramToPlantUML import convertDiagramToPlantUML
from .repositoryMiner import getFilesAndFolders, getFunctions


async def convertDiagramToSvg(relationsBlob: str):
    # Parse the relationsBlob into objects, relations and stylemap
    relationsBlob = DiagramDefinition.fromString(relationsBlob)
    plantUML = convertDiagramToPlantUML(relationsBlob)
    renderedSVG = await convertPlantUMLToSVG(plantUML)
    return plantUML, renderedSVG


def mineRepository(path: str):
    (fileObjects, fileRelations) = getFilesAndFolders(path)
    (funcObjects, funcRelations) = getFunctions(path, fileObjects, language="C")

    styleMap = DiagramDefinition.fromString("""
file in folder : rcontains
folder in folder : rcontains
function_definition in file: rcontains
function_definition calls function_call: contains
function_call isCallOf function_definition: ..>
"""
    ).styleMap
    return DiagramDefinition(
        [*fileObjects, *funcObjects], 
        [*fileRelations,*funcRelations], 
        styleMap
    )
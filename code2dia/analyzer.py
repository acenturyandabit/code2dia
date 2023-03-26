import code2dia
from typing import List
import os


def enumerateFiles(srcRoot, extensions: List[str]):
    allFiles = gatherAllFiles(srcRoot, extensions)

    tree = buildTreeFrom(allFiles)
    return renderTree(tree)


def gatherAllFiles(srcRoot, extensions):
    allFiles = []
    for root, dirs, files in os.walk(srcRoot):
        subRoot = root[len(srcRoot) :]
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    allFiles.append(subRoot + os.path.sep + file)
                    break
    return allFiles


def buildTreeFrom(allFiles: List[str]):
    root = {"part": "", "fullName": os.path.sep, "children": []}
    for file in allFiles:
        pathParts = file.split(os.path.sep)
        currentNode = root
        for part in pathParts:
            childNames = list(map(lambda i: i["part"], currentNode["children"]))
            if part not in childNames:
                currentNode["children"].append(
                    {
                        "part": part,
                        "fullName": currentNode["fullName"] + os.path.sep + part,
                        "children": [],
                    }
                )
                childNames.append(part)
            folderIdx = childNames.index(part)
            currentNode = currentNode["children"][folderIdx]
    return root


def renderTree(rootNode: dict):
    outputLines = []
    nodeStack = [rootNode]
    while len(nodeStack) > 0:
        topNode = nodeStack.pop()
        if len(topNode["children"]) == 0:
            outputLines.append(cleanedFileIdentifier(topNode["fullName"]))
        else:
            if "nextChildIdx" not in topNode:
                topNode["nextChildIdx"] = 1
                outputLines.append(startFolder(topNode["fullName"]))
                nodeStack.append(topNode)
                nodeStack.append(topNode["children"][0])
            elif topNode["nextChildIdx"] == len(topNode["children"]):
                outputLines.append("}")
            else:
                nodeStack.append(topNode)
                nodeStack.append(topNode["children"][topNode["nextChildIdx"]])
                topNode["nextChildIdx"] += 1
    return "\n".join(outputLines)


def cleanedFileIdentifier(path):
    cleanPath = code2dia.plantuml.cleanName(path)
    return f'file "{removeBackslashes(path)}" as {cleanPath}'


def startFolder(path):
    cleanPath = code2dia.plantuml.cleanName(path)
    return f'folder "{removeBackslashes(path)}" as {cleanPath} {{'


def removeBackslashes(path):
    return path.replace(os.path.sep, "/")

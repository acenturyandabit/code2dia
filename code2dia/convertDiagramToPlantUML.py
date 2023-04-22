from .DiagramDefinition import DiagramDefinition
import re
import json

def convertDiagramToPlantUML(diagram: DiagramDefinition):
    relationTypes = extractRelationTypesAsDictionary(diagram.styleMap)
    (inflatedRelations, objectTypeDictionary) = inflateRelationsAndExtractObjects(diagram.objects, diagram.relations)
    (nonContainingRelationList, componentParentTree) = buildRelationsAndHierarchy(objectTypeDictionary, inflatedRelations, relationTypes)
    componentChildrenTree = createChildTreeFrom(componentParentTree, objectTypeDictionary)
    
    plantUMLLines = [
        "@startuml main", 
        "left to right direction",
        *generateComponentDefinitionPlantUMLLines(componentChildrenTree),
        *nonContainingRelationList, # This could be taken out into its own function for better design
        "@enduml"
    ]
    return "\n".join(plantUMLLines)

def extractRelationTypesAsDictionary(stylemap):
    relationTypes={}
    for style in stylemap:
        relationType = style['clause']['type']
        if relationType not in relationTypes:
            relationTypes[relationType] = []
        relationTypes[relationType].append(style)
    return relationTypes

def inflateRelationsAndExtractObjects(objects, relations):
    objectTypeDictionary = {}
    for object in objects:
        objectTypeDictionary[plantUMLCleanName(object['name'])] = object['type']
    
    inflatedRelations = []
    for relation in relations:
        _from = plantUMLCleanName(relation['from'])
        _to = plantUMLCleanName(relation['to'])

        if _from not in objectTypeDictionary:
            objectTypeDictionary[_from]='unknown'
        if _to not in objectTypeDictionary:
            objectTypeDictionary[_to]='unknown'
        
        inflatedRelations.append({
            'typeA':objectTypeDictionary[_from],
            'typeB':objectTypeDictionary[_to],
            'relationType': relation['type'],
            'from': _from,
            'to': _to
        })

    return inflatedRelations, objectTypeDictionary

def buildRelationsAndHierarchy(objectTypeDictionary, inflatedRelations, relationTypes):
    nonContainingRelationList=[]
    componentParentTree = {objectName: objectName for objectName in objectTypeDictionary}
    for relation in  inflatedRelations:
        relationType = relation['relationType']
        relationStyleType="..>:"+relationType
        WILDCARD_SPECIFICITY=1
        TYPEMATCH_SPECIFICITY=2
        if relationType in relationTypes:
            relationStyleMatchSpecificity = WILDCARD_SPECIFICITY*2-1
            for style in relationTypes[relationType]:
                currentMatchSpecificity = WILDCARD_SPECIFICITY*2-1
                if style['clause']['from'] == "*":
                    currentMatchSpecificity += WILDCARD_SPECIFICITY
                if style['clause']['to'] == "*":
                    currentMatchSpecificity += WILDCARD_SPECIFICITY
                if style['clause']['to'] == relation['typeB']:
                    currentMatchSpecificity += TYPEMATCH_SPECIFICITY
                if style['clause']['from'] == relation['typeA']:
                    currentMatchSpecificity += TYPEMATCH_SPECIFICITY
                if currentMatchSpecificity > relationStyleMatchSpecificity:
                    relationStyleType = style['style']
                    relationStyleMatchSpecificity = currentMatchSpecificity

        if relationStyleType == 'contains':
            componentParentTree[relation['to']]=relation['from']
        elif relationStyleType == 'rcontains':
            componentParentTree[relation['from']]=relation['to']
        else: 
            if ":" in relationStyleType:
                [relationArrow, relationPostfix] = relationStyleType.split(":")
                relationString = f"{relation['from']} {relationArrow} {relation['to']} : {relationPostfix}"
            else:
                relationString = f"{relation['from']} {relationStyleType} {relation['to']}"
            nonContainingRelationList.append(relationString)

    return nonContainingRelationList, componentParentTree

def createChildTreeFrom(componentParentTree,objectTypeDictionary):
    componentChildrenTree = {objectName:{"children": [], "isRoot": (objectName == componentParentTree[objectName])} 
                             for  objectName in objectTypeDictionary}
    for nodeName in componentParentTree:
        parent = componentParentTree[nodeName]
        if parent != nodeName:
            componentChildrenTree[parent]['children'].append(nodeName)
    return componentChildrenTree

def generateComponentDefinitionPlantUMLLines(componentChildrenTree):
    componentDefinitionPlantUMLLines = []
    renderStack = []
    for component in componentChildrenTree:
        if componentChildrenTree[component]['isRoot']==True:
            renderStack.append(component)
    
    currentIndentation = 0
    while len(renderStack)>0:
        top = renderStack.pop()
        if top=="}":
            currentIndentation -= 2
            componentDefinitionPlantUMLLines.append((" " * currentIndentation) + "}")
        else:
            componentDefinitionPlantUMLLines.append((" " * currentIndentation) + "rectangle " + top + " {")
            renderStack.append("}")
            for child in componentChildrenTree[top]['children']:
                renderStack.append(child)
    return componentDefinitionPlantUMLLines

def plantUMLCleanName(name: str):
    cleanName = re.sub('\W', '_', name)
    return cleanName

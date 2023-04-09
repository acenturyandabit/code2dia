from .DiagramDefinition import DiagramDefinition
import re
import json

def convertDiagramToPlantUML(diagram: DiagramDefinition):
    # Extract containment styles because rendering of object
    # containment happens at object render time
    relationTypes = {}
    for style in diagram.styleMap:
        relationType = style['clause']['type']
        if relationType not in relationTypes:
            relationTypes[relationType] = []
        relationTypes[relationType].append(style)

    # inflate relations with type information
    (inflatedRelations, objectTypeDictionary) = inflateRelationsAndExtractObjects(diagram.objects, diagram.relations)

    # Turn all relevant relations into a parent-tree, and non-containing
    # relations into lines in the relation list
    nonContainingRelationList = []
    # print (inflatedRelations)
    componentParentTree = {objectName: objectName for objectName in objectTypeDictionary}
    for relation in  inflatedRelations:
        relationStyleType=None
        relationType = relation['relationType']
        if relationType in relationTypes:
            for style in relationTypes[relationType]:
                if style['clause']['from'] == relation['typeA'] and \
                    style['clause']['to'] == relation['typeB']:
                    relationStyleType = style['style']
        if relationStyleType is None:
            # raise Exception("Bad relation" + json.dumps(relation))
            relationStyleType = "..>"
        if relationStyleType == 'contains':
            componentParentTree[relation['to']]=relation['from']
        elif relationStyleType == 'rcontains':
            componentParentTree[relation['from']]=relation['to']
        else: 
            nonContainingRelationList.append(f"{relation['from']} {relationStyleType} {relation['to']}")
    # print (componentParentTree)

    # render a component for every object
    plantUMLLines = ["@startuml main", "left to right direction"]
    componentChildrenTree = {objectName:{"children": [], "isRoot": (objectName == componentParentTree[objectName])} 
                             for  objectName in objectTypeDictionary}
    for nodeName in componentParentTree:
        parent = componentParentTree[nodeName]
        if parent != nodeName:
            componentChildrenTree[parent]['children'].append(nodeName)
    # print (componentChildrenTree)
    
    # Convert to plantUML component tree
    renderStack = []
    for component in componentChildrenTree:
        if componentChildrenTree[component]['isRoot']==True:
            renderStack.append(component)
    
    currentIndentation = 0
    while len(renderStack)>0:
        top = renderStack.pop()
        if top=="}":
            currentIndentation -= 2
            plantUMLLines.append((" " * currentIndentation) + "}")
        else:
            plantUMLLines.append((" " * currentIndentation) + "rectangle " + top + " {")
            renderStack.append("}")
            for child in componentChildrenTree[top]['children']:
                renderStack.append(child)

    plantUMLLines += nonContainingRelationList
    plantUMLLines.append("@enduml")
    # print ("\n".join(plantUMLLines))
    return "\n".join(plantUMLLines)

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

def plantUMLCleanName(name: str):
    cleanName = re.sub('\W', '_', name)
    return cleanName

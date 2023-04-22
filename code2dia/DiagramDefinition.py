from typing import List

class DiagramSyntaxError(Exception):
    pass

class DiagramDefinition(dict):
    objects: List
    relations: List
    styleMap: List

    def __init__(self, objects=[], relations=[], styleMap=[]):
        self.objects=objects
        self.relations=relations
        self.styleMap=styleMap
        pass

    def __str__(self):
        stringList = []
        separatorForNewline = ""
        
        for object in self.objects:
            stringList.append(f"{object['type']} {object['name']}")
        stringList.append(separatorForNewline)

        for relation in self.relations:
            stringList.append(f"{relation['from']} {relation['type']} {relation['to']}")
        stringList.append(separatorForNewline)

        for style in self.styleMap:
            if style['type']=='object':
                clause = f"{style['clause']['type']} {style['clause']['name']}"
            elif style['type']=='relation':
                clause = f"{style['clause']['from']} {style['clause']['type']} {style['clause']['to']}"
            stringList.append(f"{clause} : {style['style']}")
        stringList.append(separatorForNewline)

        return "\n".join(stringList)

    @staticmethod
    def fromString(blob: str) -> "DiagramDefinition":
        objects = []
        relations = []
        styleMap = []

        blobLines = map(lambda l: l.strip(), blob.split("\n"))
        for li, line in enumerate(blobLines):
            try:
                if ":" in line:
                    styleStringParts = list(map(lambda l: l.strip(), line.split(":")))
                    clauseString = styleStringParts[0]
                    style = ":".join(styleStringParts[1:])
                    (clauseType, clause) = DiagramDefinition.objectOrRelation(clauseString)
                    styleMap.append({
                        "type": clauseType, 
                        "clause": clause,
                        "style": style 
                    })
                else:
                    clausePair = DiagramDefinition.objectOrRelation(line)
                    if clausePair is not None:
                        (clauseType, clause) = clausePair
                        if clauseType == "object":
                            objects.append(clause)
                        elif clauseType == "relation":
                            relations.append(clause)
            except Exception as e:
                raise DiagramSyntaxError(f"Error on line {li}: {line}: {e}")
        return DiagramDefinition(objects, relations, styleMap)


    @staticmethod
    def objectOrRelation(line: str):
        lineParts = line.split(" ")
        if len(lineParts) == 2:
            return ("object", {
                "type": lineParts[0],
                "name": lineParts[1],
            })
        elif len(lineParts) == 3:
            return ("relation", {
                "type": lineParts[1],
                "from": lineParts[0],
                "to": lineParts[2]
            })
        elif line == "":
            return None
        else:
            raise DiagramSyntaxError(f"Non-empty line '{line}' with neither object nor relation")

    # JSON serializability 
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, value):
        self[key] = value

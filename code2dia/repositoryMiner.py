import re
import os

# HEURISTIC: extensions
def getFilesAndFolders(path: str, extensions = [".cpp","c"]):
    objects = [{
        "type":"folder",
        "name": "root"
    }]
    relations = []
    for root, dirs, files in os.walk(path):
        subRoot = "root"+root[len(path) :]
        # HEURISTIC: ignore .git
        if ".git" in subRoot:
            continue
        for dir in dirs:
            fullFolderName = subRoot + os.path.sep + dir
            objects.append({
                "type":"folder",
                "name": fullFolderName
            })
            relations.append({
                "type": "in",
                "from": fullFolderName,
                "to": subRoot
            })
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    fullFileName = subRoot + os.path.sep + file
                    objects.append({
                        "type":"file",
                        "name": fullFileName
                    })
                    relations.append({
                        "type": "in",
                        "from": fullFileName,
                        "to": subRoot
                    })
    return objects, relations

def getFunctions(path, fileObjects, language):
    objects = [{
        "type":"function_definition",
        "name": "global"
    }]
    relations = []

    files = filter(lambda obj: obj["type"]=="file", fileObjects)
    # Read each file
    for file in files:
        objects, relations = mineFile(path, file["name"], objects, relations)
    return objects, relations

def mineFile(basePath, filename, objects, relations):
    with open (basePath + filename[len("root"):]) as f:
        context = []
        c = " "
        objects.append({
                        "type": "function_definition",
                        "name": filename+"_main"
                    })
        relations.append({
                        "type": "in",
                        "from": filename+"_main",
                        "to": filename
                    })
        while c:
            c = f.read(1)
            context, objects, relations = stateReduceCharacter(context, objects, relations, filename, c)
    return objects, relations

# TODO: reduce number of arguments of this function
def stateReduceCharacter(context, objects, relations, filename, c):
    try:
        if re.match("[a-zA-Z0-9_-]",c):
            if len(context) == 0:
                context.append("")
            context[len(context)-1] += c
        else:
            if c == "(":
                if len (context) > 0  and context[-1] == "":
                    # dirty hack - this check should be applied more broadly
                    context[-1] = c
                else:
                    context.append(c)
                context.append("")
            elif c == ")":
                # print ("pre")
                # print (context)
                context = removeAfterHighestIndexOf("(", context)
                if len (context) > 0  and context[-1] == "if" or context[-1] == "while":
                    context = context[:-1]
                elif isIdentifier(context[-1]):
                    # This is either a function call or a function declaration, depending on 
                    # whether we see a ; or a { next
                    # So flag it as a function candidate
                    context[-1] = "fn_candidate:" + context[-1]
                    # print (context)

            elif c == "{":
                if len (context) > 0  and context[-1] == "" and len(context) > 1:
                    context = context[:-1]
                # upgrade previous fn candidate to real function
                if context[-1].startswith("fn_candidate:"):
                    # print (context)
                    functionName = context[-1][len("fn_candidate:"):]
                    context[-1] = "fn_definition:" + functionName
                    # print (functionName)
                    objects.append({
                        "type": "function_definition",
                        "name": functionName
                    })
                    relations.append({
                        "type": "in",
                        "from": functionName,
                        "to": filename
                    })
                else:
                    # print ("NOT A GOOD FN")
                    # print (context)
                    pass
                if len (context) > 0  and context[-1] == "":
                    # dirty hack - this check should be applied more broadly
                    context[-1] = c
                else:
                    context.append(c)
                context.append("")
            elif c == "}":
                context = removeAfterHighestIndexOf("{", context)
                while len(context) > 0 and (\
                        context[-1] in C_RESERVED_WORDS or \
                        re.match("fn_.+?:",context[-1])):
                    # while loop also removes function type specifiers
                    context = context[:-1]
            elif c == "[":
                if len (context) > 0  and context[-1] == "":
                    # dirty hack - this check should be applied more broadly
                    context[-1] = c
                else:
                    context.append(c)
                context.append("")
            elif c == "]":
                context = removeAfterHighestIndexOf("[", context)
            elif c  == "'":
                # TODO: Make escaping strings actually useful
                if context.count("'") % 2 == 1:
                    context = removeAfterHighestIndexOf("'", context)
                else: 
                    context.append("'")
            elif c  == '"':
                # TODO: Make escaping strings actually useful
                if context.count('"') % 2 == 1:
                    context = removeAfterHighestIndexOf('"', context)
                else: 
                    context.append('"')
            elif c == ";":
                if len (context) > 0  and context[-1].startswith("fn_candidate:"):
                    functionName = context[-1][len("fn_candidate:"):]
                    context[-1] = "fn_call:" + functionName
                    callerName = filename+"_main"
                    # search up stack because we may be in an if-statement
                    for ctx in context:
                        if ctx.startswith("fn_definition:"):
                            callerName = ctx[len("fn_definition:"):]
                            break
                    fullCallName = callerName + "_call_" + functionName
                    objects.append({
                        "type": "function_call",
                        "name": fullCallName
                    })
                    relations.append({
                        "type": "calls",
                        "from": callerName,
                        "to": fullCallName
                    })
                    # relations.append({
                    #     "type": "isCallOf",
                    #     "from": fullCallName,
                    #     "to": functionName
                    # })
                    # TODO: Temporal context; callsAfter
                context = trimSemicolon(context)
            elif c == "/":
                if len (context) > 0  and context[-1] == "":
                    # dirty hack - this check should be applied more broadly
                    context[-1] = c
                else:
                    context.append(c)
                if len(context) > 0 and context[-1] == "/":
                    context[-1] = "//"
                else:
                    context.append("/")
            elif c in ["+","-","*", "&", "|", "!", "<" , ">", "?", "="]:
                # Operators get a free pass
                if len (context) > 0  and context[-1] == "":
                    # dirty hack - this check should be applied more broadly
                    context[-1] = c
                else:
                    context.append(c)
                context.append("")
            elif str.isspace(c):
                # TODO: clean up len(context) == 0 chekcs.
                if c == "\r" or c == "\n":
                    # pop off any line comments and any processor directives
                    context = removeAfterLowestIndexOf("//", context)
                    context = removeAfterLowestIndexOf("#", context)
                if len(context) == 0:
                    context.append("")
                if context[-1]!= "":
                    context.append("")
    except IndexError as e:
        # print (context)
        raise e
    return context, objects, relations

def removeAfterLowestIndexOf(item, context):
    slicePoint = -1
    for i,ctx in enumerate(context):
        if ctx == item:
            slicePoint = i
            break
    if slicePoint > -1:
        context = context [0:slicePoint]
    if len(context) == 0:
        context.append("")
    return context

def removeAfterHighestIndexOf(item, context):
    # # print (f"sliced for {item} from ")
    # # print (context)
    slicePoint = -1
    for i in range (len(context)-1, 0,-1):
        if context[i] == item:
            slicePoint = i
            break
    if slicePoint > -1:
        context = context [0:slicePoint]
    if len(context) == 0:
        context.append("")
    # # print ("to")
    # # print (context)
    return context

C_RESERVED_WORDS = [
    "auto",
    "_Packed",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "int",
    "long",
    "register",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while"
]

def isIdentifier(identifier: str):
    return re.match("^\w[\w\d]+$", identifier) is not None and \
        identifier not in C_RESERVED_WORDS

def trimSemicolon(context):
    slicePoint = 0 # willing to delete everything
    if len(context)>0:
        for i in range (len(context)-1, 0, -1):
            if context[i] == "{":
                slicePoint = i
                break
        context = context [0:slicePoint]
        if len(context) == 0:
            context.append("")
    return context
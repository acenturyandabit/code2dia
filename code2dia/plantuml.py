import re


def wrapDiagram(*args):
    wrappedOutput = "@startuml main\n"
    for arg in args:
        if type(arg) == str:
            wrappedOutput += arg + "\n"
    wrappedOutput += "@enduml"
    return wrappedOutput

def cleanName(name):
    return re.sub("\W","_",name)

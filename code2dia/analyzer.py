import code2dia
def listFiles():
    allFiles = ["test.cpp", "/to/another/test.cpp"]
    "\n".join(map (code2dia.plantuml.cleanName, allFiles))
    return outputText
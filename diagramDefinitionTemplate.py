import re

DIAGRAM_OUTPUT_FILE = re.sub("\.py$", ".svg", __file__)
with open(DIAGRAM_OUTPUT_FILE, "w") as f:
    f.write("hello world!")

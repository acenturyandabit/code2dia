# code 2 dia
A library of tools to help create diagrams of code manually or automatically, to help with understanding.

## Usage
Assumptions
- You have miniconda installed
- You have a codebase ready that you want to explore

Procedure
1. copy the `diagramDefinitionTemplate.py` to your codebase root
2. run `serveDiagram path/to/codebase/diagramDefinitionTemplate.py`.
2. run `uvicorn serveDiagram:app`
3. open the link in the browser
4. make changes to dia-template.py, it will automatically update in the browser


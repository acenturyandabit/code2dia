# code 2 dia
A library of tools to help create diagrams of code manually or automatically, to help with understanding.

## Usage
Assumptions
- You have miniconda installed
    - https://docs.conda.io/en/latest/miniconda.html
- You have added the conda-forge channel
    - https://conda-forge.org/
    - `conda config --add channels conda-forge`
- You have a codebase ready that you want to explore
- You have plantuml installed, or have access to a (dockerized or not) plantUML server
    - See server/config.template.json.
### Installation
1. `conda create -n code2dia fastapi uvicorn websockets watchfiles conda-build black`
    - Using this instead of a requirements.txt or a list file or a meta yaml file because I like keeping deps reasonably up to date. 
    - You may have to reinstall conda-build afterwards? not sure why but eh
2. Also install some stuff that isn't in conda yet: `pip install jsonc-parser`
2. `conda develop .` so that your python interpreter can find the libraries from this project.
    - If for some reason conda develop doesn't work: `pip install --editable .`
3. Copy `server/config.template.jsonc` into `server/config.jsonc` and update values as necessary.
3. copy the `diagramDefinitionTemplate.py` to your codebase root as `diagramDefinition.py`
4. run `python serveDiagram.py path/to/codebase/diagramDefinition.py`.
5. open the link in the browser
6. make changes to dia-template.py, it will automatically update in the browser

## Automation capability
- Detect every file with a given extension in the directory
- Detect entities within those files, in C++

## Todo
- End to end memory buffer / pipe, so that there are no stray .pu or .svg files created
- Viewer improvement: no need to zoom back in when the diagram changes
- Refactoring: Move http into a file
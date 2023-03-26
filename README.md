# code 2 dia
A library of tools to help create diagrams of code manually or automatically, to help with understanding.

## Inspiration
- PlantUML
    - Creating component diagrams from text is awesome. PlantUML is the backend to code2dia.
- rqt_graph
    - Shows nodes and topics in a very clean, practical way. Awesome tool.
- https://www.gituml.com/
    - An attempt to create UML diagrams from code. However, it does not have nesting like plantUML has, which is a key capability I aim to exploit in this project.

## Concepts
- At the most abstract level, a codebase is made up of a bunch of 'objects'.
    - Objects include files, folders, classes, functions, variables.
    - Objects can be represented using different symbols e.g. File = fileshape, class = Rectangle
- These objects are related to each other in a bunch of different ways. Given two objects A and B, relations include:
    - folder A contains file B
    - file A declares class B
    - file A declares method B
    - method A calls method B
    - method A isCalledAfter method B in method C
    - classInstance A isInstanceOf classPrototype B
- There are multiple ways of representing these relations, including:
    - A pointsTo B (with linestyle S)
    - A contains B
    - A sharesStyleAttribute S {e.g. thickness} with  B
- By mapping object relations to representations, we can create very versatile diagrams. For example:
    - An execution diagram where (A calls B) == (A contains B) and (B isCalledAfter A) == (A pointsTo B)

We can read the code to determine the objects and relations between them. A user can alter the relation/representation mapping to create diagrams which are useful to them.

Note: This is the long term goal. Currently this repo is just set up to show that plantUML and websockets can be used pragmatically to create a programmatic code scraping diagram generator.

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

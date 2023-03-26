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
- You have a plantuml docker container running on `localhost:8944`:
    - `docker run -p8944:8000 plantuml/plantuml-server:jetty`

# Usage
1. `conda create -n code2dia fastapi uvicorn websockets asyncinotify conda-build black`
    - Using this instead of a requirements.txt or a list file or a meta yaml file because I like keeping deps reasonably up to date. 
    - You may have to reinstall conda-build afterwards? not sure why but eh
2. `conda develop .` so that your python interpreter can find the libraries from this project.
3. copy the `diagramDefinitionTemplate.py` to your codebase root
4. run `python serveDiagram.py path/to/codebase/diagramDefinitionTemplate.py`.
5. run `uvicorn serveDiagram:app`
6. open the link in the browser
7. make changes to dia-template.py, it will automatically update in the browser


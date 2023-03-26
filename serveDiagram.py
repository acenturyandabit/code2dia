import click
import os
from server.main import Server
import uvicorn

@click.command()
@click.argument("defpath")
def main(defpath):
    s=Server(os.path.abspath(defpath))
    uvicorn.run(s.app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
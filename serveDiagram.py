import click
import subprocess
import os


@click.command()
@click.argument("defpath")
def main(defpath):
    innerEnv = {**os.environ, "DIAGRAM_DEFINITION_FILE": os.path.abspath(defpath)}
    subprocess.Popen(["uvicorn", "main:app"], env=innerEnv, cwd="server")


if __name__ == "__main__":
    main()

import click
import os


@click.command()
@click.argument("defpath")
def main(defpath):
    innerEnv = {**os.environ, "DIAGRAM_DEFINITION_FILE": os.path.abspath(defpath)}
    os.chdir("server")
    os.execlpe("uvicorn", "uvicorn", "main:app", innerEnv)


if __name__ == "__main__":
    main()

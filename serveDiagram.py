import click
import os


@click.command()
@click.argument("repository_path")
def main(repository_path):
    click.launch('http://localhost:8000')
    os.execlpe("uvicorn", 
               *("uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload".split(" ")),
               {
                **os.environ,
                "WATCH_REPOSITORY_PATH": repository_path
               })

if __name__ == "__main__":
    main()

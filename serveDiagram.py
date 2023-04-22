import click
import os


@click.command()
def main():
    click.launch('http://localhost:3429')
    os.execlpe("uvicorn", 
               *("uvicorn server.main:app --host 127.0.0.1 --port 5973 --reload".split(" ")),
               {
                **os.environ
               })

if __name__ == "__main__":
    main()

import click
import code2dia


@click.command()
@click.option("--path")
def main(path):
    diagram = code2dia.mineRepository(path)
    
    print (diagram)

if __name__ == "__main__":
    main()

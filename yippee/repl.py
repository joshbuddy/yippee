import click
from yippee.config import Config
from yippee.generator import Generator


@click.command()
@click.argument("file", type=click.Path(exists=True), default="yippee.py")
@click.version_option()
def run(file):
    config = Config(file)
    print(config.state)
    Generator(config).generate()


if __name__ == "__main__":
    run()

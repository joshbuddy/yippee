import os
import click
from yippee.config import Config
from yippee.generator import Generator


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(generate)


@cli.command(short_help="generate requirements.txt files")
@click.option("--file", type=click.Path(exists=True), default="yippee.py")
def generate(file):
    config = Config(file)
    files = Generator(config).generate()
    line = ", ".join(list(map(lambda f: "\033[1m%s\033[0m" % f, files)))
    print("\nFinished generating %s" % line)


@cli.command(short_help="initialize a configuration file")
@click.option("--force/--no-force", default=False)
@click.option("--file", type=click.Path(), default="yippee.py")
def init(force, file):
    if os.path.isfile(file) and not force:
        raise Exception(
            "cannot init, %(file)s is in the way, and not forcing" % {"file": file}
        )
    with open(file, "w") as fh:
        fh.write(
            """from yippee import group, pip

# pip("click", "~=7.0")

# with group("development"):
#    pip("twine", "~=1.12.0")
#    pip("black", "18.9b0")
#    pip("wheel")
"""
        )

    print("Initiated yippee at \033[1m%(file)s\033[0m" % {"file": file})


if __name__ == "__main__":
    cli()

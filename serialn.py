import click
from pathlib import Path

@click.command()
def hi():
    click.echo("hi")

@click.command()
def show_recipes():
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists():
        click.echo("yup its there")
    else:
        Path.mkdir(recipefolder)
        click.echo("folder mkdired")
    click.echo()
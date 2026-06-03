import click
from pathlib import Path

@click.command()
def hi():
    click.echo("hi")

@click.command()
def show_recipes():
    recipefolder = Path.home() / "recipes"
    recipeindexpath = recipefolder / "recipeindex.txt"

    if recipefolder.exists():
        click.echo("yup the recipes folder is there")
    else:
        Path.mkdir(recipefolder)
        click.echo("recipes folder mkdired")

    if recipeindexpath.exists():
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "r+")
        click.echo("can confirm the recipeindex file is there")
    else:
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "x")
        click.echo("recipeindex file has been created")

    recipeindex.close()
    recipeindex = open(f"{recipefolder}/recipeindex.txt", "a")

    recipeindex.write("hello")
    recipeindex.close()

    click.echo()
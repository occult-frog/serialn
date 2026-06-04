from idlelib import filelist

import click
from pathlib import Path

@click.command()
def hi():
    click.echo("hi")

@click.command()
def list_recipes():
    recipefolder = Path.home() / "recipes"
    recipeindexpath = recipefolder / "recipeindex.txt"

    if recipefolder.exists():
        click.echo("yup the recipes folder is there :D")
    else:
        Path.mkdir(recipefolder)
        click.echo("recipes folder mkdired :P")

    if recipeindexpath.exists():
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "r+")
        click.echo("can confirm the recipeindex file is there :P\n")
    else:
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "x")
        click.echo("recipeindex file has been created :)\n")

    recipeindex.close()
    recipeindex = open(f"{recipefolder}/recipeindex.txt", "r")
    templist = recipeindex.readlines()
    filelist = []

    for i in templist:
        filelist.append(i.strip())

    for i in filelist:
        if (recipefolder/i).exists():
            click.echo(f"{i}: found :)")
        else:
            click.echo(f"{i}: not found :(")

    recipeindex.close()


@click.command()
@click.argument('recipename')
def view_recipe(recipename):
    recipefolder = Path.home()/"recipes"

    if recipefolder.exists() and (recipefolder/"recipeindex.txt").exists():
        if (recipefolder/recipename).exists():
            recipefile = open(recipefolder/recipename, "r")
            click.echo(recipefile.read())
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"show_recipes\" to create them")


@click.command()
@click.option('--remove_absent', 'remove_absent', help="remove recipes from the recipe index that aren't in the recipe folder")
def refresh_recipes(remove_absent):
    recipefolder = Path.home()/"recipes"
    if recipefolder.exists() and (recipefolder/"recipeindex.txt").exists():
        if remove_absent == "":
            recipeindex = open(f"{recipefolder}/recipeidex.txt", "r+")
            templist = recipeindex.readlines()
            filelist = []
            for i in templist:
                filelist.append(i.strip())
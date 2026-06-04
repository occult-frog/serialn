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

    click.echo("recipes:")

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
def refresh_recipes():
    recipefolder = Path.home()/"recipes"
    if recipefolder.exists() and (recipefolder/"recipeindex.txt").exists():
        filesinfolder = []
        alltxtfiles = list(recipefolder.glob("*.txt"))
        for i in alltxtfiles:
            filesinfolder.append((str(i)).removeprefix(f"{recipefolder}/"))
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "w+")
        for i in filesinfolder:
            if i != "recipeindex.txt":
                recipeindex.write(f"{i}\n")
        click.echo("recipes:")
        recipeindex.close()
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "r")
        templist = recipeindex.readlines()
        filelist = []
        for i in templist:
            filelist.append(i.strip())
        click.echo("recipes:")
        for i in filelist:
            click.echo(i)
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"show_recipes\" to create them")
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
        click.echo("recipes folder mkdired :)")

    if recipeindexpath.exists():
        recipeindex = open(f"{recipefolder}/recipeindex.txt", "r+")
        click.echo("can confirm the recipeindex file is there :D\n")
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
@click.argument('recipename', required=True)
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


@click.command()
@click.argument("recipename", required=True)
def add_recipe(recipename):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.txt").exists():
        if (recipefolder/recipename).exists():
            click.echo(f"recipe with the name {recipename} already exists :P")
        else:
            ingredientcount = int(input("how many ingredients are there?: "))
            stepcount = int(input("how many steps are there?: "))
            ingredients = []
            steps = []
            extranotes = []

            for i in range(ingredientcount):
                if i+1 == 1: ordinalsuffix = "st"
                elif i+1 == 2: ordinalsuffix = "nd"
                elif i+1 == 3: ordinalsuffix = "rd"
                else: ordinalsuffix = "th"
                j = "N"
                ing = input(f"enter name of {i+1}{ordinalsuffix} ingredient: ")
                while j != "y":
                    k = input(f"confirm ingredient? (y/N): ")
                    if k == "y": j = k
                    else: ing = input(f"enter name of {i + 1}{ordinalsuffix} ingredient: ")
                ingredients.append(f"{ing}\n")

            for i in range(stepcount):
                if i+1 == 1: ordinalsuffix = "st"
                elif i+1 == 2: ordinalsuffix = "nd"
                elif i+1 == 3: ordinalsuffix = "rd"
                else: ordinalsuffix = "th"
                j = "N"
                step = input(f"enter {i+1}{ordinalsuffix} step: ")
                while j != "y":
                    k = input(f"confirm step? (y/N): ")
                    if k == "y": j = k
                    else: step = input(f"enter {i+1}{ordinalsuffix} step: ")
                steps.append(f"{step}\n")

            j = "N"
            extranotesquestion = input("do you want to add any extra notes? (y/N): ")
            if extranotesquestion == "y":
                i = 0
                while j != "stop":
                    i += 1
                    if i == 1: ordinalsuffix = "st"
                    elif i == 2: ordinalsuffix = "nd"
                    elif i == 3: ordinalsuffix = "rd"
                    else: ordinalsuffix = "th"
                    note = input(f"enter {i}{ordinalsuffix} note: ")
                    k = "N"
                    while k != "y":
                        l = input(f"confirm note? (y/N): ")
                        if l == "y":
                            k = l
                        else:
                            note = input(f"enter {i}{ordinalsuffix} note: ")
                    m = input("add another note? (y/N): ")
                    if m == "N":
                        j = "stop"
                    extranotes.append(f"{note}\n")

            click.echo("\n")
            recipe = "Ingredients:\n"
            for i in range(len(ingredients)):
                recipe += "".join(f"{i + 1}. {ingredients[i]}")
            recipe += "".join("\nSteps:\n")
            for i in range(len(steps)):
                recipe += "".join(f"{i+1}. {steps[i]}")
            if extranotesquestion == "y":
                recipe += "".join("\nExtra notes:\n")
                for i in range(len(extranotes)):
                    recipe += "".join(f"{i + 1}. {extranotes[i]}")
            click.echo(recipe)

            confirmrecipe = input("confirm recipe? (y/N): ")
            if confirmrecipe == "y":
                recipefile = open(f"{recipefolder}/{recipename}.txt", "w")
                recipefile.write(recipe)
                recipefile.close()
                click.echo("recipe saved :)")
                recipeindex = open(f"{recipefolder}/recipeindex.txt", "a+")
                recipeindex.write(f"\n{recipename}.txt")

    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"show_recipes\" to create them")
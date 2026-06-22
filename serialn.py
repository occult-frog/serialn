import csv
from pathlib import Path
import click


@click.command()
def hi():
    click.echo("hello")


@click.command()
def list_recipes():
    recipefolder = Path.home() / "recipes"
    recipeindexpath = recipefolder / "recipeindex.csv"

    if recipefolder.exists():
        click.echo("yup the recipes folder is there :D")
    else:
        Path.mkdir(recipefolder)
        click.echo("recipes folder mkdired :)")

    if recipeindexpath.exists():
        recipeindex = open(f"{recipefolder}/recipeindex.csv", "r+")
        click.echo("can confirm the recipeindex file is there :D\n")
    else:
        recipeindex = open(f"{recipefolder}/recipeindex.csv", "x")
        click.echo("recipeindex file has been created :)\n")

    recipeindex.close()
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    filelist = list(csv.reader(recipeindex))

    click.echo("recipes:")

    for i in filelist:
        if (recipefolder/i[0]).exists():
            click.echo(f"{i[0]} ---- {i[1]}: found :)")
        else:
            click.echo(f"{i[0]} ---- {i[1]}: not found :(")

    recipeindex.close()


@click.command()
@click.argument('recipename', required=False, default=None)
def view_recipe(recipename):
    recipefolder = Path.home()/"recipes"

    if recipefolder.exists() and (recipefolder/"recipeindex.csv").exists():
        if recipename is None:
            recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
            filelist = list(csv.reader(recipeindex))
            recipeindex.close()
            click.echo("recipes:")
            for i in filelist:
                if (recipefolder / i[0]).exists():
                    j = filelist.index(i)
                    click.echo(f"{i[0]} ---- {i[1]} ---- {j}")
            q = int(input("choose recipe: "))
            if q <= len(filelist):
                recipefile = open(f"{recipefolder}/{filelist[q][0]}", "r")
                click.echo(recipefile.read())
                recipefile.close()
        elif checkRecipeExistence(recipename):
            recipefile = open(recipefolder/f"{recipename}.txt", "r")
            click.echo(recipefile.read())
            recipefile.close()
        else:
            click.echo(f"recipe with the name {recipename} doesnt exist in the recipe index :P\n"
                       f"try typing the recipe name without the .txt extension or running \"refresh_recipes\"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list_recipes\" to create them")


@click.command()
def refresh_recipes():
    recipefolder = Path.home()/"recipes"
    if recipefolder.exists() and (recipefolder/"recipeindex.csv").exists():
        refreshIndex(recipefolder)
        recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
        filelist = list(csv.reader(recipeindex))
        click.echo("recipes:")
        for i in filelist:
            click.echo(f"{i[0]} ----- {i[1]}")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list_recipes\" to create them")


@click.command()
@click.argument("recipename", required=True)
def add_recipe(recipename):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if (recipefolder/f"{recipename}.csv").exists():
            click.echo(f"recipe with the name {recipename} already exists :P")
        else:
            ingredientcount = int(input("how many ingredients are there?: "))
            stepcount = int(input("how many steps are there?: "))
            ingredients = []
            steps = []
            extranotes = []
            tags = ""

            for i in range(ingredientcount):
                ordinalsuffix = ordinalNumber(i+1)
                j = "N"
                ing = input(f"enter name of {i+1}{ordinalsuffix} ingredient: ")
                while j != "y":
                    k = input(f"confirm ingredient? (y/N): ")
                    if k == "y" and k != "N": j = k
                    else: ing = input(f"enter name of {i + 1}{ordinalsuffix} ingredient: ")
                ingredients.append(f"{ing}\n")

            for i in range(stepcount):
                ordinalsuffix = ordinalNumber(i+1)
                j = "N"
                step = input(f"enter {i+1}{ordinalsuffix} step: ")
                while j != "y":
                    k = input(f"confirm step? (y/N): ")
                    if k == "y" and k != "N": j = k
                    else: step = input(f"enter {i+1}{ordinalsuffix} step: ")
                steps.append(f"{step}\n")

            j = "N"
            extranotesquestion = input("do you want to add any extra notes? (y/N): ")
            if extranotesquestion == "y":
                i = 0
                while j != "stop":
                    i += 1
                    ordinalsuffix = ordinalNumber(i)
                    note = input(f"enter {i}{ordinalsuffix} note: ")
                    k = "N"
                    while k != "y":
                        l = input(f"confirm note? (y/N): ")
                        if l == "y":
                            k = l
                        else:
                            note = input(f"enter {i}{ordinalsuffix} note: ")
                    m = input("add another note? (y/N): ")
                    if m == "N" or m != "y":
                        j = "stop"
                    extranotes.append(f"{note}\n")

            j = "N"
            tagsquestion = input("do you want to add any tags? (y/N): ")
            if tagsquestion == "y":
                tags = input(f"enter all the tags(with the #): ")
            else:
                tags = "no_tags"

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
                recipe1 = []
                recipe2 = [ingredients, steps, extranotes]
                recipe3 = ["", "", ""]

                longestlist = max(len(ingredients), len(steps), len(extranotes))
                if longestlist == len(ingredients):
                    longestlist = ingredients
                elif longestlist == len(steps):
                    longestlist = steps
                elif longestlist == len(extranotes):
                    longestlist = extranotes

                for i in range(len(longestlist)):
                    for j in recipe2:
                        index = recipe2.index(j)
                        if i+1 > len(j):
                            recipe3[index] = "none"
                        else:
                            recipe3[index] = j[i]
                    recipe1.append([recipe3[0], recipe3[1], recipe3[2]])


                recipe1[0].append(tags)
                recipefile = open(f"{recipefolder}/{recipename}.csv", "w")
                writer = csv.writer(recipefile)
                writer.writerows(recipe1)
                recipefile.close()
                click.echo("recipe saved :)")

                recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
                recipelist = list(csv.reader(recipeindex))
                recipeindex.close()

                recipebutinlist = [f"{recipename}.txt", tags]
                recipelist.append(recipebutinlist)
                recipeindex = open(f"{recipefolder}/recipeindex.csv", "w+")
                writer = csv.writer(recipeindex)
                writer.writerows(recipelist)
                recipeindex.close()

    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list_recipes\" to create them")


@click.command()
@click.argument("recipename", required=True)
def remove_recipe(recipename):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if checkRecipeExistence(recipename):
            confirmation = input(f"u sure you wanna remove {recipename}? this will be permanent. (y/N): ")
            if confirmation == "y":
                (recipefolder / f"{recipename}.txt").unlink()
                click.echo("recipe removed :)")
                refreshIndex(recipefolder)
        else:
            click.echo(f"recipe with the name {recipename} doesnt exist in the recipe index :P\n"
                       f"try typing the recipe name without the .txt extension or running \"refresh_recipes\"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list_recipes\" to create them")


@click.command()
@click.argument("tags", default="no_tags", required=False)
def search_tags(tags):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
        reader = list(csv.reader(recipeindex))
        taglist = []
        recipelist = []
        for i in reader:
            recipelist.append(i[0])
            taglist.append(i[1])
        click.echo("recipes with the given tags:")
        for i in range(len(taglist)):
            if tags in taglist[i]:
                click.echo(f"{recipelist[i]} ---- {taglist[i]}")
        recipeindex.close()
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list_recipes\" to create them")


@click.command()
@click.argument("recipename", required=True)
@click.argument("tags", default="no_tags", required=False)
@click.option("--overwrite", "-o", is_flag=True, required=False)
def add_tags(recipename, tags, overwrite):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if checkRecipeExistence(recipename):
            recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
            reader = list(csv.reader(recipeindex))
            taglist = []
            recipelist = []
            for i in reader:
                recipelist.append(i[0])
                taglist.append(i[1])
            recipeindex.close()
            name = f"{recipename}.txt"
            i = recipelist.index(name)
            if not overwrite and tags != "no_tags":
                taglist[i] = f"{taglist[i]}{tags}"
                updateTags(recipelist, taglist)
            elif not overwrite and tags == "no_tags":
                click.echo("no tags were given to add :(")
            elif overwrite:
                taglist[i] = tags
                updateTags(recipelist, taglist)
        else:
            click.echo(f"recipe with the name {recipename} doesnt exist in the recipe index :P\n"
                       f"try typing the recipe name without the .txt extension or running \"refresh_recipes\"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list_recipes\" to create them")


def refreshIndex(recipefolder):
    filesinfolder = []
    alltxtfiles = list(recipefolder.glob("*.txt"))
    for i in alltxtfiles:
        filesinfolder.append(f"{i}".removeprefix(f"{recipefolder}/"))
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    alllist = list(csv.reader(recipeindex))
    reicpelist = []
    hashlist = []
    finallist = []
    for i in range(len(alllist)):
        reicpelist.append(alllist[i][0])
        if alllist[i][1] != "":
            hashlist.append(alllist[i][1])
        else:
            hashlist.append("no_tags")
    recipeindex.close()
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "w+")
    for i in range(len(filesinfolder)):
        if filesinfolder[i] != "recipeindex.txt":
            if filesinfolder[i] in reicpelist:
                j = reicpelist.index(filesinfolder[i])
                finallist.append([filesinfolder[i], hashlist[j]])
            else:
                finallist.append([filesinfolder[i], "no_tags"])
    writer = csv.writer(recipeindex)
    writer.writerows(finallist)
    recipeindex.close()


def ordinalNumber(i):
    if i == 1: return "st"
    elif i == 2: return "nd"
    elif i == 3: return "rd"
    else: return "th"


def updateTags(recipelist, taglist):
    recipefolder = Path.home() / "recipes"

    recipeindex = open(f"{recipefolder}/recipeindex.csv", "w+")
    writer = csv.writer(recipeindex)
    recipeindexlist = []
    for i in recipelist:
        index = recipelist.index(i)
        recipeindexlist.append([i, taglist[index]])
    writer.writerows(recipeindexlist)
    recipeindex.close()

    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    filelist = list(csv.reader(recipeindex))
    recipeindex.close()
    click.echo("recipes:")
    for i in filelist:
        if (recipefolder / i[0]).exists():
            click.echo(f"{i[0]} ---- {i[1]}: found :)")
        else:
            click.echo(f"{i[0]} ---- {i[1]}: not found :(")


def checkRecipeExistence(recipename):
    recipefolder = Path.home() / "recipes"
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    reader = list(csv.reader(recipeindex))
    recipelist = []
    for i in reader:
        recipelist.append(i[0])
    recipeindex.close()
    name = f"{recipename}.txt"
    if name in recipelist:
        return True
    else:
        return False
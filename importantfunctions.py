import csv
from pathlib import Path
import click


def refreshIndex(recipefolder):
    filesinfolder = []
    alltxtfiles = list(recipefolder.glob("*.csv"))
    for i in alltxtfiles:
        filesinfolder.append(f"{i}".removeprefix(f"{recipefolder}/"))
    finallist = []
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "w+")
    for i in range(len(filesinfolder)):
        if filesinfolder[i] != "recipeindex.csv":
            recipereader = list(csv.reader(open(f"{recipefolder}/{filesinfolder[i]}", "r")))
            j = recipereader[0][5]
            finallist.append([filesinfolder[i], j])
    writer = csv.writer(recipeindex)
    writer.writerows(finallist)
    recipeindex.close()


def ordinalNumber(i):
    if i == 1: return "st"
    elif i == 2: return "nd"
    elif i == 3: return "rd"
    else: return "th"


def updateTags(recipename, tags):
    recipefolder = Path.home() / "recipes"

    recipefile = open(f"{recipefolder}/{recipename}", "r")
    recipereader = list(csv.reader(recipefile))
    recipereader[0][5] = tags
    recipefile.close()

    recipefile = open(f"{recipefolder}/{recipename}", "w")
    recipewriter = csv.writer(recipefile)
    recipewriter.writerows(recipereader)
    recipefile.close()

    refreshIndex(recipefolder)

    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    filelist = list(csv.reader(recipeindex))
    recipeindex.close()
    click.echo("recipes:")
    for i in filelist:
        if (recipefolder / i[0]).exists():
            printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": found :)")
        else:
            printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": not found :(")


def checkRecipeExistence(recipename):
    recipefolder = Path.home() / "recipes"
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    reader = list(csv.reader(recipeindex))
    recipelist = []
    for i in reader:
        recipelist.append(i[0])
    recipeindex.close()
    name = f"{recipename}.csv"
    if name in recipelist and (recipefolder/name).exists():
        return "exists"
    elif name in recipelist and not (recipefolder/name).exists():
        return "only in index"
    elif name not in recipelist and (recipefolder/name).exists():
        return "not in index"
    else:
        return "doesn't exist"


def printRecipe(recipefolder, file, scale):
    recipefile = open(recipefolder / f"{file}", "r")
    reader = list(csv.reader(recipefile))
    ingredients = []
    ingredientamounts = []
    ingredientunits = []
    steps = []
    extranotes = []
    tags = reader[0][5]
    recipe = ""

    for i in reader:
        ingredients.append(i[0])
        ingredientamounts.append(i[1])
        ingredientunits.append(i[2])
        steps.append(i[3])
        extranotes.append(i[4])

    recipefile.close()

    recipe = "Ingredients:\n"
    for i in range(len(ingredients)):
        if ingredients[i] == "none":
            break
        else:
            if ingredientunits[i] == "no_unit" and ingredientamounts[i] == "no_amount":
                recipe += "".join(f"{i + 1}. {ingredients[i]}\n")
            elif ingredientunits[i] == "no_unit":
                recipe += "".join(f"{i + 1}. {ingredients[i]} -- {float(ingredientamounts[i])*scale}\n")
            elif ingredientamounts[i] == "no_amount":
                recipe += "".join(f"{i + 1}. {ingredients[i]}\n")
            else:
                recipe += "".join(f"{i + 1}. {ingredients[i]} -- {float(ingredientamounts[i])*scale} {ingredientunits[i]}\n")

    recipe += "".join("\nSteps:\n")
    for i in range(len(steps)):
        if steps[i] == "none":
            break
        else:
            recipe += "".join(f"{i + 1}. {steps[i]}\n")

    recipe += "".join("\nExtra notes:\n")
    for i in range(len(extranotes)):
        if extranotes[i] == "none":
            break
        else:
            recipe += "".join(f"{i + 1}. {extranotes[i]}\n")

    recipe += "".join("\nTags:\n")
    recipe += "".join(f"{tags}\n")

    click.echo(recipe)


def printRecipeList(a, b, c, d):
    click.secho(a, fg='green', nl=False)
    click.secho(b, nl=False)
    click.secho(c, fg='yellow', nl=False)
    click.secho(d)


def editIngredients(recipefolder, recipename, isNone, number):
    recipefile = open(f"{recipefolder}/{recipename}", "r")
    recipeinlist = list(csv.reader(recipefile))
    total = 0
    for i in recipeinlist:
        if i[0] == "none":
            break
        else:
            total += 1
    if isNone:
        number = int(input("enter ingredient number to modify: "))
    if number <= total:
        j = "N"
        ordinalsuffix = ordinalNumber(number)
        ing = input(f"enter name of {number}{ordinalsuffix} ingredient: ")
        ingamount = input(f"enter amount of {ing} required along with the unit: ")
        while j != "y":
            k = input(f"confirm ingredient and amount? (y/N): ")
            if k == "y":
                j = k
            else:
                ing = input(f"enter name of {number}{ordinalsuffix} ingredient: ")
                ingamount = input(f"enter amount of {ing} required along with the unit: ")
        a = "no_amount"
        b = "no_unit"
        if ingamount.isdigit():
            a = ingamount
            b = "no_unit"
        elif ingamount == "":
            a = "no_amount"
            b = "no_unit"
        else:
            index = 0
            for k, l in enumerate(ingamount):
                if not l.isdigit() and l != ".":
                    index = k
                    break
            a = ingamount[:index].strip()
            b = ingamount[index:].strip()
        recipeinlist[number - 1][0] = ing
        recipeinlist[number - 1][1] = a
        recipeinlist[number - 1][2] = b
        recipefile.close()
        recipefile = open(f"{recipefolder}/{recipename}", "w")
        writer = csv.writer(recipefile)
        writer.writerows(recipeinlist)
        recipefile.close()


def editSteps(recipefolder, recipename, isNone, number):
    recipefile = open(f"{recipefolder}/{recipename}", "r")
    recipeinlist = list(csv.reader(recipefile))
    total = 0
    for i in recipeinlist:
        if i[0] == "none":
            break
        else:
            total += 1
    if isNone:
        number = int(input("enter step number to modify: "))
    if number <= total:
        ordinalsuffix = ordinalNumber(number)
        j = "N"
        step = input(f"enter {number}{ordinalsuffix} step: ")
        while j != "y":
            k = input(f"confirm step? (y/N): ")
            if k == "y" and k != "N":
                j = k
            else:
                step = input(f"enter {number}{ordinalsuffix} step: ")
        recipeinlist[number - 1][3] = step
        recipefile.close()
        recipefile = open(f"{recipefolder}/{recipename}", "w")
        writer = csv.writer(recipefile)
        writer.writerows(recipeinlist)
        recipefile.close()


def editNotes(recipefolder, recipename, isNone, number):
    recipefile = open(f"{recipefolder}/{recipename}", "r")
    recipeinlist = list(csv.reader(recipefile))
    total = 0
    for i in recipeinlist:
        if i[0] == "none":
            break
        else:
            total += 1
    if isNone:
        number = int(input("enter note number to modify: "))
    if number <= total:
        ordinalsuffix = ordinalNumber(number)
        note = input(f"enter {number}{ordinalsuffix} note: ")
        k = "N"
        while k != "y":
            l = input(f"confirm note? (y/N): ")
            if l == "y":
                k = l
            else:
                note = input(f"enter {number}{ordinalsuffix} note: ")
        recipeinlist[number - 1][4] = note
        recipefile.close()
        recipefile = open(f"{recipefolder}/{recipename}", "w")
        writer = csv.writer(recipefile)
        writer.writerows(recipeinlist)
        recipefile.close()


def editRecipe(recipefolder, recipename, ing, step, note):
    printRecipe(recipefolder, recipename, 1)
    if ing is None and step is None and note is None:
        part = input("Ingredients ---- ing/i"
                     "\nSteps ---- step/s"
                     "\nNotes ---- note/n"
                     "\nwhich part of the recipe do you want to edit?: ")

        if part == "ing" or part == "i":
            editIngredients(recipefolder, recipename, True, 0)

        elif part == "step" or part == "s":
            editSteps(recipefolder, recipename, True, 0)

        elif part == "note" or part == "n":
            editNotes(recipefolder, recipename, True, 0)

        else:
            click.echo("invalid input entered :(\n"
                       "enter either ing or i, step or s, or note or n")
    else:
        if ing is not None:
            editIngredients(recipefolder, recipename, False, ing)
        if step is not None:
            editSteps(recipefolder, recipename, False, step)
        if note is not None:
            editNotes(recipefolder, recipename, False, note)


def listRecipesWithIndex(recipefolder, filelist):
    click.echo("recipes:")
    for i in filelist:
        if (recipefolder / i[0]).exists():
            j = filelist.index(i)
            click.secho(f"{i[0]}", fg='green', nl=False)
            click.echo(f" ---- ", nl=False)
            click.secho(f"{i[1]}", fg='green', nl=False)
            click.echo(" ---- ", nl=False)
            click.secho(f"{j}", fg='cyan')


def addTagsLogic(recipefolder, recipename, overwrite, tags):
    recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
    reader = list(csv.reader(recipeindex))
    taglist = []
    recipelist = []
    for i in reader:
        recipelist.append(i[0])
        taglist.append(i[1])
    recipeindex.close()
    i = recipelist.index(recipename)
    click.echo(recipename)
    if not overwrite and tags != "no_tags":
        updateTags(recipename, f"{taglist[i]}{tags}")
    elif not overwrite and tags == "no_tags":
        click.echo("no tags were given to add :(")
    elif overwrite:
        updateTags(recipename, tags)


def removeRecipeLogic(recipefolder, recipename):
    confirmation = input(f"u sure you wanna remove {recipename}? this will be permanent. (y/N): ")
    if confirmation == "y":
        (recipefolder / recipename).unlink()
        click.echo("recipe removed :)")
        refreshIndex(recipefolder)
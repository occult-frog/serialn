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
            printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": found :)")
        else:
            printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": not found :(")

    recipeindex.close()


@click.command()
@click.argument('recipename', required=False, default=None)
@click.option('--scale', '-s', required=False, default=1.0, type=float)
def view_recipe(recipename, scale):
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
                    click.secho(f"{i[0]}", fg='green', nl=False)
                    click.echo(f" ---- ", nl=False)
                    click.secho(f"{i[1]}", fg='green', nl=False)
                    click.echo(" ---- ", nl=False)
                    click.secho(f"{j}", fg='cyan')

            q = int(input("choose recipe: "))
            if q < len(filelist):
                printRecipe(recipefolder, filelist[q][0], scale)
            else:
                click.echo("choose a number from the range :)")

        elif checkRecipeExistence(recipename):
            printRecipe(recipefolder, f"{recipename}.csv", scale)

        else:
            click.echo(f"recipe with the name {recipename} doesnt exist in the recipe index :P\n"
                       f"try typing the recipe name without the .csv extension or running \"refresh-recipes\"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


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
                   "run \"list-recipes\" to create them")


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
            ingredientamounts = []
            ingredientunits = []
            steps = []
            extranotes = []
            tags = ""

            for i in range(ingredientcount):
                ordinalsuffix = ordinalNumber(i+1)
                j = "N"
                ing = input(f"enter name of {i+1}{ordinalsuffix} ingredient: ")
                ingamount = input(f"enter amount of {ing} required along with the unit: ")
                while j != "y":
                    k = input(f"confirm ingredient and amount? (y/N): ")
                    if k == "y" and k != "N": j = k
                    else:
                        ing = input(f"enter name of {i + 1}{ordinalsuffix} ingredient: ")
                        ingamount = input(f"enter amount of {ing} required along with the unit: ")
                ingredients.append(f"{ing}")
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
                ingredientamounts.append(f"{a}")
                ingredientunits.append(f"{b}")

            for i in range(stepcount):
                ordinalsuffix = ordinalNumber(i+1)
                j = "N"
                step = input(f"enter {i+1}{ordinalsuffix} step: ")
                while j != "y":
                    k = input(f"confirm step? (y/N): ")
                    if k == "y" and k != "N": j = k
                    else: step = input(f"enter {i+1}{ordinalsuffix} step: ")
                steps.append(f"{step}")

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
                    extranotes.append(f"{note}")

            j = "N"
            tagsquestion = input("do you want to add any tags? (y/N): ")
            if tagsquestion == "y":
                tags = input(f"enter all the tags(with the #): ")
            else:
                tags = "no_tags"

            click.echo("\n")
            recipe = "Ingredients:\n"
            for i in range(len(ingredients)):
                if ingredientunits[i] == "no_unit" and ingredientamounts[i] == "no_amount":
                    recipe += "".join(f"{i + 1}. {ingredients[i]}\n")
                elif ingredientunits[i] == "no_unit":
                    recipe += "".join(f"{i + 1}. {ingredients[i]} -- {ingredientamounts[i]}\n")
                elif ingredientamounts[i] == "no_amount":
                    recipe += "".join(f"{i + 1}. {ingredients[i]}\n")
                else:
                    recipe += "".join(f"{i + 1}. {ingredients[i]} -- {ingredientamounts[i]} {ingredientunits[i]}\n")

            recipe += "".join("\nSteps:\n")
            for i in range(len(steps)):
                recipe += "".join(f"{i+1}. {steps[i]}\n")
            if extranotesquestion == "y":
                recipe += "".join("\nExtra notes:\n")
                for i in range(len(extranotes)):
                    recipe += "".join(f"{i + 1}. {extranotes[i]}\n")
            recipe += "".join("\nTags:\n")
            recipe += "".join(f"{tags}\n")
            click.echo(recipe)

            confirmrecipe = input("confirm recipe? (y/N): ")
            if confirmrecipe == "y":
                recipe1 = []
                recipe2 = [ingredients, ingredientamounts, ingredientunits, steps, extranotes]
                recipe3 = ["", "", "", "", ""]

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
                    recipe1.append([recipe3[0], recipe3[1], recipe3[2], recipe3[3], recipe3[4]])


                recipe1[0].append(tags)
                recipefile = open(f"{recipefolder}/{recipename}.csv", "w")
                writer = csv.writer(recipefile)
                writer.writerows(recipe1)
                recipefile.close()
                click.echo("recipe saved :)")

                refreshIndex(recipefolder)

    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


@click.command()
@click.argument("recipename", required=True)
def remove_recipe(recipename):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if checkRecipeExistence(recipename):
            confirmation = input(f"u sure you wanna remove {recipename}? this will be permanent. (y/N): ")
            if confirmation == "y":
                (recipefolder / f"{recipename}.csv").unlink()
                click.echo("recipe removed :)")
                refreshIndex(recipefolder)
        else:
            click.echo(f"recipe with the name {recipename} doesnt exist in the recipe index :P\n"
                       f"try typing the recipe name without the .csv extension or running \"refresh-recipes\"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


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
                click.secho(f"{recipelist[i]}", fg='green', nl=False)
                click.secho(" ---- ", nl=False)
                click.secho(f"{taglist[i]}", fg='yellow')
        recipeindex.close()
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


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
            name = f"{recipename}.csv"
            i = recipelist.index(name)
            if not overwrite and tags != "no_tags":
                updateTags(name, f"{taglist[i]}{tags}")
            elif not overwrite and tags == "no_tags":
                click.echo("no tags were given to add :(")
            elif overwrite:
                updateTags(name, tags)
        else:
            click.echo(f"recipe with the name {recipename} doesnt exist in the recipe index :P\n"
                       f"try typing the recipe name without the .csv extension or running \"refresh-recipes\"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


@click.command()
@click.argument('recipename', required=False, default=None)
@click.option('--ing', '-i', required=False, type=int, default=None)
@click.option('--step', '-s', required=False, type=int, default=None)
@click.option('--note', '-n', required=False, type=int, default=None)
def edit_recipe(recipename, ing, step, note):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if recipename is None:
            recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
            filelist = list(csv.reader(recipeindex))
            recipeindex.close()
            click.echo("recipes:")
            for i in filelist:
                if (recipefolder / i[0]).exists():
                    j = filelist.index(i)
                    click.secho(f"{i[0]}", fg='green', nl=False)
                    click.echo(f" ---- ", nl=False)
                    click.secho(f"{i[1]}", fg='green', nl=False)
                    click.echo(" ---- ", nl=False)
                    click.secho(f"{j}", fg='cyan')
            q = int(input("choose recipe: "))
            click.echo("")
            if q < len(filelist):
                editRecipe(recipefolder, filelist[q][0], ing, step, note)
            else:
                click.echo("invalid number entered :(")

        elif checkRecipeExistence(recipename):
                editRecipe(recipefolder, f"{recipename}.csv", ing, step, note)

    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


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
    if name in recipelist:
        return True
    else:
        return False


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
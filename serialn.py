import csv
from pathlib import Path
import click
from importantfunctions import *


@click.command()
def hi():
    click.echo("hello")


@click.command()
@click.option('--tags', '-t', default=None, required=False)
def list_recipes(tags):
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

    if tags is None:
        for i in filelist:
            if (recipefolder/i[0]).exists():
                printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": found :)")
            else:
                printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": not found :(")

    elif tags is not None:
        for i in filelist:
            if tags in i[1]:
                if (recipefolder/i[0]).exists():
                    printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": found :)")
                else:
                    printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f": not found :(")

    recipeindex.close()


@click.command()
@click.argument('recipename', required=False, default=None)
@click.option('--scale', '-s', required=False, default=1.0, type=float)
@click.option('--global_settings', '-g', is_flag=True, default=False)
def view_recipe(recipename, scale, global_settings):
    recipefolder = Path.home()/"recipes"

    if recipefolder.exists() and (recipefolder/"recipeindex.csv").exists():
        if recipename is None:
            recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
            filelist = list(csv.reader(recipeindex))
            recipeindex.close()
            listRecipesWithIndex(recipefolder, filelist)
            q = int(input("choose recipe: "))
            if q < len(filelist):
                printRecipe(recipefolder, filelist[q][0], scale)
            else:
                click.echo("invalid number entered :(")
        elif checkRecipeExistence(recipename) == "exists":
            printRecipe(recipefolder, f"{recipename}.csv", scale, global_settings=global_settings)
        elif checkRecipeExistence(recipename) == "only in index":
            click.echo("recipe is only in index and not in folder :(")
        elif checkRecipeExistence(recipename) == "not in index":
            click.echo("recipe is not in index but is in recipe folder :)\n"
                       "run \"refresh-recipes\" to add it to recipe index")
        elif checkRecipeExistence(recipename) == "doesn't exist":
            click.echo("recipe is neither in the index nor in the recipe folder :(\n"
                       "try typing the recipe name without the .csv extension")
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
            printRecipeList(f"{i[0]}", f" ----", f" {i[1]}", f"")
    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


@click.command()
@click.argument("recipename", required=True)
@click.option('--ing', '-i', required=False, type=int, default=None)
@click.option('--step', '-res', required=False, type=int, default=None)
def add_recipe(recipename, ing, step):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if (recipefolder/f"{recipename}.csv").exists():
            click.echo(f"recipe with the name {recipename} already exists :P")
        else:
            if ing is None:
                ingredientcount = int(input("how many ingredients are there?: "))
            else:
                ingredientcount = ing
            if step is None:
                stepcount = int(input("how many steps are there?: "))
            else:
                stepcount = step
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
@click.argument("recipename", required=False, default=None)
def remove_recipe(recipename):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if recipename is None:
            recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
            filelist = list(csv.reader(recipeindex))
            recipeindex.close()
            listRecipesWithIndex(recipefolder, filelist)
            q = int(input("choose recipe: "))
            if q < len(filelist):
                removeRecipeLogic(recipefolder, filelist[q][0])
            else:
                click.echo("invalid number entered :(")
        elif checkRecipeExistence(recipename) == "exists":
            removeRecipeLogic(recipefolder, f"{recipename}.csv")
        elif checkRecipeExistence(recipename) == "only in index":
            click.echo("recipe is only in index and not in folder :(")
        elif checkRecipeExistence(recipename) == "not in index":
            click.echo("recipe is not in index but is in recipe folder :)\n"
                       "run \"refresh-recipes\" to add it to recipe index")
        elif checkRecipeExistence(recipename) == "doesn't exist":
            click.echo("recipe is neither in the index nor in the recipe folder :(\n"
                       "try typing the recipe name without the .csv extension")
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
@click.argument("recipename", required=False, default=None)
@click.option("--tags", "-t", default="no_tags", required=False)
@click.option("--overwrite", "-o", is_flag=True, required=False)
def add_tags(recipename, tags, overwrite):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if recipename is None:
            recipeindex = open(f"{recipefolder}/recipeindex.csv", "r")
            filelist = list(csv.reader(recipeindex))
            recipeindex.close()
            listRecipesWithIndex(recipefolder, filelist)
            q = int(input("choose recipe: "))
            if q < len(filelist):
                addTagsLogic(recipefolder, filelist[q][0], overwrite, tags)
            else:
                click.echo("invalid number entered :(")
        elif checkRecipeExistence(recipename) == "exists":
            addTagsLogic(recipefolder, f"{recipename}.csv", overwrite, tags)
        elif checkRecipeExistence(recipename) == "only in index":
            click.echo("recipe is only in index and not in folder :(")
        elif checkRecipeExistence(recipename) == "not in index":
            click.echo("recipe is not in index but is in recipe folder :)\n"
                       "run \"refresh-recipes\" to add it to recipe index")
        elif checkRecipeExistence(recipename) == "doesn't exist":
            click.echo("recipe is neither in the index nor in the recipe folder :(\n"
                       "try typing the recipe name without the .csv extension")
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

        elif checkRecipeExistence(recipename) == "exists":
            editRecipe(recipefolder, f"{recipename}.csv", ing, step, note)
        elif checkRecipeExistence(recipename) == "only in index":
            click.echo("recipe is only in index and not in folder :(")
        elif checkRecipeExistence(recipename) == "not in index":
            click.echo("recipe is not in index but is in recipe folder :)\n"
                       "run \"refresh-recipes\" to add it to recipe index")
        elif checkRecipeExistence(recipename) == "doesn't exist":
            click.echo("recipe is neither in the index nor in the recipe folder :(\n"
                       "try typing the recipe name without the .csv extension")


    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")


@click.command()
@click.option('--recipe', '-r', required=False, default=None)
def recipe_settings(recipe):
    recipefolder = Path.home() / "recipes"
    if recipefolder.exists() and (recipefolder / "recipeindex.csv").exists():
        if recipe is not None:
            if (recipefolder / f"{recipe}.csv").exists():
                recipefile = open(f"{recipefolder}/{recipe}.csv", "r")
                recipefiledata = list(csv.reader(recipefile))
                recipefile.close()

                if len(recipefiledata[0]) == 11:
                    settingtoedit = int(input('Ingredient color ------ 1\n'
                                              'Ingredient amount color ------ 2\n'
                                              'Step color ------ 3\n'
                                              'Note color ------ 4\n'
                                              'Tag color ------ 5\n'
                                              'which setting do you want to change?: '))
                    if settingtoedit == 1:
                        newvalue = input("enter new ingredient color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][6] = newvalue
                    elif settingtoedit == 2:
                        newvalue = input("enter new ingredient amount color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][7] = newvalue
                    elif settingtoedit == 3:
                        newvalue = input("enter new step color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][8] = newvalue
                    elif settingtoedit == 4:
                        newvalue = input("enter new note color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][9] = newvalue
                    elif settingtoedit == 5:
                        newvalue = input("enter new tag color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][10] = newvalue

                elif len(recipefiledata[0]) == 6:
                    recipefiledata[0].append("")
                    recipefiledata[0].append("")
                    recipefiledata[0].append("")
                    recipefiledata[0].append("")
                    recipefiledata[0].append("")
                    settingtoedit = int(input('Ingredient color ------ 1\n'
                                              'Ingredient amount color ------ 2\n'
                                              'Step color ------ 3\n'
                                              'Note color ------ 4\n'
                                              'Tag color ------ 5\n'
                                              'which setting do you want to change?: '))
                    if settingtoedit == 1:
                        newvalue = input("enter new ingredient color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][6] = newvalue
                    elif settingtoedit == 2:
                        newvalue = input("enter new ingredient amount color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][7] = newvalue
                    elif settingtoedit == 3:
                        newvalue = input("enter new step color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][8] = newvalue
                    elif settingtoedit == 4:
                        newvalue = input("enter new note color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][9] = newvalue
                    elif settingtoedit == 5:
                        newvalue = input("enter new tag color in the form of a hex code: ")
                        if newvalue == "None":
                            newvalue = None
                        recipefiledata[0][10] = newvalue

                elif len(recipefiledata[0]) > 6 and len(recipefiledata[0]) < 11:
                    pass

                recipefile = open(f"{recipefolder}/{recipe}.csv", "w")
                writer = csv.writer(recipefile)
                writer.writerows(recipefiledata)
                recipefile.close()

        else:
            if (recipefolder / "settings.csv").exists():
                pass
            else:
                settings = open(f"{recipefolder}/settings.csv", "w")
                writer = csv.writer(settings)
                a = [["ing_color", None], ["amount_color", None], ["step_color", None], ["note_color", None], ["tag_color", None]]
                writer.writerows(a)
                click.echo("settings file has been created :)\n")
                settings.close()

            settings = open(f"{recipefolder}/settings.csv", "r")
            settings_data = list(csv.reader(settings))
            settings.close()

            settingtoedit = int(input('Ingredient color ------ 1\n'
                                  'Ingredient amount color ------ 2\n'
                                  'Step color ------ 3\n'
                                  'Note color ------ 4\n'
                                  'Tag color ------ 5\n'
                                  'which setting do you want to change?: '))
            if settingtoedit == 1:
                newvalue = input("enter new ingredient color in the form of a hex code: ")
                if newvalue == "None":
                    newvalue = None
                settings_data[0][1] = newvalue
            elif settingtoedit == 2:
                newvalue = input("enter new ingredient amount color in the form of a hex code: ")
                if newvalue == "None":
                    newvalue = None
                settings_data[1][1] = newvalue
            elif settingtoedit == 3:
                newvalue = input("enter new step color in the form of a hex code: ")
                if newvalue == "None":
                    newvalue = None
                settings_data[2][1] = newvalue
            elif settingtoedit == 4:
                newvalue = input("enter new note color in the form of a hex code: ")
                if newvalue == "None":
                    newvalue = None
                settings_data[3][1] = newvalue
            elif settingtoedit == 5:
                newvalue = input("enter new tag color in the form of a hex code: ")
                if newvalue == "None":
                    newvalue = None
                settings_data[4][1] = newvalue

            settings = open(f"{recipefolder}/settings.csv", "w+")
            writer = csv.writer(settings)
            writer.writerows(settings_data)
            settings.close()

    else:
        click.echo("recipes folder or recipeindex file does not exist :(\n"
                   "run \"list-recipes\" to create them")

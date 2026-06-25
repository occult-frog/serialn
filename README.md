# serialn

serialn is a CLI tool/CLI app to view, edit, and store recipes.

serialn is made using the click module for python.

All the code is by me. No AI was used in the development of this project.

https://github.com/user-attachments/assets/8957fbe7-dc0e-4409-bc89-e1410c3501d6

serialn has only been tested on a Mac running a Apple Silicon processor. The releases are only for Macs running a Apple Silicon processor. If you want to run on Windows you will have to build and test it by yourself. There is no guarantee it will work on Windows or Intel Macs.

There is a zip in the source code containing videos on how to use the commands incase the descriptions given below aren't clear.

## Installation:
serialn has only been tested on Mac. There are two ways to install it:  
Method 1: 
1. Install python

2. Click the green code button at the top and click "Download ZIP"

3. Unzip the file you just downloaded

4. Open terminal and navigate to the unzipped folder

5. Run
    ```
    pip3 install -e .
    ```

6. Now you can open a new terminal window and run commands. You don't need to add the "./serialn" prefix as in the videos.

Method 2:  
1. Click on serialn-v1.0.0 under Releases which towards the right.

2. In the page that opens download the serialn-v1.0.0.zip file.

3. Unzip the downloaded file.

4. In a terminal window navigate to the directory the serialn file is in.

5. Now you can run commands. Just be sure to add the "./serialn" prefix as in the videos.


## Important things:
1. Run list-recipes when you first install serialn to create the recipes folder (present in your home folder) and recipeindex.csv file.

1. Don't pass the recipe name as [RECIPENAME].csv in view-recipe, add-recipe, and remove-recipe commands. Pass it without the extension.

1. All recipe names are stored in the recipeindex.csv file. The first column is for recipe names and the second column is for the tags they contain.

1. Recipes are stored in the form of .csv files. The first column is for ingredients, second for ingredient amounts, third for the unit, fourth for steps, fifth for extra notes, and sixth for tags.

1. The recipe files itself are stored in the recipes folder present in your home folder.

1. When entering the recipe amount in add-recipe, enter it as 500 mL or 500mL. Entering only a number assigns no unit to that ingredient and leaving it blank assigns neither an amount nor a unit.


## Current commands:
1. Lists all recipes present in the recipeindex.csv file. If the recipeindex.csv file or the recipes folder is not present, it creates them. Run this command when you first install serialn.
    ```
    list-recipes
    ```
2. Allows you to view a recipe. Don't pass the recipe name as [RECIPENAME].csv. Pass it without the extension. If the recipe name argument is left blank then a list of recipes with a number next to them will be shown. Choose a number from the list to view that recipe. Pass --scale or -s and then a number to scale it by that. The default scale is 1.
    ```
    view-recipe [RECIPENAME] [OPTIONS]
    ```
3. Takes all recipes present in the recipes folder and adds their name to the recipeindex.csv file. This command overwrites all the other recipe names in the recipeindex.csv file.
    ```
    refresh-recipes
    ```
4. Walks you through a proceedure to add a recipe. Requires a recipe name. Don't pass the recipe name as [RECIPENAME].csv. Pass it without the extension. When entering the recipe amount, enter it as 500 mL or 500mL. Entering only a number assigns no unit to that ingredient and leaving it blank assigns neither an amount nor a unit.
    ```
    add-recipe [RECIPENAME]
    ```
5. Removes the specified recipe. Don't pass the recipe name as [RECIPENAME].csv. Pass it without the extension. If the recipe name argument is left blank then a list of recipes with a number next to them will be shown. Choose a number from the list to remove that recipe.
    ```
    remove-recipe [RECIPENAME]
    ```
6. Searches through the recipe index for all recipes with the given tag. Leave the tags argument blank to search for recipes with no tags. It's best to pass the tags argument with a #.
    ```
    search-tags [TAGS]
    ```
7. Appends to or overwrites the tags for a given recipe. For the tags option pass --tag or -t along with the tag or leave it blank to assign an empty tag to the recipe. -o or --overwrite can be passed as options to overwrite the current tags. Don't pass the recipe name as [RECIPENAME].csv. Pass it without the extension. If the recipe name argument is left blank then a list of recipes with a number next to them will be shown.Choose a number from the list to add tags to that recipe.
    ```
    add-tags [OPTIONS] [RECIPENAME] [TAGS]
    ```
8. Allows you to edit a recipe. Don't pass the recipe name as [RECIPENAME].csv. Pass it without the extension. If the recipe name argument is left blank then a list of recipes with a number next to them will be shown. Choose a number from the list to edit that recipe. For the options pass:  
    I. -ing or -i with the ingredient number to edit that ingredient.  
    II. -step or -s with the step number to edit that step.  
    III. -note or -n with the note number to edit that note.  
or pass a combination of these.
    ```
    edit-recipe [RECIPENAME] [OPTIONS]
    ```

## Why was this made?

I felt like it would be pretty cool to manage recipes in a terminal window so yea. Also I wanted to experiment with cli tools in python.


## Credits

All the code is by me. No AI was used. Thanks to the Click team for the click module.
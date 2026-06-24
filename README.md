# serialn

serialn is a CLI tool/CLI app to view, edit, and store recipes. It is experimental so do expect stuff to break.

serialn is made using the click module for python.

All the code is by me. No AI was used in the development of this project.

## Important things:
1. Run list-recipes when you first install serialn to create the recipes folder (present in your home folder) and recipeindex.csv file.

2. Don't pass the recipe name as [RECIPENAME].csv in view-recipe, add-recipe, and remove-recipe commands. Pass it without the extension.

3. All recipe names are stored in the recipeindex.csv file. The first column is for recipe names and the second column is for the tags they contain.

4. Recipes are stored in the form of .csv files. The first column is for ingredients, second for ingredient amounts, third for the unit, fourth for steps, fifth for extra notes, and sixth for tags.

5. The recipe files itself are stored in the recipes folder present in your home folder.

6. When entering the recipe amount in add-recipe, enter it as 500 mL or 500mL. Entering only a number assigns no unit to that ingredient and leaving it blank assigns neither an amount nor a unit.


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
Or pass a combination of these.
    ```
    edit-recipe [RECIPENAME] [OPTIONS]
    ```
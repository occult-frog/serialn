# serialn

serialn is a CLI tool/CLI app to view, edit, and store recipes. It is experimental so do expect stuff to break. It's also not finished yet.

serialn is made using the click module for python.

All the code is by me. No AI was used in the development of this project.

## Important things:
1. Run list_recipes when you first install serialn to create the recipes folder (present in your home folder) and recipeindex.csv file.

2. Don't pass the recipe name as [RECIPENAME].txt in view_recipe, add_recipe, and remove_recipe commands. Pass it without the extension.

3. All recipe names are stored in the recipeindex.csv file. The first column is for recipe names and the second column is for the tags they contain. Recipes are stored in the form of .txt files.

4. The recipe files itself are stored in the recipes folder present in your home folder.

5. It's best to pass the tags argument with a (#) for the search_tags and add_tags commands.


## Current commands:
1. Lists all recipes present in the recipeindex.csv file. If the recipeindex.csv file or the recipes folder is not present, it creates them. Run this command when you first install serialn.
    ```
    list-recipes
    ```
2. Allows you to view a recipe. Don't pass the recipe name as [RECIPENAME].txt. Pass it without the extension. If the recipe name argument is left blank then a list of recipes with a number next to them will be shown. Choose a number from the list to view that recipe.
    ```
    view-recipe [RECIPENAME]
    ```
3. Takes all recipes present in the recipes folder and adds their name to the recipeindex.txt file. This command overwrites all the other recipe names in the recipeindex.txt file.
    ```
    refresh-recipes
    ```
4. Walks you through a proceedure to add a recipe. Requires a recipe name. Don't pass the recipe name as [RECIPENAME].txt. Pass it without the extension.
    ```
    add-recipe [RECIPENAME]
    ```
5. Removes the specified recipe. Don't pass the recipe name as [RECIPENAME].txt. Pass it without the extension.
    ```
    remove-recipe [RECIPENAME]
    ```
6. Searches through the recipe index for all recipes with the given tag. Leave the tags argument blank to search for recipes with no tags. It's best to pass the tags argument with a #.
    ```
    search-tags [TAGS]
    ```
7. Appends to or overwrites the tags for a given recipe. Leave tags argument blank to assign an empty tag to recipe. -o or --overwrite can be passed as options to overwrite the current tags. It's best to pass the tags argument with a #.
    ```
    add-tags [OPTIONS] [RECIPENAME] [TAGS]
    ```
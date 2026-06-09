# serialn

serialn is a CLI tool/ CLI app to view, edit, and store recipes.
serialn is made using the click module for python.
serialn is experimental so do expect stuff to break.

It's not finished yet.

All the code is by me. No AI was used in the development of this project.

## Important things:
1. Run list_recipes when you first install serialn to create the recipes folder (present in yuor home folder) and recipeindex.txt file.
    ```
    list_recipes
    ```
2. Don't pass the recipe name as [RECIPENAME].txt in view_recipe, add_recipe, and remove_recipe commands. Pass it without the extension.


## Current commands:
1. Lists all recipes present in the recipeindex.txt file. If the recipeindex.txt file or the recipes folder is not present, it creates them. Run this command when you first install serialn.
    ```
    list_recipes
    ```
2. Allows you to view a recipe. You need to pass the required recipe's name as the RECIPENAME argument to view that recipe. Don't pass the recipe name as [RECIPENAME].txt. Pass it without the extension.
    ```
    view_recipe [RECIPENAME]
    ```
3. Takes all recipes present in the recipes folder and adds their name to the recipeindex.txt file. This command overwrites all the other recipe names in the recipeindex.txt file.
    ```
    refresh_recipes
    ```
4. Walks you through a proceedure to add a recipe. Requires a recipe name. Don't pass the recipe name as [RECIPENAME].txt. Pass it without the extension.
    ```
    add_recipe [RECIPENAME]
    ```
5. Removes the specified recipe. Don't pass the recipe name as [RECIPENAME].txt. Pass it without the extension.
    ```
    remove_recipe [RECIPENAME]
    ```

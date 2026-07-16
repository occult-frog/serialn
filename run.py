import click
from serialn import *

@click.group()
def cli():
    pass

cli.add_command(list_recipes, name="list-recipes")
cli.add_command(view_recipe, name="view-recipe")
cli.add_command(refresh_recipes, name="refresh-recipes")
cli.add_command(add_recipe, name="add-recipe")
cli.add_command(remove_recipe, name="remove-recipe")
cli.add_command(search_tags, name="search-tags")
cli.add_command(add_tags, name="add-tags")
cli.add_command(edit_recipe, name="edit-recipe")
cli.add_command(recipe_settings, name="recipe-settings")

if __name__ == "__main__":
    cli()
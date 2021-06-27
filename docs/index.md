Python library to interact with Chefkoch.

## Installation & Documentation
```
pip install get-chefkoch
```
[Documentation](https://get-chefkoch.readthedocs.io/) can be found at Read the Docs.

## Examples
```python
from get_chefkoch import Recipe, Search

s = Search("Apfelstrudel")
recipe = s.recipes(limit=1)[0]
print(recipe.name)
print(recipe.description)
```

```python
from get_chefkoch import Recipe, Search

recipe = Search().recipeOfTheDay()

print(recipe.name)
print(recipe.description)
```

## Recipe-Class Parameters
     name              Name of the recipe
     id                Unique identification of the recipe
     description       Description of the recipe
     image             Url of a beautiful picture of the recipe
     ingredients       Recipe ingredients
     category          Recipe category
     prepTime          Preparation time
     totalTime         Total Time
     cookTime          Cooking time
     
     Many more parameters are available after calling Recipe().data_dump()


## Features
- Query the recipe of the day
- Search for specific recipe
- Querying information about a recipe(cooking time, description, ingredients, ...)
- Use the automatic suggestions from Chefkoch

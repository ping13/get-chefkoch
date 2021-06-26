# get_chefkoch
<a href="http://pepy.tech/count/get-chefkoch"><img src="http://pepy.tech/badge/get-chefkoch"></a> <a href="https://badge.fury.io/py/get-chefkoch"><img src="https://badge.fury.io/py/get-chefkoch.svg" alt="PyPI version" height="18"></a> <a href="https://github.com/olzeug/get_chefkoch/blob/master/LICENSE"><img src="https://img.shields.io/github/license/olzeug/get_chefkoch.svg"></a><br>
Python library to interact with Chefkoch.

## Examples:

```python
from get_chefkoch import Recipe, Search

s = Search("Apfelstrudel")
recipe = s.recipes(limit=1)
print(recipe.name)
print(recipe.description)
```

```python
from get_chefkoch import Recipe, Search

recipe = Search().recipeOfTheDay()

print(recipe.name)
print(recipe.description)
```

## Recipe-Class Parameters:
     name              Name of the recipe
     id                Unique identification of the recipe
     description       Description of the recipe
     image             Url of a beautiful picture of the recipe
     ingredients       Recipe ingredients
     category          Recipe category
     prepTime          Preparation time
     totalTime         Total Time
     cooktime          Cooking time
     
     Many more parameters are available after calling Recipe().data_dump()

## Features:

- Query the recipe of the day
- Search for specific recipe
- Querying information about a recipe(cooking time, description, ingredients, ...)
- Use the automatic suggestions from Chefkoch

## Get it now:

```
pip install get-chefkoch
```

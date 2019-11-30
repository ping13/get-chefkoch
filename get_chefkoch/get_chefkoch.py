#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests,feedparser
from bs4 import BeautifulSoup
from json import loads
class SaveRecipe(object):
    def __init__(self):
        pass
class chefkoch:
    def __init__(self):
        pass

    def daily_recipe(self):
        feed = feedparser.parse("https://www.chefkoch.de/rss/rezept-des-tages.php")
        url = feed['entries'][0]['link']
        recipe = self.get(url.split("/")[4])
        return(recipe)

    def get(self,recipe_id):
        url = "https://www.chefkoch.de/rezepte/"+ str(recipe_id)
        recipe = SaveRecipe()
        content = BeautifulSoup(requests.get(url).text, 'lxml')
        recibe_json = loads(content.findAll("script",type="application/ld+json")[1].text)
        recipe.name = recibe_json["name"]
        recipe.description = recibe_json["recipeInstructions"]
        recipe.image = recibe_json["image"]
        recipe.ingredients = recibe_json["recipeIngredient"]
        recipe.rating = float(recibe_json["aggregateRating"]["ratingValue"])
        recipe.category = recibe_json["recipeCategory"]
        recipe.published = recibe_json["datePublished"]
        #recipe.cooktime = recibe_json["cookTime"]
        recipe.autor = recibe_json["author"]["name"]
        recipe.reviews = recibe_json["aggregateRating"]["reviewCount"]
        recipe.Yield = recibe_json["recipeYield"]
        recipe.id = recipe_id
        return recipe
    def search(self,search):
        url = "https://www.chefkoch.de/rs/s0/"+search+"/Rezept.html"
        content = BeautifulSoup(requests.get(url).text, 'lxml')
        objects = loads(content.findAll('script', type='application/ld+json')[1].text)["itemListElement"]
        ckid = objects[0]["url"].split("/")[4]
        return(self.get(ckid))

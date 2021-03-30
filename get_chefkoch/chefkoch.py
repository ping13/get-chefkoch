#!/usr/bin/python3

from get_chefkoch.exceptions import *

import logging
from typing import Union, List

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re

def recipeParameter(func):
    def wrapper(self):
        if not self.gotMeta:
            self.getMeta()
        try:
            return func(self)
        except KeyError:
            return None
        
    return wrapper

class Recipe:
    def __init__(self, url: Union[str, None] = None, id: Union[str, None] = None) -> None:
        self._baseurl = "https://www.chefkoch.de/"
        
        if url != None and not isinstance(url, str):
            raise TypeError("Invalid argument type for 'url'.")
        
        if url != None:
            hostname = re.search('(?:http.*://)?(?P<host>[^:/ ]+)?', url).group('host')
            if "chefkoch" not in hostname:
                raise InvalidUrl("Url does not look like a 'Chefkoch' url.")
        
        if id != None and not isinstance(id, str):
            raise TypeError("Invalid argument type for 'id'.")
        
        if not url and not id:
            raise ArgumentError("You must either enter the 'id' or the 'url'")
        
        self._id = id
        self._url = url
        self.gotMeta = False
        self.data = {}
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        args = list()
        if self._url:
            args.append(f"url='{self._url}'")
        if self._id:
            args.append(f"url='{self._id}'")
        return "{}({})".format(self.__class__.__qualname__,', '.join(args))
    
    def _durationToTimeDelta(self, duration: str) -> timedelta:
        if isinstance(duration, timedelta):
            return duration
        
        replacements = {"M":"minutes",
                        "H": "hours",
                        "DT": "days"}
        e = {}
        i = 0
        while i < len(duration):
            letter = duration[i]
            if letter.isalpha() and (len(duration) == i+1 or not duration[i+1].isalpha()):
                if not duration[0].isdecimal():
                    if duration[:i+1] in replacements:
                        e[repalcements[duration[:i+1]]] = 0
                else:
                    for j,l in enumerate(duration[:i+1]):
                        if not l.isdecimal():
                            if duration[j:i+1] in replacements:
                                e[replacements[duration[j:i+1]]] = int(duration[:j])
                            break
                

                duration = duration[i+1:]
                i = 0
                continue
            i+=1
        return timedelta(**e)
    
    def getMeta(self) -> None:
        if self._url:
            url = self._url
            
        elif self._id:
            url = self._baseurl + "rezepte/" + self._id
        
        else:
            raise ArgumentError("Neither argument for 'id' nor for 'url' found.")
        
        req = requests.get(url)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'html.parser')
        
        data = soup.findAll("script", type="application/ld+json")
        
        if len(data) < 2:
            raise ParserError("Data section could not be found.")
            
        
        data = data[1].text
        
        try:
            self.data = json.loads(data)
        except json.decoder.JSONDecodeError:
            raise ParserError(f"Parsed section is not json-decodeable.{str(data)}")
        
        self._processData()
        self.gotMeta = True
        
    def _processData(self) -> None:
        timeKeys = ['prepTime', 'totalTime', 'cookTime']
        for timeKey in timeKeys:
            if timeKey in self.data:
                self.data[timeKey] = self._durationToTimeDelta(self.data[timeKey])
        
        if "datePublished" in self.data:            
            self.data["datePublished"] = datetime.strptime(self.data["datePublished"], "%Y-%m-%d")
       
    @property
    @recipeParameter
    def name(self) -> str:
        return self.data['name']
    
    @property
    @recipeParameter
    def id(self) -> str:
        return self._url.split("/")[4]
    
    @property
    @recipeParameter
    def description(self) -> str:
        return self.data['description']
    
    @property
    @recipeParameter
    def image(self) -> str:
        return self.data['image']
    
    @property
    @recipeParameter
    def ingredients(self) -> list:
        return self.data['recipeIngredient']
    
    @property
    @recipeParameter
    def category(self) -> str:
        return self.data['recipeCategory']
    
    @property
    @recipeParameter
    def prepTime(self) -> timedelta:
        d = self.data['prepTime']
        return self._durationToTimeDelta(d)
    
    @property
    @recipeParameter
    def totalTime(self) -> timedelta:
        d = self.data['totalTime']
        return self._durationToTimeDelta(d)
    
    @property
    @recipeParameter
    def cookTime(self) -> timedelta:
        d = self.data['cookTime']
        return self._durationToTimeDelta(d)
    
    def data_dump(self) -> dict:
        return self.data
    
class Search:
    def __init__(self, q: Union[str, None]=None) -> None:
        self._baseurl = "https://www.chefkoch.de/"
        self.q = q
        
    def __repr__(self) -> str:
        args = list()
        if self.q is not None:
            args.append(f"q='{self.q}'")
        
        return "{}({})".format(self.__class__.__qualname__,', '.join(args))
    
    def _argsToUrlParams(self, **args) -> str:
        argsString = [key+"="+str(arg) for key,arg in args.items()]
        return "&".join(argsString)
    
    def recipes(self, q: Union[str, None]=None, offset: int=0, limit: int=-1) -> List[Recipe]:
        if q is not None:
            self.q = q
        
        req = requests.get(self._baseurl+f'rs/s0/{self.q}/Rezepte.html')
        req.raise_for_status()
        
        soup = BeautifulSoup(req.text, 'html.parser')
        
        data = soup.findAll("script", type="application/ld+json")
        
        if len(data) < 2:
            raise ParserError("Data section could not be found.")
            
        
        data = data[1].text
        
        try:
            recipes = json.loads(data)["itemListElement"]
        except json.decoder.JSONDecodeError:
            raise ParserError("Parsed section is not json-decodeable.")
        
        result = list()
        
        for recipe in recipes[offset:limit]:
            result.append(Recipe(url=recipe['url']))
            
        return result
        
        
    def suggestions(self, q: Union[str, None]=None, **args) -> dict:
        if q is not None:
            self.q = q
        
        args = "&" + self._argsToUrlParams(**args)
        req = requests.get(self._baseurl+f"api/v2/search-suggestions/combined?t={self.q}{args}")
        req.raise_for_status()
        return req.json()
    
    def recipeOfTheDay(self) -> Recipe:
        import feedparser
        feed = feedparser.parse(self._baseurl+"rss/rezept-des-tages.php")
        url = feed['entries'][0]['link']
        return Recipe(url=url)


if __name__ == "__main__":
    r = Recipe(url="https://www.chefkoch.de/rezepte/2378411377118199/Scharfer-Hack-Nudelauflauf.html")
    print(r.name)
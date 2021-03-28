import pytest

from get_chefkoch import Recipe, exceptions
from datetime import timedelta

r = Recipe(url="https://www.chefkoch.de/rezepte/2378411377118199/Scharfer-Hack-Nudelauflauf.html")

def test_invalid_url():
    with pytest.raises(exceptions.InvalidUrl) as e_info:
        Recipe(url="rezepte/2378411377118199/Scharfer-Hack-Nudelauflauf.html")
        
def test_no_argument():
    with pytest.raises(exceptions.ArgumentError) as e_info:
        Recipe()
        
def test_invalid_argument_type():
    with pytest.raises(TypeError) as e_info:
        Recipe(url=0)
    with pytest.raises(TypeError) as e_info:
        Recipe(id=0)
        
def test_getMeta():
    r.getMeta()
        
def test__str__type():
    assert type(r.__str__()) is str
    
def test__repr__type():
    assert type(r.__repr__()) is str
    
def test_durationToTimeDelta():
    duration = "P0DT0H25M"
    e = r._durationToTimeDelta(duration)
    assert isinstance(e, timedelta)
    assert e == timedelta(seconds=1500)

def test_recipe_name():
    assert type(r.name) is str
    
def test_recipe_id():
    assert type(r.id) is str
    
def test_recipe_description():
    assert type(r.description) is str
    
def test_recipe_image():
    assert type(r.image) is str
    
def test_recipe_ingredients():
    assert len(r.ingredients) > 0
    
def test_recipe_category():
    assert type(r.category) is str

def test_recipe_prepTime():
    assert type(r.prepTime) is timedelta
    
def test_recipe_totalTime():
    assert type(r.totalTime) is timedelta
    
def test_recipe_cookTime():
    assert type(r.cookTime) is timedelta
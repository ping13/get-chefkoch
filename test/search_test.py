from get_chefkoch import Search, Recipe, exceptions

s = Search()


def test__repr__type():
    assert type(s.__repr__()) is str
    
def test_argsToUrlParams():
    assert s._argsToUrlParams(t="23", e={}, f=[], i=1, b="test") == 't=23&e={}&f=[]&i=1&b=test'
    
def test_search_recipes():
    assert isinstance(s.recipes("Apfelstrudel"), list)
    
def test_suggestions():
    assert isinstance(s.suggestions("Toas"), dict)
    
def test_recipeOfTheDay():
    assert isinstance(s.recipeOfTheDay(), Recipe)
    
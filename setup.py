from setuptools import setup
__project__ = "get_chefkoch"
__version__ = "0.0.5"
__description__ = "A Python Library with which you can get data from Chefkoch."

with open("README.md", "r") as fh:
    long_description = fh.read()

__packages__ = ["get_chefkoch"]
__keywords__ = ["Chefkoch","python"]
__requires__ = ["requests","feedparser","bs4","json","lxml"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    keywords = __keywords__,
    requires = __requires__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olzeug/get_chefkoch",
    python_requires='>=3.0',
)

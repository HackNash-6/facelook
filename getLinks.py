__author__ = 'chrisgraff'

import requests
import re

SEED_PAGE = "http://www.people.com/people/celebrities/"

NAMES_LIST = ['Ashton Kutcher', 'Taylor Swift']

def getPage(url):
    """
    :param url: (string) url of page to be scraped
    :returns: (string) html of scraped page
    """
    r = requests.get(SEED_PAGE)
    return r.text

def getNames(page):
    """
    :param page: (string) html from getPage()
    :returns: (list) ['Adam Levine', 'Britney Spears', 'Christie Brinkley']
    """
    result = []
    lines = page.split('\n')
    return lines[2]


def getCelebPage(name):
    """
    :param name: (string) A celebrity name
    :return: (string) url of celeb's IMDB page
    """
    BASE_URL = "http://www.imdb.com/search/name?name="
    name_list = name.split(' ')
    name_string = '%20'.join(name_list)
    search_result = BASE_URL + name_string

print (getCelebPage("Ashton Kutcher"))

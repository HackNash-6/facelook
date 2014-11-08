__author__ = 'chrisgraff'

import requests


SEED_PAGE = "http://www.people.com/people/celebrities/"

NAMES_LIST = ['Ashton Kutcher', 'Taylor Swift']

def getPage(url):
    """
    :param url: (string) url of page to be scraped
    :returns: (string) html of scraped page
    """
    r = requests.get(url)
    return r.text

def getNames(page):
    """
    :param page: (string) html from getPage()
    :returns: (list) ['Adam Levine', 'Britney Spears', 'Christie Brinkley']
    """
    result = []
    lines = page.split('\n')
    return lines


def get_celeb_page(name):
    """
    :param name: (string) A celebrity name
    :return: (string) url of celeb's IMDB page
    """
    BASE_URL = "http://www.imdb.com/search/name?name="
    name_list = name.split(' ')
    name_string = '%20'.join(name_list)
    search_result = BASE_URL + name_string

    search_result_page = getPage(search_result)
    start_pos = search_result_page.find('title="{}"'.format(name))
    error_pos = search_result_page.find('No results.')
    if error_pos != -1:
        return None
    search_result_slice = search_result_page[start_pos-30: start_pos-3]
    celebrity_page_link = "http://www.imdb.com/name/" + search_result_slice.split('/')[-1]
    return celebrity_page_link


def test_get_celeb_page():
    TEST_NAMES = ['Ashton Kutcher', 'Gwen Stefani', 'Paul Rudd', 'David Hasselhoff',
                  'Liv Tyler','Tiger Woods', 'Lucy Liu', 'Ryan Seacrest', 'Sally Field',
                  'Tyra Banks', 'Vince Vaughn', 'Will Smith', 'Katy Perry', 'Kelly Ripa',
                  'Emma Stone', 'Emma Roberts', 'Julia Roberts', 'Paris Hilton', 'Jon Hamm',
                  'Bruce Willis', 'Brad Pitt', 'Angelina Jolie', 'George Clooney', 'Tim McGraw',
                  'Jennifer Lawrence', 'Keith Urban', 'Kenny Chesney', 'Faith Hill'
                  ]

    print('total number of celebs is: {}'.format(len(TEST_NAMES)))



    #celebs = [get_celeb_page(name) for name in TEST_NAMES]
    for name in TEST_NAMES:
        print name, get_celeb_page(name)

#print(getCelebPage('David Hasselhoff'))
test_get_celeb_page()
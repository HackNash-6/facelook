__author__ = 'chrisgraff'

import time
import requests
import json
import lxml


import GetNames
import GetPicture
import getPhotos


NAMES_LIST = GetNames.get_names()


def getPage(url):
    """
    :param url: (string) url of page to be scraped
    :returns: (string) html of scraped page
    """
    r = requests.get(url)
    return r.text


def get_celeb_page(name):
    """
    :param name: (string) A celebrity name
    :return: (string) url of celeb's IMDB page
    """
    #TODO: Soon to be deprecated by GetNames.get_imdb_links()
    
    BASE_URL = "http://www.imdb.com/search/name?name="
    BAD_LAST_NAMES = ['Knowles', 'Kardashian', 'Saldana', 'Dion', 'Cruz', 'Zellweger', 'Minnillo']
    BAD_FIRST_NAMES = ['Gisele']
    name_list = name.split(' ')
    if len(name_list) > 1 and (name_list[1] in BAD_LAST_NAMES or name_list[0] in BAD_FIRST_NAMES):
        return None
    name_string = '%20'.join(name_list)
    search_result = BASE_URL + name_string

    search_result_page = getPage(search_result)
    time.sleep(.4)
    print('sleeping...after retrieving {}.'.format(name))
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
                  'Jennifer Lawrence', 'Keith Urban', 'Kenny Chesney', 'Faith Hill',
                  ]

    print('total number of celebs is: {}'.format(len(TEST_NAMES)))

    celebs = [get_celeb_page(name) for name in TEST_NAMES]
    for name in celebs:
        print name, get_celeb_page(name)


def deliver_links():
    """
    :return: json file {'celeb_name': 'celeb_img_link'}
    """

    links_dict = {name: GetPicture.get_picture(get_celeb_page(name)) for name in NAMES_LIST}

    for k, v in links_dict.items():
        if v == [] or v is None:
            del links_dict[k]

    with open('new_celeb_img_links.json', 'w') as outfile:
        json.dump(links_dict, outfile, indent=4)




if __name__ == '__main__':
    deliver_links()
__author__ = 'Jack'

import requests
from lxml import html

def get_imdb_links():
    """
    :returns: (list) ['url 1', 'url 2', 'url 3']
    :comment: returns celeb page urls from imdb.com search results'
    """
    IMDB_SEED = "http://www.imdb.com/search/name?gender=male,female&ref_nv_cel_m_3&start="
    return ['{}{}'.format(IMDB_SEED, x) for x in xrange(1, 2000, 50)]

def get_imdb_names(imdb_urls_list):
    """
    :param imdb_urls_list: A list of urls
    :return: (list) list of celeb names (a string)
    TODO: Finish this !!!
    """
    names_list = []
    for url in imdb_urls_list:
        pass #...this is where I left off
    return


def get_names():
    #gets names from people.com
    input_array = []
    allNames = requests.get('http://www.people.com/people/celebrities/')
    tree = html.fromstring(allNames.text)

    #parse doc for names of celebs
    celeb_elements = tree.xpath('//dt[. = "A"]/following-sibling::dd')
    celebs_second = tree.xpath('//dt[. = "G"]/following-sibling::dd')
    celebs_third = tree.xpath('//dt[. = "L"]/following-sibling::dd')
    celebs_fourth = tree.xpath('//dt[. = "R"]/following-sibling::dd')

    celeb_elements += celebs_second + celebs_third + celebs_fourth


    for stuff in celeb_elements:
        person = stuff.text_content()
        if ('Usher' in person):
            input_array.append(stuff.text_content() + ' Raymond')
        else:
            input_array.append(stuff.text_content())


    return input_array


print(get_imdb_names(get_imdb_links()))

if __name__ == '__main__':
    pass





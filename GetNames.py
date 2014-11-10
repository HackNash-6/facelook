__author__ = 'Jack'
__author__= 'chrisgraff'
__author = 'Bennett'

import requests
from lxml import html

# TODO get_imdb_links(),

def get_page(url):
    """
    :param url: (string)
    :return: html of given page
    """
    page = requests.get(url)
    return html.fromstring(page.text)


def get_celeb_gender(imdb_celeb_bio):
    """
    :param imdb_celeb_bio: (string) html of a celeb's imdb page
    :return: (string or None) 'boy' or 'girl' or None
    :comment: parse celeb's imdb page bio for masculine/feminine pronouns to determine gender.
    """
    TEST_TEXT = 'Jonny Weston was born in 1988 and was raised in Charleston, South Carolina. After turning 18, ' \
           'he went to the University of South Carolina in Columbia, SC, where he took a theatre class, fell in love' \
           ' with acting and decided to pursue it. He is probably most known for his part as Jay Moriarty in' \
           ' Chasing Mavericks (2013).'

    celeb_bio = TEST_TEXT.lower().split()
    boy_pronouns = ('he', 'him')
    girl_pronouns = ('she', 'her')
    is_boy = False
    is_girl = False
    for word in celeb_bio:
        if (word in boy_pronouns): is_boy = True
        if (word in girl_pronouns): is_girl = True

    if is_boy and not is_girl:
        return 'boy'
    elif is_girl and not is_boy:
        return 'girl'
    return None

def get_imdb_links():
    """
    :returns: (list) ['url 1', 'url 2', 'url 3']
    :comment: returns celeb page urls from imdb.com search results'
    TODO currently returning a list of search pages.  We need a list of celeb page urls (derived from each search page)
    """
    IMDB_SEED = "http://www.imdb.com/search/name?gender=male,female&ref_nv_cel_m_3&start="
    search_pages = ['{}{}'.format(IMDB_SEED, x) for x in xrange(1, 1000, 50)]
    for url in search_pages:
        print(url)



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
    tree = get_page('http://www.people.com/people/celebrities/')

    #parse doc for names of celebs
    celeb_elements = tree.xpath('//dt[. = "A"]/following-sibling::dd')
    celebs_second = tree.xpath('//dt[. = "G"]/following-sibling::dd')
    celebs_third = tree.xpath('//dt[. = "L"]/following-sibling::dd')
    celebs_fourth = tree.xpath('//dt[. = "R"]/following-sibling::dd')

    celeb_elements += celebs_second + celebs_third + celebs_fourth


    for stuff in celeb_elements:
        person = stuff.text_content()
        if ('Usher' in person):
            input_array.append(stuff.text_content() + ' Raymond') # Usher in IMDB as 'Usher Raymond'
        else:
            input_array.append(stuff.text_content())


    return input_array


#print(get_imdb_names(get_imdb_links()))
#print(get_imdb_links())
#print(get_celeb_gender())


if __name__ == '__main__':
    pass





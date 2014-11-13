__author__ = 'Jack'
__author__= 'chrisgraff'
__author__ = 'Bennett'

import requests
import time
from lxml import html


def get_page(url):
    """
    :param url: (string)
    :return: html of given page
    """
    page = requests.get(url).text
    return html.fromstring(page)


def get_celeb_gender(imdb_celeb_bio):
    """
    :param imdb_celeb_bio: (string) html of a celeb's imdb page
    :return: (string or None) 'boy' or 'girl' or None
    :comment: parse celeb's imdb page bio for masculine/feminine pronouns to determine gender.
    """
    celeb_bio = imdb_celeb_bio.lower().split()
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

def get_imdb_links(start_page_num, stop_page_num):
    """
    :param start_page_num, stop_page_num: (int) range of search pages to search
    :returns: (dict) {"celeb name": "celeb imdb page url"}
    :comment: returns all celebs found on imdb.com search results'
    """
    celeb_dict = {}
    invalid_celebs = ['', u'sa\xafd taghmaoui',]
    IMDB_SEED = "http://www.imdb.com/search/name?gender=male,female&ref_nv_cel_m_3&start="

    search_result_pages = ['{}{}'.format(IMDB_SEED, x) for x in xrange(start_page_num, stop_page_num, 50)]

    for page in search_result_pages:
        celeb_page_tree = get_page(page)
        print('retrieving {}'.format(celeb_page_tree))
        celeb_objects = celeb_page_tree.xpath('//td[@class="image"]/a') #list of all celeb objects on page

        for celeb in celeb_objects:
            if filter_unicode(celeb.attrib['title']) not in invalid_celebs:
                celeb_dict[filter_unicode(celeb.attrib['title'])] = celeb.attrib['href'] #.attrib gives us the goods!
                print('saving entry for {}'.format(celeb.attrib))
        time.sleep(.5)
    return celeb_dict


def filter_unicode(name):
    """
    :param name: (unicode string) word/name that may or may not contain unicode chars
    :return: (string) same as input but with unicode chars replaced (if none...returns input)
    """
    def get_char(c):
        if char in [u'\xc3', u'\xe3', '.']: # \xe3 is 'seen' within u'Ren\xc3\xa9e Zellweger'
            return ''
        elif char in [u'\xa4', u'\xa5', u'\xa1', u'\xe0', u'\xe1', u'\xe2', u'\xe4', u'\xe5']:
            return 'a'
        elif char in [u'\xe9', u'\xe8', u'\xa8', u'\xeb', u'\xea', u'\xa9', u'\xab']:
            return 'e'
        elif char in [u'\xec', u'\xed', u'\xad', u'\xee', u'\xef' u'\xaf']:
            return 'i'
        elif char in [u'\xb8', u'\xb3', u'\xf2', u'\xf3', u'\xf4', u'\xf5', u'\xf6']:
            return 'o'
        elif char in [u'\xf9', u'\xfa', u'\xfb', u'\xfc', u'\xbc']:
            return 'u'
        elif char in [u'\xf1', u'\xb1']:
            return 'n'
        elif char in [u'\u0155']:
            return 'r'
        elif char in [u'\xa7']:
            return 'c'
        elif char in [u'\xbf']:
            return 'y'
        else:
            return c

    result = ''
    for char in name.lower():
        result += (get_char(char))

    return result

def test_filter_unicode():
    uni_list = [u'Ren\xc3\xa9e Zellweger', u'Chlo\xc3\xab Grace Moretz', u'Ingrid Bols\xc3\xb8 Berdal',
            u'Ang\xc3\xa9lica Celaya', u'M\xc3\xa4dchen Amick', u'Jenna von O\xc3\xbf', u'Zo\xc3\xab Wanamaker',
            u'Alejandro Gonz\xc3\xa1lez I\xc3\xb1\xc3\xa1rritu', u'Michael Pe\xc3\xb1a', u'Pen\xc3\xa9lope Cruz',
            u'Aitana S\xc3\xa1nchez-Gij\xc3\xb3n', u'Magn\xc3\xbas Scheving', u'Stellan Skarsg\xc3\xa5rd',
            u'Nicole Mu\xc3\xb1oz', u'Birgitte Hjort S\xc3\xb8rensen', u'Gisele B\xc3\xbcndchen',
            u'Oscar Nu\xc3\xb1ez', u'Astrid Berg\xc3\xa8s-Frisbey', u'Guillermo D\xc3\xadaz',
            u'Khlo\xc3\xa9 Kardashian', u'Fran\xc3\xa7ois Arnaud', u'Sa\xc3\xafd Taghmaoui',
            u'Stef\xc3\xa1n Karl Stef\xc3\xa1nsson']

    for name in uni_list:
        print filter_unicode(name)



#def get_names():
    #gets names from people.com
    #-------get_names() DEPRECATED since we already have these names & images------###
    #input_array = []
    #allNames = requests.get('http://www.people.com/people/celebrities/') # WE ALREADY HAVE THESE
    #tree = html.fromstring(allNames.text)

    #parse doc for names of celebs
    #celeb_elements = tree.xpath('//dt[. = "A"]/following-sibling::dd')
    #celebs_second = tree.xpath('//dt[. = "G"]/following-sibling::dd')
    #celebs_third = tree.xpath('//dt[. = "L"]/following-sibling::dd')
    #celebs_fourth = tree.xpath('//dt[. = "R"]/following-sibling::dd')

    #celeb_elements += celebs_second + celebs_third + celebs_fourth

    #for stuff in celeb_elements:
        #person = stuff.text_content()
        #if ('Usher' in person):
            #input_array.append(stuff.text_content() + ' Raymond') # Usher in IMDB as 'Usher Raymond'
        #else:
            #input_array.append(stuff.text_content())

    #return input_array

#print(get_imdb_links(1, 2))
#print(test_filter_unicode())

if __name__ == '__main__':
    pass





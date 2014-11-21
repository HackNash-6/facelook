__author__ = ['Jack', 'chrisgraff', 'Bennett']

import time
import requests
import json
from lxml import html

#TODO: get_new_links.py --- replaces getLinks.py, GetNames.py, GetPicture.py

def get_page(url):
    """
    :param url: (string)
    :return: (obj) html tree of given page
    :ref lxml: http://lxml.de/lxmlhtml.html
    """
    page = requests.get(url).text
    return html.fromstring(page)


def get_single_imdb_page(name):
    """
    :param name: (string) A celeb name
    :return: (string) relative url of celeb's imdb page: '/name/nm0000126'
    """
    base_url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
    url_params = "&s=nm"
    name_str = '+'.join(filter_unicode(name).split())
    search_result_page = base_url + name_str + url_params
    tree = get_page(search_result_page)
    result = tree.xpath('//td[@class="primary_photo"]/a')[0] #grab the first result on the page
    celeb_id = result.attrib['href'].split('/')[2]
    return '/name/{}/'.format(celeb_id)


def get_celeb_bio(tree_obj):
    """
    :param tree_obj: (object) html tree of celeb's imdb page
    :return: (set) bio from celeb's imdb page - set is 2x more efficient for searching vs string
    """
    bio = tree_obj.xpath('//div[@class="name-trivia-bio-text"]/div/text()')
    return set([filter_unicode(word) for word in ''.join(bio).strip('\n').lower().split()])


def celeb_is_girl(imdb_celeb_bio):
    """
    :param imdb_celeb_bio: (set) bio from celeb's imdb page
    :return: (Boolean) True if feminine pronouns present, False if masculine...or None if neither/both present
    :comment: parse celeb's imdb page bio for masculine/feminine pronouns.
    """
    boy_pronouns = ('he', 'his')
    girl_pronouns = ('she', 'her')
    is_boy = False
    is_girl = False

    if boy_pronouns[0] in imdb_celeb_bio or boy_pronouns[1] in imdb_celeb_bio:
        is_boy = True
    if girl_pronouns[0] in imdb_celeb_bio or girl_pronouns[1] in imdb_celeb_bio:
        is_girl = True

    if is_boy and not is_girl:
        return False
    elif is_girl and not is_boy:
        return True
    return None


def filter_unicode(name):
    """
    :param name: (string) word/name that may or may not contain unicode chars
    :return: (string) same as input but with unicode chars replaced (if none...returns input)
    """
    def fix_char(letter):
        """
        :param letter: (string) a single char that may or may not trigger a unicode error.
        :return: (string) the ascii equiv found in uni_dict...else the original char
        """
        uni_dict = {
            u'\xc3': '',  u'\xe3': '', '.': '',
            u'\xa1': 'a', u'\xa4': 'a', u'\xa5': 'a',
            u'\xe0': 'a', u'\xe1': 'a', u'\xe2': 'a', u'\xe4': 'a',  u'\xe5': 'a',
            u'\xa8': 'e', u'\xa9': 'e', u'\xab': 'e',
            u'\xe8': 'e', u'\xe9': 'e', u'\xea': 'e', u'\xeb': 'e',
            u'\xad': 'i', u'\xaf': 'i',
            u'\xec': 'i', u'\xed': 'i', u'\xee': 'i', u'\xef': 'i',
            u'\xb3': 'o', u'\xb8': 'o',
            u'\xf2': 'o', u'\xf3': 'o', u'\xf4': 'o', u'\xf5': 'o', u'\xf6': 'o',
            u'\xba': 'u', u'\xbc': 'u',
            u'\xf9': 'u', u'\xfa': 'u', u'\xfb': 'u', u'\xfc': 'u',
            u'\xf1': 'n', u'\xb1': 'n', u'\xa7': 'c', u'\xbf': 'y', u'\u0155': 'u'
        }

        try:
            return uni_dict[letter]
        except KeyError:
            return letter


    result = ''
    for c in name.lower():
        result += (fix_char(c))

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


def get_picture(html_tree):
    """
    :param html_tree: (obj) html tree object of a celeb's imdb page
    :return: url (string) url of the profile pic on celeb's imdb page
    """
    try:
        return html_tree.xpath('//img[@id = "name-poster"]/@src')[0]
    except IndexError:
        print('No picture found for {}'.format(' '.join(html_tree.findtext('head/title').split()[:2])))
        pass


def get_imdb_links(start, stop):
    """
    :param start, stop: (int) how many celebs do you want?  More->less famous via imdb Star-score.
    :returns: (dict) {"celeb name": "celeb imdb page url"}
    :comment: returns all celebs found on imdb.com search results'
    :ref .attrib: https://docs.python.org/3.1/library/xml.etree.elementtree.html#the-element-interface
    """
    celeb_dict = {}

    invalid_celebs = {'', 'Usher'} # Error causing names reside in this set literal
    imdb_seed = "http://www.imdb.com/search/name?gender=male,female&ref_nv_cel_m_3&start="
    celeb_page_seed = "http://www.imdb.com"

    search_result_pages = ['{}{}'.format(imdb_seed, x) for x in xrange(start, stop, 50)]

    for page in search_result_pages:
        celeb_page_tree = get_page(page)
        celeb_objects = celeb_page_tree.xpath('//td[@class="image"]/a') # A list of all celeb objects on page

        for celeb in celeb_objects:
            if filter_unicode(celeb.attrib['title']) not in invalid_celebs:
                celeb_page = get_page(celeb_page_seed + celeb.attrib['href'])
                is_girl = celeb_is_girl(get_celeb_bio(celeb_page))
                celeb_dict[filter_unicode(celeb.attrib['title'])] = \
                    [celeb.attrib['href'], get_picture(celeb_page), is_girl] # [page, pic, is_girl]
                print('saving entry for {}'.format(celeb.attrib))
            time.sleep(.4)
    return celeb_dict


def deliver_imdb_links(start, stop, filename):
    """
    :param start, stop, filename: (ints, str) range of most->least famous according to imdb, filename to be saved
    :return: (file.json) {'celeb_name': ['celeb_page_link', 'celeb_img_link', is_girl (boolean)]
    """
    links_dict = get_imdb_links(start, stop) # {name: [page_url, pic_url, is_girl]}

    for k, v in links_dict.items():
        if v == [] or v[1] is None:
            del links_dict[k] #celebs without an img are deleted

    with open(filename, 'w') as outfile:
        json.dump(links_dict, outfile, indent=4)

#TODO: grab the next 1000 celebs (4001-5000)
#deliver_imdb_links(4001, 5000, 'new_celeb_img_links5.json')


if __name__ == '__main__':
    pass
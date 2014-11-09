__author__ = 'Jack'

import requests
from lxml import html

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
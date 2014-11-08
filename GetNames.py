__author__ = 'Jack'

import requests
from lxml import html
celeb_names = []

def getNames(input_array):
    #gets names from people.com

    allNames = requests.get('http://www.people.com/people/celebrities/')
    tree = html.fromstring(allNames.text)

    #parse doc for names of celebs
    celeb_elements = tree.xpath('//dt[. = "A"]/following-sibling::dd')
    celebs_second = tree.xpath('//dt[. = "G"]/following-sibling::dd')
    celebs_third = tree.xpath('//dt[. = "L"]/following-sibling::dd')
    celebs_fourth = tree.xpath('//dt[. = "R"]/following-sibling::dd')

    celeb_elements += celebs_second + celebs_third + celebs_fourth


    for stuff in celeb_elements:
        input_array.append(stuff.text_content())






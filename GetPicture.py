__author__ = 'Jack'

import requests
from lxml import html


def get_picture(url):
    """
    :param URL: (string) url of an imdb celeb page such as: "http://www.imdb.com/name/nm1297015/"
    :return: URL (string) url of the profile pic on celeb's imdb page
    """
    if(url is not None):
        if url[:5] not in ["http", "www."]:
            url = "{}{}".format("http://www.imdb.com", url)
        allNames = requests.get(url)

        tree = html.fromstring(allNames.text)

        #get the pic
        celeb_elements = tree.xpath('//img[@id = "name-poster"]/@src')
        return celeb_elements
    else:
        return None




if __name__ == '__main__':
    pass

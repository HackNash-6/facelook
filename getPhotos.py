__author__ = 'chrisgraff'

import time
import json
import subprocess


def get_links_from_json(json_file):
    """
    :param json_file: (file) {'celeb name': 'url of celeb photo'}
    :return: (dict) same as input
    """
    with open(json_file) as json_data:
        data = json.load(json_data)
    return data

def get_photos(celeb_dict):
    """
    :param celeb_dict: (dict) {'celeb name': ['url of celeb photo']}
    :return photos_dict: (dict) {'celeb name': 'celeb_name.jpg'}
    """
    photos_dict = {}
    for key, elem in celeb_dict.items():
        celeb_name = '_'.join(key.lower().split(' ')) + '.jpg'
        photos_dict[key] = celeb_name
        subprocess.check_output(['wget', elem[0], '-O', './images/{}'.format(photos_dict[key])])
        subprocess.call(['rm', elem[0].split('/')[-1]]) #.jpg has been renamed and moved to /images...deletes the original

        time.sleep(.4)
        print('sleeping after downloading {}'.format(key))







print(get_photos(get_links_from_json('celeb_img_links.json')))

if __name__ == '__main__':
    pass

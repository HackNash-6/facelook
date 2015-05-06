__author__ = 'chrisgraff'

import os
import time
import json
import subprocess
import collections


# TODO: Write a function to check whether celeb photo already exists
# TODO: save img to gender-specific dir based on the last val in celeb listing - {name: [celeb_page, img_url, is_girl]}


def check_img_inventory(dir_name):
    """
    :param dir_name: (string) name of target dir
    :return: (set) names of celebs we already have
    """
    file_names = os.listdir(dir_name)
    return set(n.replace('_', ' ') for n in ''.join(file_names).split('.jpg')[2:])


def detect_img_duplicates(dir_name):
    """
    :param dir_name: (string) name of target dir
    :return: (list) list of duplicate filenames
    """
    file_names = os.listdir(dir_name)
    return [x for x, y in collections.Counter(file_names).items() if y > 1]



def get_links_from_json(json_file):
    """
    :param json_file: (string) 'whatever.json'
    :return: (dict) converted data from json file
    """
    with open(json_file) as json_data:
        data = json.load(json_data)
    return data


def get_photos(celeb_dict):
    """
    :param celeb_dict: (dict) {'name': ['celeb page url (eg /name/nm1234)', 'celeb img url (eg http://..)', is_girl]}
    :return photos_dict: (dict) {'celeb name': 'celeb_name.jpg'}
    """
    photos_dict = {}
    inventory = check_img_inventory()
    for key, elem in celeb_dict.items():
        if key not in inventory:
            celeb_name = '_'.join(key.lower().split(' ')) + '.jpg'
            photos_dict[key] = celeb_name
            subprocess.check_output(['wget', elem[1], '-O', './images/{}'.format(photos_dict[key])])
            time.sleep(.6)
            print('sleeping after downloading {}'.format(key))


def test_get_photos(dict_to_be_tested=None):
    """
    :param dict_to_be_tested: (dict)
    :return: (string) - "pass" or "fail"
    :comment: Checks the round-trip of json.dump/json.loads....Was valid json created & successfully loaded?
    """
    if dict_to_be_tested is not None:
        test_dict = dict_to_be_tested
    else:
        test_dict = {'example_name': 'example_value'}

    with open('test.json', 'w') as outfile:
        json.dump(test_dict, outfile, indent=4)

    with open('test.json') as infile:
        test_data = json.load(infile)

    if test_data:
        subprocess.call(['rm', 'test.json']) #deletes the recently created file
        return 'Pass...Test returns the data: {}'.format(test_data)
    else:
        #'test.json' is preserved for inspection
        return 'Fail...No data returned'


# Uncomment the following to test validity of celeb_img_links.json:
# print(test_get_photos(get_links_from_json('celeb_img_links.json')))
print(detect_img_duplicates('images'))


if __name__ == '__main__':
    pass
    #get_photos(get_links_from_json('celeb_links/new_celeb_img_links1.json'))

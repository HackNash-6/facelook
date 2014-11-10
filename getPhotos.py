__author__ = 'chrisgraff'

import time
import json
import subprocess


def get_links_from_json(json_file):
    """
    :param json_file: (string) 'whatever.json'
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
        subprocess.check_output(['wget', elem[0], '-O', './images/{}'.format(photos_dict[key])]) #download the file
        subprocess.call(['rm', elem[0].split('/')[-1]]) # jpg renamed/moved to images...deletes the original

        time.sleep(.4)
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


if __name__ == '__main__':
    get_photos(get_links_from_json('celeb_img_links.json'))

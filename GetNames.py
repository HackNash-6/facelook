__author__ = 'Jack'
import requests

def getNames():
    allNames = requests.get('http://www.people.com/people/celebrities/')
    html = allNames.text
    print(html)

getNames()
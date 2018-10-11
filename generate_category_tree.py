#!/usr/bin/env python3

import sys
import json
import unicodedata
import re
import pathlib

CATSEP = ' --- ' # separator for category and its description in the directory name
DIRSEP = '/'     # directory path separator

def slugify(value, allow_unicode=False):
    """
    Taken from the Django Project. BSD-style license:
    https://github.com/django/django/blob/master/LICENSE
    https://github.com/django/django/blob/master/django/utils/text.py

    Based on this SO post:
    https://stackoverflow.com/questions/295135/
    """
    """
    Convert to ASCII if 'allow_unicode' is False.  Remove characters that
    aren't alphanumerics, underscores, spaces, or hyphens.  Convert to
    lowercase (currently disabled) . Also strip leading and trailing
    whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    #value = re.sub(r'[^\w\s-]', '', value).strip()#.lower()
    #return re.sub(r'[-\s]+', ' ', value).strip()
    # Strip trailing period because Windows is fucking stupid.
    # https://superuser.com/questions/585097/
    value = re.sub(r'\.$', '', value)
    value = re.sub(r'\.\s{2,}', '. ', value)
    return re.sub(r':',' -', value).strip()

def loadJSON(filepath):
    with open(filepath) as JSONFile:
        JSONData = json.load(JSONFile)
    return JSONData

def generatePaths(JSONData):
    path_list = []
    for node in JSONData:
        path = slugify(node['id']) + CATSEP + slugify(node['subject'])
        for parent_node_subj in reversed(node['parentsSubjects']):
            parent_node_subj = slugify(re.sub(r'\[', '', parent_node_subj))
            parent_node_subj = re.sub(r'\]\s', CATSEP, parent_node_subj)
            path = parent_node_subj + DIRSEP + path
        path_list.append(path)
    return path_list

def generateDirs(path_list, out_dir):
    for path in path_list:
        path = slugify(out_dir + DIRSEP + path, allow_unicode=True)
        pathlib.Path(path).mkdir(parents = True, exist_ok = True)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("USAGE: \n" + str(sys.argv[0]) + ' [JSON file] [out directory]')

    if (len(sys.argv) == 3):
        out_dir = str(sys.argv[2])
    else:
        out_dir = '.'

    JSONData = loadJSON(sys.argv[1])
    path_list = generatePaths(JSONData['nodes'])
    generateDirs(path_list, out_dir)

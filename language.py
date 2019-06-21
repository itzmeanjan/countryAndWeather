#!/usr/bin/python3

from requests import get
from json import dumps


def build(target_file='language.json'):
    code = {'error': 'incomplete'}
    try:
        with open(target_file, mode='w') as fd:
            fd.write(dumps([{'iso3': lang[0], 'iso': lang[2], 'name': lang[3]} for lang in (line.split('\t') for line in get('http://download.geonames.org/export/dump/iso-languagecodes.txt').text.split(
                '\n')[1:-1])], indent=4, ensure_ascii=False))
        code = {'success': 'true'}
    except Exception as e:
        code = {'error': str(e)}
    return code


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

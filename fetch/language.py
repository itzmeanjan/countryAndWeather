#!/usr/bin/python3

from requests import get
from json import dumps
from os.path import join, abspath, dirname, exists
from os import mkdir


def build(target_file=abspath(join(dirname(__file__), '../data/language.json'))):
    '''
        Builds language info dataset.

        First it fetches data from GeoNames data dumping site, then processes text data and converts to JSON. Finally stores it in provided file `/data/language.json`.

        In success returns
            `{'success': 'true'}`
        else 
            `{'error': ' ... '}`

    '''
    code = {'error': 'incomplete'}
    try:
        if(not exists(dirname(target_file))):
            # creates target data store directory, if that doesn't exists already
            mkdir(dirname(target_file))
        with open(target_file, mode='w') as fd:
            fd.write(dumps([{'iso3': lang[0], 'iso': lang[2], 'name': lang[3]} for lang in (line.split('\t') for line in get('http://download.geonames.org/export/dump/iso-languagecodes.txt').text.split(
                '\n')[1:-1])], indent=4, ensure_ascii=False))
        code = {'success': 'true'}
    except Exception as e:
        code = {'error': str(e)}
    return code


if __name__ == '__main__':
    try:
        print(build())
    except KeyboardInterrupt:
        print('\n[!]Terminated :/')
    finally:
        exit(0)

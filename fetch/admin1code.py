#!/usr/bin/python3

from requests import get
from json import dump
from os.path import abspath, join, dirname, exists
from os import mkdir


def fetchIt(target_file: str = abspath(join(dirname(__file__), '../data/admin1Code.json'))) -> bool:
    status = False
    try:
        if(not exists(dirname(target_file))):
            mkdir(dirname(target_file))
        with open(target_file, 'w') as fd:
            dump(
                [{'admin1Code': code[0], 'name': code[1]} for code in (line.split('\t') for line in get(
                    'http://download.geonames.org/export/dump/admin1CodesASCII.txt').text.split('\n')[:-1])],
                fd,
                ensure_ascii=False,
                indent=4
            )
        status = True
    except Exception as e:
        status = False
    finally:
        return status


if __name__ == '__main__':
    print(fetchIt())
    #print('[!]This module is expected to be used as a backend handler')
    exit(0)

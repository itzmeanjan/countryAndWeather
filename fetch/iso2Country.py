#!/usr/bin/python3

from __future__ import annotations
from sys import path
from os.path import abspath, dirname, join
from json import dump
path.append(abspath(join(dirname(__file__), '../')))
try:
    from model.country import CountryList, importIt as importCountryList
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def generate(target_file=abspath(join(dirname(__file__), '../data/iso2Country.json'))) -> bool:
    '''
        Function helps in generating a JSON file, storing ISO2CountryName mapping,
        which is to be used in one dependent project https://github.com/itzmeanjan/weatherz-desktop
    '''
    target = False
    try:
        countryList = importCountryList()
        if(countryList):
            with open(target_file, mode='w') as fd:
                dump(
                    dict((elem.iso, elem.country)
                         for elem in countryList.allCountry),
                    fd,
                    ensure_ascii=False,
                    indent=4)
            target = True
    except Exception:
        target = False
    finally:
        return target


if __name__ == '__main__':
    try:
        print('Success' if generate() else 'Failure')
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)

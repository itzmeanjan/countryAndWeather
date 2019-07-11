#!/usr/bin/python3

from __future__ import annotations
from os.path import abspath, join, dirname
from sys import path
from json import dump
path.append(abspath(join(dirname(__file__), '../')))
try:
    from model.country import CountryList, importIt as importCountryList
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(0)


def generate(target_file=abspath(join(dirname(__file__), '../data/iso3_2_iso2.json'))) -> bool:
    target = False
    try:
        countryList = importCountryList()
        if(countryList):
            with open(target_file, mode='w') as fd:
                dump(dict((elem.iso3, elem.iso)
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

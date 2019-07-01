#!/usr/bin/python3

from __future__ import annotations
from typing import Dict
from requests import get
from json import dumps
from os.path import join, abspath, dirname, exists, realpath
from os import mkdir


def build(target_file: str = abspath(join(dirname(realpath(__file__)), '../data/country.json'))) -> Dict[str, str]:
    '''
        Builds country info dataset.

        First it fetches data from GeoNames data dumping site, then processes text data and converts to JSON. Finally stores it in provided file `/data/country.json`.

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
            fd.write(dumps(
                {
                    'countries': [{'iso': country[0], 'iso3': country[1], 'isoNumeric': country[2], 'fips': country[3], 'country': country[4], 'capital': country[5], 'area(in sq km)': country[6], 'population': country[7], 'continent': country[8], 'tld': country[9], 'currencyCode': country[10], 'currencyName': country[11], 'phone': country[12], 'postalFormat': country[13], 'postalRegex': country[14], 'languages': country[15].split(','), 'geonameid': country[16], 'neighbours': country[17].split(','), 'equivalentFips': country[18]} for country in (line.split('\t') for line in get(
                        'http://download.geonames.org/export/dump/countryInfo.txt').text.split('\n') if(line and (not line.startswith('#'))))]
                }, indent=4, ensure_ascii=False))
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

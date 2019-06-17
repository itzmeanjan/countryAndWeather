#!/usr/bin/python3

from requests import get
from json import dumps


def build(target_file='country.json'):
    code = ''
    try:
        with open(target_file, mode='w') as fd:
            fd.write(dumps([{'iso': country[0], 'iso3': country[1], 'isoNumeric': country[2], 'fips': country[3], 'country': country[4], 'capital': country[5], 'area(in sq km)': country[6], 'population': country[7], 'continent': country[8], 'tld': country[9], 'currencyCode': country[10], 'currencyName': country[11], 'phone': country[12], 'postalFormat': country[13], 'postalRegex': country[14], 'languages': country[15].split(','), 'geonameid': country[16], 'neighbours': country[17].split(','), 'equivalentFips': country[18]} for country in (line.split('\t') for line in get(
                'http://download.geonames.org/export/dump/countryInfo.txt').text.split('\n') if(line and (not line.startswith('#'))))], indent=4))
        code = 'Success'
    except Exception as e:
        code = str(e)
    return code


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

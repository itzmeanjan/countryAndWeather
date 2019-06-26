#!/usr/bin/python3

from __future__ import annotations
from typing import Dict
try:
    from os.path import dirname, abspath, join, realpath
    from sys import path
    path.append(abspath(join(dirname(realpath(__file__)), '../')))
    from model.country import Country, CountryList, importIt
    from fetch.place import getAll
except ImportError as e:
    print('[!]Error : {}'.format(str(e)))
    exit(1)


def bringIn(base_url: str = 'http://download.geonames.org/export/dump/{}.zip') -> Dict(str, str):
    '''
        Reads Country data from downloaded JSON files and objectifies those
        Then fetches each country specific places record from generated URL
        Processes those places data and JSONifies those and stores in seperate file for each Country

        In success returns 
            {'success': 'true'}
        else
            {'error': ' ... '}

    '''
    status = {'error': 'incomplete'}
    try:
        countryList: CountryList = importIt()
        if(not countryList):
            status['error'] = 'failed'
        else:
            for i in countryList.allCountry:
                result = getAll(iso=i.iso, country=i.country,
                                url=base_url.format(i.iso.upper()), target_file=abspath(join(dirname(__file__), '../data/{}.json'.format(i.iso.upper()))), countryListObj=countryList)
                if(result.get('success', '') != 'true'):
                    status = {'success': 'false'}
                    break
                print(
                    '[+]{} ({}) --> {}'.format(i.country, i.iso, result))
            else:
                status = {'success': 'true'}
    except Exception as e:
        status['error'] = str(e)
    finally:
        return status


if __name__ == '__main__':
    try:
        print(bringIn())
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)

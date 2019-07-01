#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict
from json import dump
from sys import path
from os.path import abspath, join, dirname
path.append(abspath(join(dirname(__file__), '../')))
try:
    from model.place import Place, PlaceList, importIt as placeListImport
    from model.country import CountryList, importIt as countryListImport
except ImportError as e:
    print('[!]Error : {}'.format(str(e)))
    exit(1)


def __handle_country__(placeListObj: PlaceList) -> List[Dict[str, str]]:
    '''
        Handles all places record under a certain country
        Returns a list of those places which are eligible for receiving weather foecast

        In case of error, returns a blank list
    '''

    def __validate__(placeObj: Place) -> bool:
        '''
            Validates whether this certain place record is eligible for receiving weather forecast or not
        '''
        return True if(
            placeObj.name and placeObj.country and placeObj.admin1Code and placeObj.admin2Code) else False

    if(not placeListObj):
        return []

    try:
        return [{'name': elem.name, 'url': 'http://yr.no/place/{}/{}/{}/forecast.xml'.format('_'.join(elem.country.strip(' ').split(' ')), '_'.join(elem.admin1Code.strip(' ').split(' ')), '_'.join(elem.admin2Code.strip(' ').split(' ')))}
                for elem in placeListObj.places if (__validate__(elem))]  # URL generation is done here
    except Exception:
        return []


def eligiblePlaceNames() -> bool:
    '''
        Iterates over all place records, country by country, and returns boolean value to denote success or failure of desired operation

        This will extract out all those places name and url, and store in JSON file for individual countries
    '''
    target = False
    try:
        countryListObj = countryListImport()
        if(not countryListObj):
            raise Exception('Failed to fetch Country List')
        for elem in countryListObj.allCountry:
            with open(abspath(
                    join(
                        dirname(__file__),
                        '../data/weather{}.json'.format(elem.iso.upper())
                    )), mode='w') as fd:
                dump(
                    {
                        'places': __handle_country__(placeListImport(
                            abspath(join(dirname(__file__), '../data/{}.json'.format(elem.iso.upper())))))
                    },
                    fd,
                    ensure_ascii=False,
                    indent=4
                )
            print(
                '[+]{} ({}) -- `success`'.format(elem.country.capitalize(), elem.iso.upper()))
        else:
            target = True
    except Exception as e:
        target = False
    finally:
        return target


if __name__ == '__main__':
    try:
        print(
            'Success' if eligiblePlaceNames() else 'Failure'
        )
    except KeyboardInterrupt as e:
        print('\n[!]Terminated')
    finally:
        exit(0)

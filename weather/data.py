#!/usr/bin/python3

from __future__ import annotations
from sys import path
from os.path import abspath, join, dirname
path.append(abspath(join(dirname(__file__), '../')))
try:
    from model.weatherPlaces import EligiblePlaceList, importIt as eligiblePlaceListImport
    from model.country import CountryList, importIt as countryListImport
except ImportError as e:
    print('[!]Error : {}'.format(str(e)))
    exit(1)


def getIt() -> bool:
    '''
        Reads all eligible place records from corresponding data files and converts them to Python Object,
        which will be used to fetch weather data from Yr.no
    '''
    target = False
    try:
        countryListObj = countryListImport()
        if(not countryListObj):
            raise Exception('Failed to fetch country details')
        count: int = 0
        for elem in countryListObj.allCountry:
            eligiblePlaceListObj = eligiblePlaceListImport(
                abspath(
                    join(
                        dirname(
                            __file__
                        ),
                        '../data/weather{}.json'.format(elem.iso.upper())
                    )
                )
            )
            if(not eligiblePlaceListObj):
                continue
            for innerElem in eligiblePlaceListObj.places:
                count += 1
                print('{} |:| {} -- {}'.format(count,
                                               innerElem.name, innerElem.url))
        else:
            target = True
    except Exception:
        target = False
    finally:
        return target


if __name__ == '__main__':
    try:
        print('Success' if getIt() else 'Failure')
    #print('[!]This module is expected to be used as a backend handler')
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)

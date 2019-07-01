#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, List
from json import loads
from os.path import abspath, dirname, join, realpath


class Country:
    '''
        This class will hold information about a certain country
    '''

    def __init__(self, iso: str, country: str):
        self.iso = iso
        self.country = country

    @staticmethod
    def fromJson(data: Dict[str, str]) -> Country:
        '''
            Builds a Country object from deserialized JSON data i.e. Dict<K, V>
        '''
        _country = Country(*[None]*2)
        for key, value in data.items():
            if(key == 'iso'):
                _country.iso = value
            elif(key == 'country'):
                _country.country = value
        return _country


class CountryList:
    '''
        Holds record of all countries, helps in enquiring country record by using several properties ( though currently only ISO ;) )
    '''

    def __init__(self, allCountry: List[Country]):
        self.allCountry = allCountry

    def getCountryByISO(self, iso: str) -> Country:
        '''
            Gets record of a country by its ISO2 code.

            If no record is found, simply returns None.
        '''
        target = None
        if(not iso):
            return target
        for i in self.allCountry:
            if(i.iso == iso):
                target = i
                break
        return target

    @staticmethod
    def fromJson(data: List[Dict[str, str]]) -> CountryList:
        '''
            Builds a CountryList object from deserialized JSON data i.e. List<Dict<K, V>>
        '''
        _countryList = CountryList([])
        for i in data:
            _countryList.allCountry.append(Country.fromJson(i))
        return _countryList


def importIt(target_file: str = abspath(join(dirname(realpath(__file__)), '../data/country.json'))) -> CountryList:
    '''
        Reads from JSON file and deserializes data back to python object
    '''
    try:
        with open(abspath(target_file), mode='r') as fd:
            return CountryList.fromJson(loads(fd.read()).get('countries', []))
    except Exception:
        return None


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')
    exit(0)

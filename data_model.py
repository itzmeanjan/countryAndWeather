#!/usr/bin/python3

from json import loads


class Country:
    '''
        This class will hold information for a certain country
    '''

    def __init__(self, iso, iso3, isoNumeric, fips, country, capital, area, population, continent, tld, currencyCode, currencyName, phone, postalFormat, postalRegex, languages, geonameId, neighbours, equivalentFips):
        self.iso = iso
        self.iso3 = iso3
        self.isoNumeric = isoNumeric
        self.fips = fips
        self.country = country
        self.capital = capital
        self.area = area
        self.population = population
        self.continent = continent
        self.tld = tld
        self.currencyCode = currencyCode
        self.currencyName = currencyName
        self.phone = phone
        self.postalFormat = postalFormat
        self.postalRegex = postalRegex
        self.languages = languages
        self.geonameId = geonameId
        self.neighbours = neighbours
        self.equivalentFips = equivalentFips

    @staticmethod
    def fromJson(data):
        _country = Country(*[None]*19)
        for key, value in data.items():
            if(key == 'iso'):
                _country.iso = value
            elif(key == 'iso3'):
                _country.iso3 = value
            elif(key == 'isoNumeric'):
                _country.isoNumeric = value
            elif(key == 'fips'):
                _country.fips = value
            elif(key == 'country'):
                _country.country = value
            elif(key == 'capital'):
                _country.capital = value
            elif(key == 'area'):
                _country.area = value
            elif(key == 'population'):
                _country.population = value
            elif(key == 'continent'):
                _country.continent = value
            elif(key == 'tld'):
                _country.tld = value
            elif(key == 'currencyCode'):
                _country.currencyCode = value
            elif(key == 'currencyName'):
                _country.currencyName = value
            elif(key == 'phone'):
                _country.phone = value
            elif(key == 'postalFormat'):
                _country.postalFormat = value
            elif(key == 'postalRegex'):
                _country.postalRegex = value
            elif(key == 'languages'):
                _country.languages = value
            elif(key == 'geonameid'):
                _country.geonameId = value
            elif(key == 'neighbours'):
                _country.neighbours = value
            elif(key == 'equivalentFips'):
                _country.equivalentFips = value
        return _country


class CountryList:
    def __init__(self, country):
        self.country = country


def importIt(target_file='country.json'):
    '''
        Reads from JSON file and deserializes data back to python objects
    '''
    with open(target_file, mode='r') as fd:
        print(loads(fd.read()))


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

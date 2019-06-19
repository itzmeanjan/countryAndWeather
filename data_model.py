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
        '''
            Builds a Country object from deserialized JSON data i.e. Dict<K, V>
        '''
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
    '''
        Holds record of all countries, helps in enquiring country record by using several properties
    '''

    def __init__(self, allCountry):
        self.allCountry = allCountry

    def getCountryByISO(self, iso):
        '''
            Gets record of a country by its ISO2 code.

            If no record is found, simply returns None.
        '''
        target = None
        for i in self.allCountry:
            if(i.iso == iso):
                target = i
                break
        return target

    @staticmethod
    def fromJson(data):
        '''
            Builds a CountryList object from deserialized JSON data i.e. List<Dict<K, V>>
        '''
        _countryList = CountryList([])
        for i in data:
            _countryList.allCountry.append(Country.fromJson(i))
        for i in _countryList.allCountry:
            i.neighbours = [_countryList.getCountryByISO(
                j) for j in i.neighbours]  # fetches Country record from already processed CountryList in puts in neighbours list
        return _countryList


def importIt(target_file='country.json'):
    '''
        Reads from JSON file and deserializes data back to python objects
    '''
    with open(target_file, mode='r') as fd:
        return CountryList.fromJson(loads(fd.read()))


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

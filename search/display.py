#!/usr/bin/python3

from re import compile as reg_compile, I as case_insensitive


def getContinentCodeToName(code: str) -> str:
    regex = reg_compile(r'^({0})$'.format(code), flags=case_insensitive)
    target = None
    for key, value in {'as': 'Asia', 'na': 'North America', 'sa': 'South America', 'eu': 'Europe', 'oc': 'Ociania', 'an': 'Antertica'}.items():
        if(regex.match(key)):
            target = value
            break
    return target


def showIt(countryData):
    print('\n\t[+]Country Name : {0}\n\t[+]ISO Code : {1}\n\t[+]ISO3 Code : {2}\n\t[+]ISO Numeric Code : {3}\n\t[+]FIPS Code : {4}\n\t[+]Capital : {5}\n\t[+]Area( in sq. km ) : {6}\n\t[+]Population : {7}\n\t[+]Continent : {8}\n\t[+]Top Level Domain : {9}\n\t[+]Currency : {10}( {11} )\n'.format(
        countryData.country, countryData.iso, countryData.iso3, countryData.isoNumeric, countryData.fips, countryData.capital, countryData.area, countryData.population, getContinentCodeToName(countryData.continent), countryData.tld, countryData.currencyName, countryData.currencyCode))


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

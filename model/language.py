#!/usr/bin/python3

from __future__ import annotations
from json import loads
from os.path import abspath, dirname, join


class Language:
    '''
        This class will hold information about a certain langauge
    '''

    _countrySpecific = ''

    def __init__(self, iso3, iso, name):
        self.iso3 = iso3
        self.iso = iso
        self._name = name

    @property
    def name(self):
        if(self._countrySpecific):
            return '{}-{}'.format(self._name, self._countrySpecific)
        else:
            return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def countrySpecific(self):
        return self._countrySpecific

    @countrySpecific.setter
    def countrySpecific(self, value):
        self._countrySpecific = value

    @staticmethod
    def fromJson(data):
        '''
            Builds a Language object from deserialized JSON data i.e. Dict<K, V>
        '''
        _language = Language(*[None]*3)
        for key, value in data.items():
            if(key == 'iso3'):
                _language.iso3 = value
            elif(key == 'iso'):
                _language.iso = value
            elif(key == 'name'):
                _language.name = value
        return _language

    @staticmethod
    def copyFrom(language: Language, countrySpecific: str) -> Language:
        '''
            Returns an object of Language class, while setting countrySpecific argument passed to it and retaining all other properties

            Can be helpful while handling ISO language code, having country name in it
        '''
        _lang = Language(*[None]*3)
        _lang.iso3 = language.iso3
        _lang.iso = language.iso
        _lang.name = language.name
        _lang.countrySpecific = countrySpecific
        return _lang


class LanguageList:
    '''
        Holds record of all languages, helps in enquiring language record by using several properties
    '''

    def __init__(self, allLanguage):
        self.allLanguage = allLanguage

    def getLanguageByISO(self, iso):
        '''
            Gets record of a language by its ISO code.

            If no record is found, simply returns None.
        '''
        target = None
        if(not iso):
            return target
        for i in self.allLanguage:
            if(i.iso == iso):
                target = i
                break
        return target

    def getLanguageByISO3(self, iso3):
        '''
            Gets record of a language by its ISO3 code.

            If no record is found, simply returns None.
        '''
        target = None
        if(not iso3):
            return target
        for i in self.allLanguage:
            if(i.iso3 == iso3):
                target = i
                break
        return target

    @staticmethod
    def fromJson(data):
        '''
            Builds a LanguageList object from deserialized JSON data i.e. List<Dict<K, V>>
        '''
        _languageList = LanguageList([])
        for i in data:
            _languageList.allLanguage.append(Language.fromJson(i))
        return _languageList


def importIt(target_file=abspath(join(dirname(__file__), '../language.json'))):
    '''
        Reads from JSON file and deserializes data back to python objects
    '''
    try:
        with open(target_file, mode='r') as fd:
            return LanguageList.fromJson(loads(fd.read()).get('languages', []))
    except Exception:
        return None


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

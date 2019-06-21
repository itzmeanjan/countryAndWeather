#!/usr/bin/python3

from sys import argv
from country import build
from model.country import importIt as countryImport
from model.language import importIt as languageImport
from model.language import Language


def __argument_fetcher__():
    args = {}
    if(argv[1] == 'build'):
        args = {'args': ['build']}
    return args


def __show_usage__():
    print('[+]Usage ::\n\n\tBuild Country Info : country build\n'.format(argv[0]))
    return


def __merge__():
    countryData = countryImport()
    languageData = languageImport()
    if((not countryData) or (not languageData)):
        return None
    for i in countryData.allCountry:
        i.languages = [None if(len(j) == 0) else languageData.getLanguageByISO(
            j.lower()) if(len(j) == 2) else languageData.getLanguageByISO3(j.lower()) if(len(j) == 3) else Language.copyFrom(languageData.getLanguageByISO(
                j[:2].lower()), countryData.getCountryByISO(j[3:]).country) for j in i.languages]
    return countryData


def app():
    if(len(argv) != 2):
        __show_usage__()
        return
    args = __argument_fetcher__().get('args', [])
    if(args and args[0] == 'build'):
        result = build()
        if(result.get('success', 'false') == 'true'):
            print('[+]Success !!!')
        else:
            print('[!]Error : {}'.format(result.get('error', ':/')))
    else:
        __show_usage__()
    return


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated !!!')
    finally:
        exit(0)

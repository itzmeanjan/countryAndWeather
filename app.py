#!/usr/bin/python3

from sys import argv
from country import build as country_build
from language import build as language_build
from model.country import importIt as countryImport
from model.language import importIt as languageImport
from model.language import Language
from search.iso import findIt as findByISO
from search.display import showIt


def __argument_fetcher__():
    args = {}
    if(argv[1] == 'build-country'):
        args = {'args': argv[1:]}
    elif(argv[1] == 'build-language'):
        args = {'args': argv[1:]}
    elif(argv[1] == 'search' and argv[2] == '--iso'):
        args = {'args': argv[1:]}
    return args


def __show_usage__():
    print('[+]Usage ::\n\n\tBuild Country Info :\n\t\t>> country build-country\n\n\tBuild Language Info :\n\t\t>> country build-language\n\n\tSearch Country by ISO Code :\n\t\t>> country search --iso `search keyword`\n\n'.format(argv[0]))
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
    if(len(argv) != 2 and len(argv) != 4):
        __show_usage__()
        return
    args = __argument_fetcher__().get('args', [])
    if(args):
        if(args[0] == 'build-country'):
            result = country_build()
            if(result.get('success', 'false') == 'true'):
                print('[+]Success !!!')
            else:
                print('[!]Error : {}'.format(result.get('error', ':/')))
        elif(args[0] == 'build-language'):
            result = language_build()
            if(result.get('success', 'false') == 'true'):
                print('[+]Success !!!')
            else:
                print('[!]Error : {}'.format(result.get('error', ':/')))
        elif(args[0] == 'search' and args[1] == '--iso'):
            result = findByISO(__merge__(), keyword=args[2])
            if(result):
                showIt(result)
            else:
                print('[!] No result found :/')
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

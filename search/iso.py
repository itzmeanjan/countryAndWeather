#!/usr/bin/python3

from re import compile as reg_compile, I as ignore_case


def findIt(data, keyword: str = ''):
    if(len(keyword) > 2):
        return None
    elif(len(keyword) < 2):
        return None
    else:
        regex = reg_compile(r'^({0})$'.format(keyword), flags=ignore_case)
        target = None
        for i in data.allCountry:
            if(regex.match(i.iso)):
                target = i
                break
        return target


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')

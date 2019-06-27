#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, List
from json import loads
from os.path import abspath, dirname, join


class Admin2Code:
    '''
        Holds record of certain place's admin code level 2
        Record stored using two elements code, which is period seperated and name of place
    '''

    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    @staticmethod
    def fromJSON(data: Dict(str, str)) -> Admin2Code:
        '''
            Reads data from JSON, actually a python dict object and returns a Admin2Code object
        '''
        admin2Code = Admin2Code(*[None]*2)
        admin2Code.code = data.get('admin2Code')
        admin2Code.name = data.get('name')
        return admin2Code


class Admin2CodeList:
    '''
        Holds a collection of Admin2Code object, where each one of them pointing to a record
    '''

    def __init__(self, codes: List(Admin2Code)):
        self.codes = codes

    def getRecordByCode(self, code: str) -> Admin2Code:
        '''
            Searches for a record using its unique identifier code
        '''
        target: Admin2Code = None
        for elem in self.codes:
            if(elem.code == code.upper()):
                target = elem
                break
        return target

    @staticmethod
    def fromJSON(data: List(Dict(str, str))) -> Admin2CodeList:
        '''
            Reads from JSON and converts to Admin2CodeList object, which is eventaully returned
        '''
        admin2CodeList = Admin2CodeList([])
        for elem in data:
            admin2CodeList.codes.append(
                Admin2Code.fromJSON(elem)
            )
        return admin2CodeList


def importIt(target_file: str = abspath(join(dirname(__file__), '../data/admin2Code.json'))) -> Admin2CodeList:
    '''
        Use this function to convert a JSON file, full of admin code level 2 records, into Admin2CodeList object,
        which can be eventually used to query for a certain record using code

        In case of error, returns None, so be careful when using it
    '''
    try:
        with open(target_file, 'r') as fd:
            return Admin2CodeList.fromJSON(
                loads(fd.read())
            )
    except Exception as e:
        return None


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')
    exit(0)

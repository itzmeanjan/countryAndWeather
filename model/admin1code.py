#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, List
from json import loads
from os.path import abspath, dirname, join


class Admin1Code:
    '''
        Holds record of certain place's admin code level 1
        Record stored using two elements code, which is period seperated and name of place
    '''

    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    @staticmethod
    def fromJSON(data: Dict(str, str)) -> Admin1Code:
        '''
            Reads data from JSON, actually a python dict object and returns a Admin1Code object
        '''
        admin1Code = Admin1Code(*[None]*2)
        admin1Code.code = data.get('admin1Code')
        admin1Code.name = data.get('name')
        return admin1Code


class Admin1CodeList:
    '''
        Holds a collection of Admin1Code object, where each one of them pointing to a record
    '''

    def __init__(self, codes: List(Admin1Code)):
        self.codes = codes

    def getRecordByCode(self, code: str) -> Admin1Code:
        '''
            Searches for a record using its unique identifier code
        '''
        target: Admin1Code = None
        for elem in self.codes:
            if(elem.code == code.upper()):
                target = elem
                break
        return target

    @staticmethod
    def fromJSON(data: List(Dict(str, str))) -> Admin1CodeList:
        '''
            Reads from JSON and converts to Admin1CodeList object, which is eventaully returned
        '''
        admin1CodeList = Admin1CodeList([])
        for elem in data:
            admin1CodeList.codes.append(
                Admin1Code.fromJSON(elem)
            )
        return admin1CodeList


def importIt(target_file: str = abspath(join(dirname(__file__), '../data/admin1Code.json'))) -> Admin1CodeList:
    '''
        Use this function to convert a JSON file, full of admin code level 1 records, into Admin1CodeList object,
        which can be eventually used to query for a certain record using code

        In case of error, returns None, so be careful when using it
    '''
    try:
        with open(target_file, 'r') as fd:
            return Admin1CodeList.fromJSON(
                loads(fd.read()).get('codes', [])
            )
    except Exception as e:
        return None


if __name__ == '__main__':
    print('[!]This module is expected to be used as a back end handler')
    exit(0)

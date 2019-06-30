#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, List
from json import load


class EligiblePlace:
    '''
        Holds record of a certain place, which is eligible to get weather data

        These data set is exported from ../data/weatherXX.json files, where XX denotes ISO country code

        Every record will hold place name and its corresponding URL, for fetching weather data
    '''

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    @staticmethod
    def fromJson(data: Dict[str, str]) -> EligiblePlace:
        '''
            This statis method will help to convert a Dict(str, str) object, holding place record, into EligiblePlace object
        '''
        eligiblePlace = EligiblePlace(*[None]*2)
        eligiblePlace.name = data.get('name', '')
        eligiblePlace.url = data.get('url', '')
        return eligiblePlace


class EligiblePlaceList:
    '''
       Holds a list of EligiblePlace objects, where each of them will hold record of certain place, eligible to receive weather update
    '''

    def __init__(self, places: List[EligiblePlace]):
        self.places = places

    @staticmethod
    def fromJson(data: List[Dict[str, str]]) -> EligiblePlaceList:
        '''
            This method will help you to convert a List(Dict(str, str)) into EligiblePlaceList object

            While invoking method, make sure you decode JSON object into python object and send to this method as argument
        '''
        eligiblePlaceList = EligiblePlaceList([])
        for elem in data:
            eligiblePlaceList.places.append(
                EligiblePlace.fromJson(elem)
            )
        return eligiblePlaceList


def importIt(target_file: str) -> EligiblePlaceList:
    '''
        You'll mostly invoke this function from outside to read a JSON file and convert its content into a handy EligiblePlaceList object
    '''
    targetObj = None
    try:
        with open(target_file, mode='r') as fd:
            targetObj = EligiblePlaceList.fromJson(load(fd))
    except Exception:
        targetObj = None
    finally:
        return targetObj


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)

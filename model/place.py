#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict
from os.path import dirname, abspath, join
from json import load


class Place:
    '''
        Holds record of a certain Place, will be used to import data set and then extract weather query url from it
    '''

    def __init__(self, name: str, country: str, admin1Code: str, admin2Code: str):
        self.name = name
        self.country = country
        self.admin1Code = admin1Code
        self.admin2Code = admin2Code

    @staticmethod
    def fromJson(data: Dict[str, str]) -> Place:
        '''
            Takes a JSON object i.e. python form of JSON object, and returns an intance of Place class, holding information of this place
        '''
        place = Place(*[None]*4)
        for key, value in data.items():
            if(key == 'name'):
                place.name = value
            elif(key == 'country'):
                place.country = value
            elif(key == 'admin1Code'):
                place.admin1Code = value
            elif(key == 'admin2Code'):
                place.admin2Code = value
            else:
                pass
        return place


class PlaceList:
    '''
        Holds a list of Place objects i.e. record of all places present in a certain country
    '''

    def __init__(self, places: List[Place]):
        self.places = places

    @staticmethod
    def fromJson(data: List[Dict[str, str]]) -> PlaceList:
        '''
            Converts JSON to PlaceList object
        '''
        placeList = PlaceList([])
        for item in data:
            placeList.places.append(Place.fromJson(item))
        return placeList


def importIt(target_file: str) -> PlaceList:
    '''
        Reads place records from JSON file and returns one PlaceList object from it

        In case of error, returns None
    '''
    placeListObj = None
    try:
        with open(target_file, mode='r') as fd:
            placeListObj = PlaceList.fromJson(
                load(fd).get('places', [])
            )
    except Exception as e:
        placeListObj = None
    finally:
        return placeListObj


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)

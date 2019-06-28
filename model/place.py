#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict
from os.path import dirname, abspath, join
from json import load


class Place:
    def __init__(self, name: str, country: str, admin1Code: str, admin2Code: str):
        self.name = name
        self.country = country
        self.admin1Code = admin1Code
        self.admin2Code = admin2Code

    @staticmethod
    def fromJson(data: Dict(str, str)) -> Place:
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
    def __init__(self, places: List(Place)):
        self.places = places

    @staticmethod
    def fromJson(data: List(Dict(str, str))) -> PlaceList:
        placeList = PlaceList([])
        for item in data:
            placeList.places.append(Place.fromJson(item))
        return placeList


def importIt(target_file=abspath(join(dirname(__file__), '../data/*.json'))) -> PlaceList:
    placeListObj = None
    try:
        with open(target_file, mode='r') as fd:
            placeListObj = PlaceList.fromJson(
                load(fd)
            )
    except Exception as e:
        placeListObj = None
    finally:
        return placeListObj


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)

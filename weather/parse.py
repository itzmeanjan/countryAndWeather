#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, Any, List
from requests import get
from dateutil import parser
from bs4 import BeautifulSoup, Tag
from os.path import exists
from json import dump


def __parseLocation__(element: Tag) -> Dict[str, Any]:
    return {
        'name': element.find('name').getText(),
        'type': element.find('type').getText(),
        'country': element.find('country').getText(),
        'tz': element.find('timezone').attrs,
        'loc': element.find('location').attrs
    }


def __parseMeta__(element: Tag) -> Dict[str, str]:
    return {
        'lastupdate': parser.parse(element.find('lastupdate').getText()).timestamp(),
        'nextupdate': parser.parse(element.find('nextupdate').getText()).timestamp()
    }


def __parseSunRiseAndSet(element: Tag) -> Dict[str, str]:
    return {
        'sunrise': parser.parse(element.find('sun').get('rise')).timestamp(),
        'sunset': parser.parse(element.find('sun').get('set')).timestamp()
    }


def __parseASingleForecast(element: Tag) -> Dict[str, Any]:

    def __parseTime__(data: Dict[str, str]) -> Dict[str, str]:
        data['from'] = parser.parse(data.get('from', '')).timestamp()
        data['to'] = parser.parse(data.get('to', '')).timestamp()
        return data

    return {
        'time': __parseTime__(element.attrs),
        'symbol': element.symbol.attrs,
        'precipitation': element.precipitation.get('value'),
        'winddirection': element.winddirection.attrs,
        'windspeed': element.windspeed.attrs,
        'temperature': element.temperature.attrs,
        'pressue': element.pressure.attrs
    }


def __parseAllForecast__(element: Tag) -> List[Dict[str, Any]]:
    return [
        __parseASingleForecast(item) for item in element.findAll('time')
    ]


def __deepParser__(data: str) -> Dict[str, Any]:
    '''
        Main data parsing from XML to Python Object is done here
    '''
    target = {}
    root = BeautifulSoup(data, 'lxml')
    target['location'] = __parseLocation__(root.find('location'))
    target['meta'] = __parseMeta__(root)
    target.update(__parseSunRiseAndSet(root))
    target['forecast'] = __parseAllForecast__(root.find('forecast'))
    return target


def parseIt(place: str, url: str) -> Dict[str, Any]:
    '''
        Fetches weather forecast data from provided URL and returns parsed data set, which can be easily JSONified
    '''
    target = None
    try:
        target = __deepParser__(get(url).text)
        '''
        with open('sample.json', mode='w') as fd:
            dump(target, fd, ensure_ascii=False, indent=4)
        '''
    except Exception:
        target = None
    finally:
        return target


if __name__ == '__main__':
    try:
        print(parseIt(
            'Bolpur', 'http://www.yr.no/place/India/West_Bengal/B%C4%ABrbh%C5%ABm/forecast.xml'))
    #print('[!]This module is expected to be used as a backend handler')
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)

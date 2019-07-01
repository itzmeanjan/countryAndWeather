#!/usr/bin/python3

from __future__ import annotations
from requests import get


def fetch(icon_id: str, target_file: str, template_url: str = 'http://yr.github.io/weather-symbols/png/100/{}.png') -> bool:
    '''
        This function will help you in fetching PNG Weather Icon from Yr.no,
        where a certain icon will be identified by its id, which is to be passed while invoking function.

        E.g. 10/ 05d/ 29m etc

        Example Usage: 
            >> icon.fetch('29m', '../data/29m.png')

        * You may not be interested in touching template_url parameter, which is having a default value.

        * Make sure you pass a target_file name, which is having `.png` extension.

        * If intended operation succeeds, will return True, else False

    '''
    target = False
    try:
        response = get(template_url.format(icon_id))
        if(response.status_code != 200):
            raise Exception('Response Code not okay')
        with open(target_file, mode='wb') as fd:
            fd.write(response.content)
        target = True
    except Exception:
        target = False
    finally:
        return target


if __name__ == '__main__':
    try:
        print('Success' if fetch(icon_id='29m',
                                 target_file='../data/29m.png') else 'Failure')
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)

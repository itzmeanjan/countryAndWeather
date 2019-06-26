#!/usr/bin/python3

from __future__ import annotations
from typing import Dict
from urllib.request import Request, urlopen
from http.client import HTTPResponse
from os.path import abspath, exists, join, dirname, realpath
from os import remove
from zipfile import ZipFile
from json import dumps
from sys import path
try:
    path.append(abspath(join(dirname(realpath(__file__)), '../')))
    from model.country import CountryList
except ImportError as e:
    print('[!]Error : {}'.format(str(e)))
    exit(1)


def __process__(data: str, target_file: str, countryListObj: CountryList) -> bool:
    '''
        Takes utf-8 string data, after processing and cleaning converts to JSON string,
        which finally gets stored in target file.

        Location of a certain place will be stored as a string -> `longitude,latitude`

        Returns status of operation as boolean
    '''
    status = False
    try:
        with open(target_file, mode='w') as fd:
            fd.write(
                dumps(
                    [{'geonameid': point[0], 'name': point[1], 'alternateNames': point[3].split(','), 'loc': '{},{}'.format(point[5], point[4]), 'featureClass': point[6], 'featureCode': point[7], 'country': countryListObj.getCountryByISO(point[8].upper()).country, 'cc2': [countryListObj.getCountryByISO(j.upper()).country for j in point[9].split(
                        ',') if(len(j) != 0)], 'admin1Code': point[10], 'admin2Code': point[11], 'admin3Code': point[12], 'admin4Code': point[13], 'population': point[14], 'elevation': point[15], 'tz': point[17]} for point in (line.split('\t') for line in data.split('\n')[:-1])],
                    ensure_ascii=False, indent=4
                )
            )
        status = True
    except Exception as e:
        pass
    finally:
        return status


def __decompressIt__(iso: str, tmp_file: str) -> bytes:
    '''
        Decompresses a Zip file and reads data as bytes from a certain file, present within that Zip
    '''
    data: bytes = bytes()
    try:
        fileName = None
        zipObj = ZipFile(tmp_file)
        for i in zipObj.infolist():
            if(i.filename == '{}.txt'.format(iso.upper())):
                fileName = i.filename
                break
        if(fileName):
            with zipObj.open(fileName) as fd:
                data = fd.read()
    except Exception as e:
        data = bytes()
    finally:
        return data


def __writeInto__(data: bytes, tmp_file: str) -> bool:
    '''
        Writes byte data into provided file
    '''
    status = False
    if(len(data) == 0):
        return status
    try:
        with open(tmp_file, mode='wb') as fd:
            fd.write(data)
        status = True
    except Exception as e:
        status = False
    finally:
        return status


def __readIt__(response: HTTPResponse) -> bytes:
    '''
        Reads data from HTTPResponse object and returns bytes
    '''
    data: bytes = bytes()
    amt: int = 1024
    tmp: bytes = bytes(amt)
    try:
        tmp = response.read(amt)
        if(tmp):
            while(len(tmp) != 0):
                data += tmp
                tmp = response.read(amt)
                if(tmp == None):
                    data = bytes()
                    break
    except Exception as e:
        data = bytes()
    finally:
        return data


def __get_data__(iso: str, request: Request, target_file: str, countryListObj: CountryList) -> bool:
    '''
        Does all heavy lifting for fetching places info and storing into JSON file,
        for a certain country
    '''
    returnVal = False
    try:
        response: HTTPResponse = urlopen(request)
        if(not response):
            pass
        elif(response.getcode() != 200):
            pass
        else:
            if(__writeInto__(data=__readIt__(response=response),
                             tmp_file=abspath('./tmp.zip'))):
                decompressed = __decompressIt__(
                    iso=iso, tmp_file=abspath('./tmp.zip')).decode()
                if(len(decompressed) != 0):
                    returnVal = __process__(
                        data=decompressed, target_file=target_file, countryListObj=countryListObj)
    except Exception as e:
        pass
    finally:
        return returnVal


def getAll(iso: str, country: str, url: str, target_file: str, countryListObj: CountryList) -> Dict(str, str):
    '''
        Externally you're supposed to invoke this function, which will get JSON formatted places for a certain country.

        Return value will be a dictionary, holding status of operation
    '''
    status = {'error': 'incomplete'}
    try:
        if(__get_data__(iso=iso, request=Request(url), target_file=target_file, countryListObj=countryListObj)):
            status = {'success': 'true'}
        else:
            status = {'success': 'false'}
    except Exception as e:
        status['error'] = str(e)
    finally:
        if(exists(abspath('./tmp.zip'))):
            remove(abspath('./tmp.zip'))
        return status


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)

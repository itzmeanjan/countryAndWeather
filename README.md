# countryAndWeather
A collection of scripts for grabbing and processing detailed Country/ Place Record & Weather Data for almost 6.36M places, written in Python with :heart:

Consider putting :star: to show some :heart:

Fork, watch this repo, use and/ or modify.

## what does it do ?
- These scripts will help you to fetch Country and Language data from [GeoNames](http://download.geonames.org)
- Then process those text data and convert them to JSON, after some cleaning
- Now we can fetch Admin Code Level 1 & 2 from same site, after some cleaning, we'll store those in JSON files
- Now we need detailed places record for each of those countries, which will be fetched
- No doubt this will be a time consuming operation
- As our final goal is to grab Weather Data for almost 6.36M places all over world, we need to filter out eligible places using criteria such as whether we've any County and Municipality record for that place or not
- And then we'll store filtered out place records in data/weatherXX.json files, where XX denotes ISO country code. Each record will hold Place Name and URL, where we can find Weather Data
- Which can used by other applications for grabbing Weather Data of those places

## how to use it ?
- Well for using these scripts make sure you've Python3.7 installed
- Now follow steps below to generate final data set, whcih can used for many more purposes.

### grab Country Data :
First we'll require list of all Countries, which will be downloaded via [this](fetch/country.py) script.
```bash
>> cd fetch
>> python3 country.py
```
And processed data will be stored in `data/country.json`.

#### Example Data :
```json
{
    "countries": [
        {
            "iso": "AD",
            "iso3": "AND",
            "isoNumeric": "020",
            "fips": "AN",
            "country": "Andorra",
            "capital": "Andorra la Vella",
            "area(in sq km)": "468",
            "population": "84000",
            "continent": "EU",
            "tld": ".ad",
            "currencyCode": "EUR",
            "currencyName": "Euro",
            "phone": "376",
            "postalFormat": "AD###",
            "postalRegex": "^(?:AD)*(\\d{3})$",
            "languages": [
                "ca"
            ],
            "geonameid": "3041565",
            "neighbours": [
                "ES",
                "FR"
            ],
            "equivalentFips": ""
        },
        {

        }
    ]
}
```
### grab Language Data :
Well this step isn't mandatory, if you don't need this data set, you can simply ignore it. 
```bash
>> cd fetch
>> python3 langauge.py
```
Fetches language records along with their code and name, stores it in `data/language.json`, which can be used for mapping Language Code to Name or reverse.
#### Example Data :
```json
{
    "languages": [
        {
            "iso3": "aaa",
            "iso": "",
            "name": "Ghotuo"
        },
        {
            "iso3": "aab",
            "iso": "",
            "name": "Alumu-Tesu"
        },
        {

        }
    ]
}
```
### grab Admin Code Level 1 :
We're interested in this dataset because finally we'll generate Weather Data fetching URL, which requires both `admin1Code` and `admin2Code` for a certain place.
```bash
>> cd fetch
>> python3 admin1Code.py
```
Generated data set will be available in `data/admin1Code.json`
#### Example Data :
```json
{
    "codes": [
        {
            "admin1Code": "AD.06",
            "name": "Sant Julià de Loria"
        },
        {
            "admin1Code": "AD.05",
            "name": "Ordino"
        },
        {

        }
    ]
}
```
Seeing admin1Code dataset, you may have already understood, `admin1Code` field will be name period seperated.

So in above example,

`AD` denotes `Andorra`, which is where this place belongs to.
Now, in `AD.06`, remaining part

`06` denotes admin1Code of a certain place, which is available in each detailed place record files, which are to be processed in next step.

So our objective is to build this `data/admin1Code.json` dataset previously so that when in next step we start building detailed place record, we can use a simple replacement algorithm, which will eventually replace `admin1Code` field in `data/XX.json` file.

And in further step we've to use `data/XX.json` files for filtering out eligible places which can receive Weather data from [Yr.no](http://yr.no). And eligible place records will be kept in `data/weatherXX.json`.

Well in case of `data/XX.json` / `data/weatherXX.json`, _XX_ denotes ISO Country Code.
### grab Admin Code Level 2 :
We're interested in this dataset due to same reason depicted in previous section.
```bash
>> cd fetch
>> python3 admin1Code.py
```
Fetched and processed dataset will be kept in `data/admin2Code.json`.
#### Example Data :
```json
{
    "codes": [
        {
            "admin2Code": "AE.01.101",
            "name": "Abu Dhabi Municipality"
        },
        {
            "admin2Code": "AE.01.102",
            "name": "Al Ain Municipality"
        },
        {

        }
    ]
}
```
We'll objectify both `data/admin1Code.json` and `data/admin2Code.json` records and use in next step while processing detailed place records.
### grab Detailed Place Record :
Now we've Country Data, so we can proceed to fetch Detailed Place Records from GeoNames and store processed ( _required_ ) data as JSON in `data/XX.json` files, where XX denotes ISO-2 Code for a certain country ( _capitalized_ ).

**Note :- This step includes a very time consuming operation. We'll fetch `252` countries detailed Place records _( more than `20M` place records to be processed )_ and then extract those for processing and finally storing as JSON in target file.**

```bash
>> cd fetch
>> python3 places.py
```
Time taken :
```bash
{'success': 'true'}

real	1227m48.254s
user	1199m37.516s
sys	3m8.032s
```
**So be patient :)**

You may find one script `fetch/place.py`, this is basically doing all heavy liftings behind the scene, when you ran `fetch/places.py`. In `fetch/places.py` we start fetching detailed Place Record for each and every country iteratively. And decompression, processing for certain country's Places is done via methods present in `fetch/place.py`.
#### Example Data :
```json
{
    "places": [
        {
            "geonameid": "11945555",
            "name": "Pavelló Joan Alay",
            "alternateNames": [
                "Pavello Joan Alay",
                "Pavelló Joan Alay"
            ],
            "loc": "1.51674,42.50421",
            "featureClass": "S",
            "featureCode": "STDM",
            "country": "Andorra",
            "cc2": [],
            "admin1Code": "Andorra la Vella",
            "admin2Code": "",
            "population": "0",
            "elevation": "",
            "tz": "Europe/Andorra"
        },
        {

        }
    ]
}
```
### extract eligible Places :
So now we've almost **20M+** records of places all over world. We'll require to filter out which among these places will be able to receive Weather Data from [Yr.no](http://yr.no)

For this I've written a script `weather/extract.py` which will be iterating over all those country's detailed place record files, named as `XX.json`, and extract out those place records which has _name_, _couuntry_, _admin1Code_ & _admin2Code_ fields present. And finally generate _URL_, where it can query it's Weather.

Generated data set will be stored in `data/weatherXX.json` for each of those Countries.
```bash
>> cd weather
>> python3 extract.py
```
This one won't take longer.
```bash
Success

real	6m3.095s
user	4m48.007s
sys	0m30.560s
```
#### Example Data :
```json
{
    "places": [
        {
            "name": "Nchelenge District",
            "url": "http://yr.no/place/Zambia/Luapula/Nchelenge_District/forecast.xml"
        },
        {
            "name": "Mporokoso District",
            "url": "http://yr.no/place/Zambia/Northern/Mporokoso_District/forecast.xml"
        },
        {

        }
    ]
}
```
### grabbing Weather Forecast :
Now we've a collection of JSON files in `data` directory, which are having form like `weatherXX.json`, where `XX` denotes ISO Country Code.

We're able to fetch processed Weather Forecast of almost **6.36M** places all over World.

Our `weather/parse.py` script can fetch Weather Forecast of any of those places.

Use `weather.parse.parseIt('target-place-url')` to get Weather Forecast of your intended place in `Dict[str, Any]` form.

Time Taken :
```bash
real	0m0.452s
user	0m0.341s
sys	0m0.012s
```
#### Example Response :
```json
{
    "location": {
        "name": "Bīrbhūm",
        "type": "Administrative division",
        "country": "India",
        "tz": {
            "id": "Asia/Kolkata",
            "utcoffsetminutes": "330"
        },
        "loc": {
            "altitude": "55",
            "latitude": "24",
            "longitude": "87.58333",
            "geobase": "geonames",
            "geobaseid": "1275525"
        }
    },
    "meta": {
        "lastupdate": 1561924522.0,
        "nextupdate": 1561968000.0
    },
    "sunrise": 1561937128.0,
    "sunset": 1561986074.0,
    "forecast": [
        {
            "time": {
                "from": 1561968000.0,
                "to": 1561986000.0,
                "period": "2"
            },
            "symbol": {
                "number": "9",
                "numberex": "9",
                "name": "Rain",
                "var": "09"
            },
            "precipitation": "0.9",
            "winddirection": {
                "deg": "81.6",
                "code": "E",
                "name": "East"
            },
            "windspeed": {
                "mps": "3.0",
                "name": "Light breeze"
            },
            "temperature": {
                "unit": "celsius",
                "value": "30"
            },
            "pressue": {
                "unit": "hPa",
                "value": "996.1"
            }
        },
        {
            "time": {
                "from": 1561986000.0,
                "to": 1562007600.0,
                "period": "3"
            },
            "symbol": {
                "number": "9",
                "numberex": "9",
                "name": "Rain",
                "var": "09"
            },
            "precipitation": "3.5",
            "winddirection": {
                "deg": "71.9",
                "code": "ENE",
                "name": "East-northeast"
            },
            "windspeed": {
                "mps": "3.2",
                "name": "Light breeze"
            },
            "temperature": {
                "unit": "celsius",
                "value": "29"
            },
            "pressue": {
                "unit": "hPa",
                "value": "996.3"
            }
        },
        {

        }
    ]
}
```
In response all time related fields will be in form of timestamp.

#### explanation of Forecast Data :
So there'll be mainly _5_ keys in returned `Dict`.

- location
- meta
- sunrise
- sunset
- forecast

### _location_ ::
This one will have following _5_ keys inside it.
- _name_ : Place Name, of which we've received Forecast
- _type_ : Category of Place
- _country_ : Country Name where place belongs to
- _tz_ : Place's TimezoneId and UTCOffset, in this form `{
            "id": "Asia/Kolkata",
            "utcoffsetminutes": "330"
        }`
- _loc_ : Location information of this place, in this form `{
            "altitude": "55",
            "latitude": "24",
            "longitude": "87.58333",
            "geobase": "geonames",
            "geobaseid": "1275525"
        }`
### _meta_ ::
Well this field is more like meta data, keeps this data `{
        "lastupdate": 1561924522.0,
        "nextupdate": 1561968000.0
    }`. As previously said all time related data will be kept as timestamp, so both `lastupdate` & `nextupdate` fields will hold timestamps.
### _sunrise_ ::
Timestamp of sunrise in current place.
### _sunrise_ ::
Same as previous one, but sunrise.
### _forecast_ ::
This field will hold a JSON array object ( actually a Python List object ), where each element will be of this form.
```json
{
            "time": {
                "from": 1561968000.0,
                "to": 1561986000.0,
                "period": "2"
            },
            "symbol": {
                "number": "9",
                "numberex": "9",
                "name": "Rain",
                "var": "09"
            },
            "precipitation": "0.9",
            "winddirection": {
                "deg": "81.6",
                "code": "E",
                "name": "East"
            },
            "windspeed": {
                "mps": "3.0",
                "name": "Light breeze"
            },
            "temperature": {
                "unit": "celsius",
                "value": "30"
            },
            "pressue": {
                "unit": "hPa",
                "value": "996.1"
            }
}
```
- _time_ :: Field holds `from` and `to`, denoting time span of this forecast. Another field `period` is interesting, in the sense, [Yr.no](http://yr.no/) Forecast Data splits a _24h_ lengthy day into _4_ segements as below.
```
Period 0 |-| 00:30:00 - 06:30:00
Period 1 |-| 06:30:00 - 12:30:00
Period 2 |-| 12:30:00 - 18:30:00
Period 3 |-| 18:30:00 - 00:30:00
```
- _symbol_ :: This data will be required for fetching Weather State PNG Icon using `weather.icon.fetch()`. Weather state name is provided inside it. Use `var` field as `icon_id` parameter, while invoking `weather.icon.fetch()`.
```json
{
    "number": "9",
    "numberex": "9",
    "name": "Rain",
    "var": "09"
}
```
- _precipitation_ :: Holds value of precipitation, for current time slot.
```txt
"0.9"
```
- _winddirection_ :: Name, Code of direction along with degree.
```json
{
    "deg": "81.6",
    "code": "E",
    "name": "East"
}
```
- _windspeed_ :: Speed of wind flow in `meters/second` unit, along with name of wind.
```json
{
    "mps": "3.0",
    "name": "Light breeze"
}
```
- _temperature_ :: Value along with unit.
```json
{
    "unit": "celsius",
    "value": "30"
}
```
- _pressure_ :: Value along with unit.
```json
{
    "unit": "hPa",
    "value": "996.1"
}
```
### fetching Weather Icon :
I've added one small utility script `weather/icon.py`, which will download requested Weather Icon, to be identified by _IconId_, and place in _target_file_path_.

Use it this way. First get _iconId_ from forecast data you've just received ( _var_ field in each forecast timeslot )
```python
weather.icon.fetch(icon_id='29m', target_file='../data/29m.png')
```
In success returns `True` else `False`.

Well make sure you pass target_file parameter has `*.png` form.

**More may come in near future ...**

### courtesy :
Weather Data is fetched from [Yr.no](http://yr.no/), so thanks to them for keeping this great service up. And feel free to check [T&C](https://hjelp.yr.no/hc/en-us/articles/360001946134-Data-access-and-terms-of-service).


Hope this helps ;)
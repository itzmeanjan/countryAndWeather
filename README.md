# country
A collection of scripts for grabbing and processing detailed Country/ Place Record & Weather Data for almost 6.36M places, written in Python with :heart:

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

Time Taken :
```bash
real	0m0.452s
user	0m0.341s
sys	0m0.012s
```
**More coming soon ...**
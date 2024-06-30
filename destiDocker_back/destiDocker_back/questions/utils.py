import requests
import json
import urllib


def get_countries(url, country):
    response = requests.get(url + country)
    response.raise_for_status()
    data_continents = response.json()
    countries = [country for country in data_continents]
    return countries


def filter_countries(countries, weather):
    weather_dict = {
        'tropical': [
            "Angola", "Cape Verde", "Somalia", "Comoros", "Mauritius",
            "Tanzania", "Senegal", "Seychelles", "São Tomé and Príncipe",
            "Liberia", "Guinea", "Madagascar", "Mayotte", "Kenya", "Ghana",
            "Malawi", "Réunion", "Sierra Leone", "Nigeria",
            "Saint Helena, Ascension and Tristan da Cunha", "Mozambique",
            "Cameroon", "Republic of the Congo", "Gabon", "Ivory Coast",
            "Equatorial Guinea", "Burkina Faso", "Burundi", "Suriname", "Bolivia",
            "Guadeloupe", "Barbados", "El Salvador", "Saint Kitts and Nevis",
            "Trinidad and Tobago", "Jamaica", "Bahamas", "Paraguay",
            "Saint Lucia", "United States Virgin Islands", "Panama",
            "Antigua and Barbuda", "Dominica", "Venezuela", "Guyana", "Mexico",
            "Bermuda", "British Virgin Islands", "Nicaragua",
            "Saint Pierre and Miquelon", "Dominican Republic", "Haiti", "Cuba",
            "Belize", "Anguilla", "Colombia", "Costa Rica", "Brazil",
            "Martinique", "Saint Vincent and the Grenadines", "Sint Maarten", "Grenada",
            "Maldives", "Hong Kong", "Sri Lanka", "Singapore", "Philippines",
            "Brunei", "Laos", "Taiwan", "Indonesia", "Kiribati", "Cook Islands",
            "Vanuatu", "Tuvalu", "Samoa", "Fiji", "Micronesia", "Niue",
            "Solomon Islands", "New Caledonia", "Tonga", "Tokelau",
            "Marshall Islands", "American Samoa", "Palau", "Guam", "Christmas Island",
            "Pitcairn Islands", "French Polynesia", "Northern Mariana Islands",
            "Papua New Guinea"
        ],
        'arid': [
            "Namibia", "Sudan", "Western Sahara", "Zimbabwe", "Togo",
            "Lesotho", "Mauritania", "Mali", "Niger", "Botswana",
            "Libya", "Chad", "Algeria", "Kuwait", "Oman", "Yemen",
            "Iraq", "United Arab Emirates", "Bahrain", "Myanmar",
            "Azerbaijan", "Kazakhstan", "Jordan", "Qatar", "Iran",
            "Saudi Arabia", "Syria", "Lebanon", "Pakistan", "Nepal"
        ],
        'subtropical': [
            "Saint Martin", "Turks and Caicos Islands", "Aruba", "Puerto Rico",
            "Honduras", "Ecuador", "Guatemala", "Cayman Islands",
            "Curaçao", "Montserrat", "Uruguay", "Peru",
            "United States Minor Outlying Islands", "Chile",
            "French Guiana", "Saint Barthélemy", "Anguilla", "Israel", "Georgia",
            "Australia", "New Zealand"
        ],
        'temperate': [
            "Falkland Islands", "Greenland", "Argentina", "Sint Maarten", "Colombia",
            "Timor-Leste", "Uzbekistan", "Bangladesh", "Tajikistan", "South Korea",
            "Turkey", "Afghanistan", "Japan", "South Korea", "Turkey", "Belarus",
            "Estonia", "Ireland", "Slovenia", "Liechtenstein", "North Macedonia",
            "Ukraine", "Faroe Islands", "Svalbard and Jan Mayen", "Poland",
            "United Kingdom", "France", "Romania", "Croatia", "Norway",
            "Czechia", "Moldova", "Iceland", "Portugal", "Montenegro",
            "Luxembourg", "Germany", "Switzerland", "Andorra", "Bulgaria",
            "Cyprus", "Hungary", "Malta", "Italy", "Latvia", "Denmark",
            "Greece", "Lithuania", "Monaco", "Gibraltar", "San Marino",
            "Sweden", "Belgium", "Vatican City", "Netherlands", "Spain",
            "Isle of Man", "Slovakia", "Bosnia and Herzegovina", "Serbia",
            "Austria"
        ],
        'mountainous': [
            "Nepal", "Kyrgyzstan", "Afghanistan", "Tajikistan", "Bhutan",
            "Georgia", "Armenia", "Switzerland", "Andorra", "Austria",
            "Bolivia", "Chile", "Ecuador", "Peru", "Canada", "United States",
            "Norway", "New Zealand", "Iran", "Italy", "France", "Germany",
            "Pakistan", "India", "Japan"
        ]}
    filtered_countries = []
    for w in weather:
        for country in countries:
            if country['name']['common'] in weather_dict[w] and country not in filtered_countries:
                filtered_countries.append(country)
    return filtered_countries


def get_country_id(countries):
    dict_countries = {}
    for country in countries:
        where_dict = {
            "name": str(country)
        }
        where = urllib.parse.quote_plus(json.dumps(where_dict))
        url = f'https://parseapi.back4app.com/classes/Continentscountriescities_Country?where={where}'
        headers = {
            'X-Parse-Application-Id': 'J0N5Xu7Z4hPhdlnXEa9iK5vIXOfSxDTsEwK7nHia',
            'X-Parse-REST-API-Key': 'nb139EQwb7s0iRfZrFye2WqLACTQL9C7cfKKMV87'
        }
        data = json.loads(requests.get(
            url, headers=headers).content.decode('utf-8'))
        try:
            dict_countries[country] = data['results'][0]['objectId']
        except:
            pass
    return dict_countries


def get_cities(countries, many_cities):
    cities = {}
    for country, id in countries.items():
        where_dict = {
            "country": {
                "__type": "Pointer",
                "className": "Continentscountriescities_Country",
                "objectId": id
            }
        }
        limit = 10 if many_cities else 3
        where = urllib.parse.quote_plus(json.dumps(where_dict))
        url = f'https://parseapi.back4app.com/classes/Continentscountriescities_City?where={where}&order=-population&limit={limit}'
        headers = {
            'X-Parse-Application-Id': 'J0N5Xu7Z4hPhdlnXEa9iK5vIXOfSxDTsEwK7nHia',
            'X-Parse-REST-API-Key': 'nb139EQwb7s0iRfZrFye2WqLACTQL9C7cfKKMV87'
        }
        data = json.loads(requests.get(
            url, headers=headers).content.decode('utf-8'))
        city_data = [{'name': result['name'], 'population': result['population']}
                     for result in data['results']]
        cities[country] = city_data
    return cities


def get_flights(api_key, dep_iata, arr_iata, departure_date):
    url = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': api_key,
        'dep_iata': dep_iata,
        'arr_iata': arr_iata,
        'flight_date': departure_date,
        'limit': 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        flights = [
            {
                'flight_number': flight['flight']['iata'],
                'departure_time': flight['departure']['estimated'],
                'arrival_airport': flight['arrival']['airport'],
                'price': 'N/A'
            }
            for flight in data.get('data', [])
        ]
        return flights
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return []

def get_airports(country, city):
    if country == 'US':
        api_url = 'https://api.api-ninjas.com/v1/airports?city={}&name={}'.format(city, 'International')
        response = requests.get(api_url, headers={'X-Api-Key': 'e05Mw921/fGtzcIw08mVvw==1LhUMEen5QY4OMJs'})
        if response.status_code == requests.codes.ok:
            airports = response.json()
        else:
            print("Error:", response.status_code, response.text)
        if not airports:
            api_url = 'https://api.api-ninjas.com/v1/airports?region={}&name={}'.format(city, 'International')
            response = requests.get(api_url, headers={'X-Api-Key': 'e05Mw921/fGtzcIw08mVvw==1LhUMEen5QY4OMJs'})
            if response.status_code == requests.codes.ok:
                airports = response.json()
            else:
                print("Error:", response.status_code, response.text)
    else:
        api_url = 'https://api.api-ninjas.com/v1/airports?country={}&name={}'.format(country, 'International')
        response = requests.get(api_url, headers={'X-Api-Key': 'e05Mw921/fGtzcIw08mVvw==1LhUMEen5QY4OMJs'})
        if response.status_code == requests.codes.ok:
            airports = response.json()
        else:
            print("Error:", response.status_code, response.text)
    
    airports_filtered = [airport for airport in airports if airport['city'] == city]
    if airports_filtered:
        return airports_filtered
    return airports

def get_city_depp(city):
    api_url = 'https://api.api-ninjas.com/v1/airports?iata={}&name={}'.format(city, 'International')
    response = requests.get(api_url, headers={'X-Api-Key': 'e05Mw921/fGtzcIw08mVvw==1LhUMEen5QY4OMJs'})
    if response.status_code == requests.codes.ok:
        airports = response.json()
    return airports
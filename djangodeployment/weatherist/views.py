import os
from dotenv import load_dotenv
from pathlib import Path
import datetime
import requests
from django.shortcuts import render
from urllib.parse import urlencode
import pandas as pd
import pickle





# Create your views here.


def location_finder(request):   
    if request.method == 'POST':
        ADDRESS = request.POST['Address']
        dict = {
        0: ['amusement_park','aquarium','art_gallery','food','bakery','bar',
        'beauty_salon','campground','hindu_temple',
        'mosque','museum','park','rv_park','stadium',
        'tourist_attraction','zoo','landmark','place_of_worship','town_square','cemetery',
        'church',
        'city_hall','synagogue','travel_agency','archipelago','restaurant','tourist_attraction'],
        1: [ 'amusement_park',
        'aquarium',
        'art_gallery','bakery',
        'bar','cafe',
        'campground','synagogue','travel_agency','archipelago','mosque','restaurant','tourist_attraction'],
        2: [
        'beauty_salon','book_store',
        'bowling_alley','casino','library','night_club', 'shoe_store',
        'shopping_mall','aquarium','art_gallery','food','bakery','bar',
        'beauty_salon',
        'spa','clothing_store',
        'convenience_store','restaurant','department_store','meal_takeaway','gas_station'],
        3: ['restaurant','food','locality',
        'natural_feature',
        'neighborhood',
        'subway_station',
        'supermarket','intersection','synagogue','travel_agency','archipelago',
        'food','mosque','gas_station','florist','colloquial_area','pet_store','tourist_attraction'],
        4: ['university','archipelago','food','restaurant','mosque','gym','gas_station','supermarket',
            'intersection','point_of_interest','synagogue','travel_agency','archipelago','food',
            'mosque','gas_station','florist','colloquial_area','pet_store'],
        5: ['archipelago','food','mosque','restaurant','florist','gas_station','amusement_park','aquarium','art_gallery','food','bakery','bar',
        'campground','hindu_temple',
        'mosque','museum','park','rv_park','stadium',
        'tourist_attraction','zoo','landmark','place_of_worship','town_square','cemetery',
        'church',
        'city_hall']
        }
        lat, long = extract_lat_long(ADDRESS)
        weather_info = weather_from_lat_long(lat,long)
        cluster_number = getting_cluster_number(weather_info)
        places = dict[cluster_number]
        places_data = getting_places(lat, long)
        final_places_list = getting_places_relevant_info(places_data)
        result_list = []
        for place in final_places_list:
            if any(element in places for element in place['keywords']):
                result_list.append({
                    'name': place['name'],
                    'rating': place['rating'],
                    'vicinity': place['vicinity'],
                    'keywords': place['keywords']
                })
        return render(request, 'index.html', {'weather_info': weather_info,'cluster_number': cluster_number, 'result_list': result_list, 'ADDRESS': ADDRESS})
    else:
        return render(request, 'index.html')
    


def extract_lat_long(address, data_type = 'json', api_key = 'Enter Your Maps API KEY'):
    endpoint = f'https://maps.googleapis.com/maps/api/geocode/{data_type}'
    params = {'address': address, 'key': api_key}
    url_params = urlencode(params)
    url = f'{endpoint}?{url_params}'
    r = requests.get(url)
    if r.status_code not in range(200,299):
        return{}
    latlong = {}
    try:
        latlong =  r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlong.get('lat'), latlong.get('lng')

def weather_from_lat_long(lat,long, weather_api_key = 'Enter Your Weather API KEY'):
    endpoint = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'lat': lat, 'lon': long, 'appid': weather_api_key}
    url_params = urlencode(params)
    url = f'{endpoint}?{url_params}'
    r = requests.get(url)
    if r.status_code not in range(200,299):
        return{}
    weather_data = {}
    try:
        weather_data =  r.json()
    except:
        pass
    weather_info = {
        'temp': round(weather_data.get('main', {}).get('temp'),2),
        'main': weather_data.get('weather', [{}])[0].get('main'),
        'clouds': weather_data.get('clouds',{}).get('all'),
    }

    return weather_info


def getting_cluster_number(data):
   
    data = [data]
    df = pd.DataFrame(data)
    df.columns = ['Temperature', 'Weather_Main', 'Cloudiness']
    weather_main_order = {
        'Clear': 0,
        'Clouds': 1,
        'Drizzle': 2.5,
        'Thunderstorm': 1.5,
        'Rain': 3.5,
        'Snow': 4.5,
    }
    df['Weather_Main_encoded'] = df['Weather_Main'].map(weather_main_order)
    df.fillna(1.5, inplace= True)
    df.drop(columns = 'Weather_Main', inplace=True)
    with open('.\savedmodels\standard_scalar_pickle','rb') as scalars:
        scalar = pickle.load(scalars)
    y = scalar.transform(df)
    with open('.\savedmodels\kmeans_model_pickle','rb') as kmeans:
        model = pickle.load(kmeans)
    z = model.predict(y)
    return z[0]  


def getting_places(lat, long, radius = 5000, api_key = 'Enter Your Maps API KEY'):
    base_endpoint_places = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
 
    params = {
    'key' : api_key,
    'location': f'{lat},{long}',
    'keyword' : 'attractions',
    'radius': radius
    }
    encoded_param = urlencode(params)
    places_url = f'{base_endpoint_places}?{encoded_param}'
    r = requests.get(places_url)
    places = r.json()
    return places

def getting_places_relevant_info(places_data):
    info_list = []
    for result in places_data['results']:
        info_dict = {}
        info_dict['name'] = result['name']
        if 'rating' in result:
            info_dict['rating'] = result['rating']
        else:
            info_dict['rating'] = 'N/A'
        if 'vicinity' in result:
            info_dict['vicinity'] = result['vicinity']
        else:
            info_dict['vicinity'] = 'N/A'
        info_list.append(info_dict)
        info_dict['keywords'] = result['types']
    return info_list
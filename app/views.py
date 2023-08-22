from django.shortcuts import render
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def index(request):
    API_KEY = os.environ.get('API_KEY')
    cw_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    fc_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,allerts&appid={}'


    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.get('city2', None)

        weather_data1, daily_forecasts1  = fetch_weather_and_forecast(city1, API_KEY, cw_url, fc_url)

        if city2:
            weather_data2, daily_forecasts2  = fetch_weather_and_forecast(city2, API_KEY, cw_url, fc_url)
        else:
            weather_data2, daily_forecasts2 = None, None
        
        context = {
        'weather_data1': weather_data1,
        'daily_forecasts1': daily_forecasts1,
        'weather_data2': weather_data2,
        'daily_forecasts2': daily_forecasts2,
        }
        return render(request, 'w_app/index.html', context)


    else:
        return render(request, 'w_app/index.html')
    
    




def fetch_weather_and_forecast(city, api_key, cw_url, fc_url):
    response = requests.get(cw_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(fc_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }

    daily_forecasts = []

    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon']

        })

    return weather_data, daily_forecasts



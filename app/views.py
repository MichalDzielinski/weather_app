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
        city2 = request.POST['city2']
    else:
        return render(request, 'w_app/index.html')
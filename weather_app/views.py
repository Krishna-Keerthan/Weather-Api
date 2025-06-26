from django.shortcuts import render
import requests
import datetime
import logging
# Create your views here.

def index(request):
    API_KEY = open("API_KEY",'r').read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    
    if request.method =='POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2',None)
        weather_data1 , daily_forecast1 =fetch_weather_and_forecast(city1 , API_KEY , current_weather_url, forecast_url)
        
        if city2:
            weather_data2 , daily_forecast2 =fetch_weather_and_forecast(city2 , API_KEY , current_weather_url, forecast_url)
        else:
             weather_data2 , daily_forecast2 = None ,None
             
        context = {
            "weather_data1" : weather_data1,
            "daily_forecast1" : daily_forecast1, 
            "weather_data2" : weather_data2,
            "daily_forecast2" : daily_forecast2,
            }
        
        return render(request , 'weather_app/index.html',context)
    
    else:
        return render(request, 'weather_app/index.html')
    
def fetch_weather_and_forecast(city , api_key , current_weather_url , forecast_url):
    response = requests.get(current_weather_url.format(city,api_key)).json()
    
    lat , lon = response['coord']['lat'] , response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json()
    
    weather_data = {
        "city":city.upper(),
        "temperature":round(response['main']['temp'] - 253.15,2),
        "description":response['weather'][0]['description'],
        "icon":response['weather'][0]['icon']
    }
    
    daily_forecasts = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Iterate through the first 5 entries in the forecast response
    for i, daily_data in enumerate(forecast_response["list"][:5]):
        daily_forecasts.append({
            "day": days[i],  # Use the corresponding day from the `days` list
            "min_temp": round(daily_data['main']['temp_min'] - 253.15,2),
            "max_temp": round(daily_data['main']['temp_max'] - 253.15,2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })
        
    
    return weather_data , daily_forecasts
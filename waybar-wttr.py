#!/usr/bin/env python
import os
import json
import requests
from  datetime import datetime
from dotenv import load_dotenv
load_dotenv()
conf = os.getenv("WETHER_LOCATiON")
WEATHER_CODES = {
    '113': '☀️ ',
    '116': '⛅ ',
    '119': '☁️ ',
    '122': '☁️ ',
    '143': '☁️ ',
    '176': '🌧️',
    '179': '🌧️',
    '182': '🌧️',
    '185': '🌧️',
    '200': '⛈️ ',
    '227': '🌨️',
    '230': '🌨️',
    '248': '☁️ ',
    '260': '☁️ ',
    '263': '🌧️',
    '266': '🌧️',
    '281': '🌧️',
    '284': '🌧️',
    '293': '🌧️',
    '296': '🌧️',
    '299': '🌧️',
    '302': '🌧️',
    '305': '🌧️',
    '308': '🌧️',
    '311': '🌧️',
    '314': '🌧️',
    '317': '🌧️',
    '320': '🌨️',
    '323': '🌨️',
    '326': '🌨️',
    '329': '❄️ ',
    '332': '❄️ ',
    '335': '❄️ ',
    '338': '❄️ ',
    '350': '🌧️',
    '353': '🌧️',
    '356': '🌧️',
    '359': '🌧️',
    '362': '🌧️',
    '365': '🌧️',
    '368': '🌧️',
    '371': '❄️',
    '374': '🌨️',
    '377': '🌨️',
    '386': '🌨️',
    '389': '🌨️',
    '392': '🌧️',
    '395': '❄️ '
}

data = {}
if conf:
    weather = requests.get(f"https://wttr.in/{conf}?lang=uk&format=j1").json()
else:
    weather = requests.get(f"https://wttr.in?lang=uk&format=j1").json()

def format_time(time):
    return time.replace("00", "").zfill(2)


def format_temp(temp):
    return (hour['FeelsLikeC']+"C°").ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Туман",
        "chanceoffrost": "Холодно",
        "chanceofovercast": "похмуро",
        "chanceofrain": "Дощ",
        "chanceofsnow": "Сніг",
        "chanceofsunshine": "Сонячно",
        "chanceofthunder": "Злива",
        "chanceofwindy": "Вітеряно"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

tempint = int(weather['current_condition'][0]['FeelsLikeC'])
extrachar = ''
if tempint > 0 and tempint < 10:
    extrachar = '+'


data['text'] = ' '+WEATHER_CODES[weather['current_condition'][0]['weatherCode']] + \
    " "+extrachar+weather['current_condition'][0]['FeelsLikeC']+"C°"
data['tooltip'] = f"<b>Країна: {weather['nearest_area'][0]['country'][0]['value']}</b>"
data['tooltip'] += f"\n<b>Місто: {weather['nearest_area'][0]['areaName'][0]['value']}</b>\n"
data['tooltip'] += f"<b>Регіон: {weather['nearest_area'][0]['region'][0]['value']}</b>\n"
data['tooltip'] += f"<b>Стан: {weather['current_condition'][0]['lang_uk'][0]['value']} {WEATHER_CODES[weather['current_condition'][0]['weatherCode']]}</b>\n"
data['tooltip'] += f"Відчувається, як: {weather['current_condition'][0]['FeelsLikeC']}С°\n"
data['tooltip'] += f"Вітер: {weather['current_condition'][0]['windspeedKmph']}км/год\n"
data['tooltip'] += f"Вологість: {weather['current_condition'][0]['humidity']}%\n"
for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Сьогодні, "
    if i == 1:
        data['tooltip'] += "Завтра, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f"⬆️ {day['maxtempC']}С° ⬇️ {day['mintempC']}С° "
    data['tooltip'] += f"🌅 {(datetime.strptime(day['astronomy'][0]['sunrise'], '%I:%M %p')):%H:%M} 🌇 {(datetime.strptime(day['astronomy'][0]['sunset'], '%I:%M %p')):%H:%M}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time'])}:00 {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])}, {hour['lang_uk'][0]['value']}\n"
print(json.dumps(data))
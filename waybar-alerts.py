#!/usr/bin/env python
import requests
import os 
import json
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()
config = {
    "sity":os.getenv("SITY"),
    "district":os.getenv("DISTRICT")
    }
def alerts_is_check(x):
    if x == "🟢":
        return 'Дата відбою: '
    else:
        return 'Початок: '
rest = {
     'tooltip':''
}
data = {
    "text":'',
    "tooltip":''
}

count = 0
def convert_isotime_to_time(iso_time, timezone):
    dt = datetime.fromisoformat(iso_time)
    converted_dt = dt.astimezone(pytz.timezone(timezone))
    return converted_dt.strftime("%d.%m.%y 🕐 %H:%M:%S")

timezone = "Europe/Kiev"
alerts = requests.get("https://programmershouse-api.is-an.app/alerts")
data_alerts = alerts.json()

for _ in data_alerts:
    if data_alerts[f'{_}']['alarm'] == 'true':
            count += 1
            rest["tooltip"] += f"<b>{_} {data_alerts[f'{_}']['emoji']} {convert_isotime_to_time(data_alerts[f'{_}']['time'],timezone='Europe/Kiev')}</b>\n"
if config["sity"]:
        data["text"] = f"{data_alerts[config['sity']]['emoji']} {config['sity']} ({count})"
        data["tooltip"] = f"<b>{config['sity']}</b>\n<b>Стан: {data_alerts[config['sity']]['emoji']}</b>\n<b>{alerts_is_check(data_alerts[config['sity']]['emoji'])}{datetime.fromisoformat(data_alerts[config['sity']]['time']):%y/%m/%d 🕐 %H:%M}</b>\n\nТривога в:\n"

if config["district"]:
        for _ in data_alerts:
            for disc in data_alerts[f'{_}']['districts']:
                 if disc == config['district']:
                    data["tooltip"] = f"<b>{config['sity']}</b>\n<b>Cтан: {data_alerts[config['sity']]['emoji']}</b>\n<b>{alerts_is_check(data_alerts[config['sity']]['emoji'])}{convert_isotime_to_time(data_alerts[config['sity']]['time'],timezone='Europe/Kiev')}</b>\n<b>{config['district']}</b>\n<b>Стан: {data_alerts[_]['districts'][config['district']]['emoji']}</b>\n<b>{alerts_is_check(data_alerts[_]['districts'][config['district']]['emoji'])}{convert_isotime_to_time(data_alerts[_]['districts'][config['district']]['time'],timezone=timezone)}</b>\n\nТривога в:\n"
        
data["tooltip"] += rest['tooltip']
print(json.dumps(data))    

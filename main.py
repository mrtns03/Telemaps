# This script must run every minute between the timerange you normally start going to work
# from MON-FRI 06:00:00-07:00:00 every minute
# * 6-7 * * 1-5 /path/to/main.py

import os
import time
import requests
import json
import sys


def send_message(text: str):
    url_tele = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?TELEGRAM_CHAT_ID={TELEGRAM_CHAT_ID}&text={text}"
    requests.get(url_tele).json()


def get_data_from_file(filename: str):
    f = open(filename)
    value = bool(int(f.readlines()[0]))
    f.close()
    return value


def set_data_in_file(filename: str,data: str):
    w = open(filename, 'w')
    w.write(data)
    w.close()


def get_message_text():
    normal_distance = 46745
    # specify the normal distance of your route
    # you can get the distance also from the maps api

    duration_good = 2100
    # duration in s for green emoji
    duration_bad = 2700
    # duration in s for red emoji
    # yellow emoji is between duration_good and duration_bad

    url_maps = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={PLACE_START}%{STREET_START}%20{HOUSENUMBER_START}&destinations={PLACE_DEST}%{STREET_DEST}%20{HOUSENUMBER_DEST}&departure_time=now&key={MAPS_API_KEY}"
  
    response = json.loads(requests.request("GET", url_maps).text)
    distance = response['rows'][0]['elements'][0]['distance']['value']
    duration = response['rows'][0]['elements'][0]['duration_in_traffic']['value']

    if distance == normal_distance:
        text_way = 'Fastest route: \U0001F7E2 default'
    else:
        text_way = 'Fastest route: \U0001F7E1 deviating'

    if duration < duration_good:
        text_duration = f"Duration to work: \U0001F7E2 {round(duration / 60)} min"
    elif duration_good < duration < duration_bad:
        text_duration = f"Duration to work: \U0001F7E1 {round(duration / 60)} min"
    elif duration > duration_bad:
        text_duration = f"Duration to work: \U0001F7E0 {round(duration / 60)} min"

    tele_text = text_way + '\n' + text_duration
    return tele_text


def get_connected_devices():
    macs = []
    output_stream = os.popen('sh shell.sh')
    output = output_stream.read().split('\n')
    lines = output[2:-4]
    for line in lines:
        item = line.split('\t')
        macs.append(item[1])
    return macs


#-------------------------CONFIG-------------------------#
# Personal config
MOBILEPHONE_MAC = "YOUR MAC OF YOUR MOBILEPHONE"

# Telegram API config
TELEGRAM_CHAT_ID = "YOUR TELEGRAM CHAT ID"
TELEGRAM_API_TOKEN = 'YOUR TELEGRAM API TOKEN'

# Google Maps API config
MAPS_API_KEY = "YOUR API KEY"

PLACE_START = "YOUR STARTPOINT CITY"
STREET_START = "YOUR STARTPOINT STREET"
HOUSENUMBER_START = "YOUR STARTPOINT HOUSENUMBER"

PLACE_DEST = "YOUR DESTINATION CITY"
STREET_DEST = "YOUR DESTINATION STREET"
HOUSENUMBER_DEST = "YOUR DESTINATION HOUSENUMBER"
#-----------------------CONFIG-END-----------------------#


if MOBILEPHONE_MAC not in get_connected_devices():
    old_connection_state = get_data_from_file('connection_state.txt')
    if old_connection_state:
        executed_today = get_data_from_file('executed_today.txt')
        if not executed_today:
            time.sleep(30)
            if MOBILEPHONE_MAC not in get_connected_devices():
                set_data_in_file('connection_state.txt', '0')
                set_data_in_file('executed_today.txt', '1')
                message_text = get_message_text()
                send_message(message_text)
else:
    set_data_in_file('connection_state.txt', '1')


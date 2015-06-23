__author__ = 'Terrace Boiz'

import urllib
import json
import time

access_key = 'aceec2d6587b3b0c'
weather_url = 'http://api.wunderground.com/api/' + access_key + '/conditions/q/MA/Roxbury_Crossing.json'
spacer = "-------------------------------------------"

def main():
    try:
        while True:
            print spacer
            grab_weather()
            print spacer
            time.sleep(300)
    except (IOError):
        print "Error Loading Weather, Trying Again"
        time.sleep(600)
        main()


def grab_weather():
    response = urllib.urlopen(weather_url)
    global weather_data
    weather_data = json.loads(response.read().decode())
    print "Boston Weather:\n"
    print weather_data['current_observation']['weather']
    print weather_data['current_observation']['feelslike_f'] + u"\u00b0"

def weatherPanel():
    global weather_data
    temperature = int(float(weather_data['current_observation']['feelslike_f']))
    weather = weather_data['current_observation']['weather']
    return  str(temperature) + u"\u00b0", getTempColor(temperature)

#Determine display color for temperature
def getTempColor(temp):
    if (temp >= 90):
        return (255,0,0)
    elif (temp >= 80):
        return (255,50,0)
    elif (temp >= 70):
        return (255,100,0)
    elif (temp >= 60):
        return (255,150,0)
    else:
        return (0,0,255)


if __name__ == "__main__":
    main()
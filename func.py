from vars import conf, token_accu, token_yandex, bot, cities
import json
import requests as req
from geopy import geocoders


with open(cities, encoding='utf-8') as f:
    cities = json.load(f)
    
    
def weather(code_loc: str, token_accu: str):
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{code_loc}?' \
                  f'apikey={token_accu}&language=ru&metric=True'
    response = req.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    dict_weather = dict()
    dict_weather['link'] = json_data[0]['MobileLink']
    print(dict)
    time = 'сейчас'
    dict_weather[time] = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
    for i in range(1, len(json_data)):
        time = 'через' + str(i) + 'ч'
        dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'sky': json_data[i]['IconPhrase']}
    return dict_weather

def code_location(latitude: str, longitude: str, token_accu: str):
    url_location_key = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' \
                       f'{token_accu}&q={latitude},{longitude}&language=ru'
    resp_loc = req.get(url_location_key, headers={"APIKey": token_accu})
    json_data = json.loads(resp_loc.text)
    code = json_data['Key']
    return code

def print_weather(dict_weather, message):
    print(dict)
    bot.send_message(message.from_user.id, f'Погода в городе <b>{message.text}</b>\n'
                                           f' Температура сейчас <b>{dict_weather["сейчас"]["temp"]}</b>\n'
                                           f' <b>{dict_weather["сейчас"]["sky"]}</b>.\n'
                                           f' Температура через три часа <b>{dict_weather["через3ч"]["temp"]}</b>. \n'
                                           f' А на небе <b>{dict_weather["через3ч"]["sky"]}</b>.\n'
                                           f' Температура через шесть часов <b>{dict_weather["через6ч"]["temp"]}</b>!\n'
                                           f' А на небе <b>{dict_weather["через6ч"]["sky"]}</b>.\n'
                                           f' Температура через девять часов <b>{dict_weather["через9ч"]["temp"]}</b>!\n'
                                           f' А на небе <b>{dict_weather["через9ч"]["sky"]}</b>.\n'
                                           f' А здесь ссылка на подробности '
                                           f'{dict_weather["link"]}', parse_mode="HTML")

def print_yandex_weather(dict_weather_yandex, message):
    day = {'night': 'ночью', 'morning': 'утром', 'day': 'днем', 'evening': 'вечером', 'fact': 'сейчас'}
    bot.send_message(message.from_user.id, f'А яндекс говорит:')
    #print(dict_weather_yandex)
    bot.send_message(message.from_user.id, f'Температура Ночью: <b>{dict_weather_yandex["fact"]["temp"]}</b>\n'
                                            f'<b>{dict_weather_yandex["fact"]["condition"]}</b>\n'
                                            f'Направление ветра: {dict_weather_yandex["fact"]["wind_dir"]}\n'
                                            f'Давление: {dict_weather_yandex["fact"]["pressure_mm"]} мм. рт. столба\n'
                                            f'Влажность: {dict_weather_yandex["fact"]["humidity"]} %\n'                                            
                                            f' <b>А здесь ссылка на подробности: </b>'
                                            f'{dict_weather_yandex["link"]}', parse_mode="HTML")
def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude

# нужно получить погоду от яндекса
def yandex_weather(latitude, longitude, token_yandex: str):
    url_yandex = f'https://api.weather.yandex.ru/v2/informers/?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    yandex_req = req.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex}, verify=False)
    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
    wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль', 'с': 'штиль'}

    yandex_json = json.loads(yandex_req.text)
    #print(f'Ответ от яндекса: {yandex_req.text}')
    yandex_json['fact']['condition'] = conditions[yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = wind_dir[yandex_json['fact']['wind_dir']]
    for parts in yandex_json['forecast']['parts']:
        parts['condition'] = conditions[parts['condition']]
        parts['wind_dir'] = wind_dir[parts['wind_dir']]

    weather = dict()
    params = ['condition', 'wind_dir', 'pressure_mm', 'humidity']
    for parts in yandex_json['forecast']['parts']:
        weather[parts['part_name']] = dict()
        weather[parts['part_name']]['temp'] = parts['temp_avg']
        for param in params:
            weather[parts['part_name']][param] = parts[param]

    weather['fact'] = dict()
    weather['fact']['temp'] = yandex_json['fact']['temp']
    for param in params:
        weather['fact'][param] = yandex_json['fact'][param]

    weather['link'] = yandex_json['info']['url']
    return weather

# функция сохранения городов:
def add_city(message):
    try:
        latitude, longitude = geo_pos(message.text.lower().split('город ')[1])
        global cities
        cities[message.from_user.id] = message.text.lower().split('город ')[1]
        with open(cities, 'w') as f:
            f.write(json.dumps(cities))
        return cities, 0
    except Exception as err:
        return cities, 1

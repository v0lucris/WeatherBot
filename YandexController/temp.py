import requests
import json
import pprint

CONDITIONS = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
              'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
              'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
              'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
              'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
              'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
              'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
              }
WIND_DIR = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
            'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}

LATITUDE = '48.7194'
LONGITUDE = '44.5018'

url = f'https://api.weather.yandex.ru/v2/forecast?lat={LATITUDE}&lon={LONGITUDE}&extra=true&lang=ru_RU'
headers = {'X-Yandex-API-Key': 'd7eddc63-6b56-4c2c-a9c6-2641b77db82f'}

test_request = requests.get(url, headers=headers)

# print(test_request.text)
# print(test_request.status_code)
# print(test_request.json())
test_output = test_request.text
yandex_json = json.loads(test_output)

pprint.pprint(yandex_json)

weather = dict()
params = ['condition', 'wind_dir', 'pressure_mm', 'humidity']

yandex_json['fact']['condition'] = CONDITIONS[yandex_json['fact']['condition']]
yandex_json['fact']['wind_dir'] = WIND_DIR[yandex_json['fact']['wind_dir']]

for parts in yandex_json['forecasts']:
    for low_parts in parts['prts']:
        parts['condition'] = CONDITIONS[parts['condition']]
        parts['wind_dir'] = WIND_DIR[parts['wind_dir']]

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


# print(json.dumps(test_output, indent=1, sort_keys=True))

# # GET
# r = requests.get(url)
#
# # GET with params in URL
# r = requests.get(url, params=payload)
#
# # POST with form-encoded data
# r = requests.post(url, data=payload)
#
# # POST with JSON
# import json
# r = requests.post(url, data=json.dumps(payload))
#
# # Response, status etc
# r.text
# r.status_code

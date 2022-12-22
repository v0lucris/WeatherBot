import json

from YandexController import text_speach


class YandexWeather:
    __CONDITIONS = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                    'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                    'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                    'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                    'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                    'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                    'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                    }
    __WIND_DIR = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                  'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}

    __latitude = '48.7194'
    __longitude = '44.5018'

    def __init__(self, input_latitude: str, input_longitude: str):
        self.__latitude = input_latitude
        self.__longitude = input_longitude

    @staticmethod
    def __get_yandex_token():
        import os
        dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
        if os.path.exists(dotenv_path):
            import dotenv
            dotenv.load_dotenv(dotenv_path)
        return dotenv.get_key(dotenv_path, 'token_yandex')

    @staticmethod
    def __get_json(latitude=__latitude, longitude=__longitude):
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&extra=true&lang=ru_RU'
        headers = {'X-Yandex-API-Key': YandexWeather.__get_yandex_token()}

        import requests
        test_request = requests.get(url, headers=headers)
        test_output = test_request.text
        return json.loads(test_output)

    @staticmethod
    def get_forecast():
        yandex_json = YandexWeather.__get_json()
        weather_answer = text_speach.ORIGINAL_TEXT

        yandex_json['fact']['condition'] = YandexWeather.__CONDITIONS[yandex_json['fact']['condition']]
        yandex_json['fact']['wind_dir'] = YandexWeather.__WIND_DIR[yandex_json['fact']['wind_dir']]

        def concatinate_data(first_part: str, second_part: str):
            return first_part + str(second_part) + '\n'

        weather_answer = concatinate_data(weather_answer, yandex_json['info']['url'])

        params = ['temp', 'feels_like', 'condition', 'wind_dir', 'pressure_mm']

        for item in params:
            weather_answer = weather_answer + concatinate_data(text_speach.ANSWER[item], yandex_json['fact'][item])

        return weather_answer

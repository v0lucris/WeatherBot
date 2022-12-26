
import urllib3
from vars import token_accu, token_yandex, cities, bot, tmp_city, hello
from func import weather, code_location, add_city, print_weather, print_yandex_weather, geo_pos, yandex_weather, cities


urllib3.disable_warnings()

# функции ответа на сообщения:
@bot.message_handler(command=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я погодабот, приятно познакомитсья, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global cities
    if message.text.lower() in hello:
        bot.send_message(message.from_user.id,
                         f'Здравствуйте! {message.from_user.first_name}! Позвольте Я доложу '
                         f' Вам о погоде! Напишите  слово "погода" и я напишу погоду в Вашем'
                         f' "стандартном" городе или напишите название города в готором Вы сейчас')
    elif message.text.lower() == 'погода':
        if message.from_user.id in cities.keys():
            city = cities[message.from_user.id]
            bot.send_message(message.from_user.id, f'О великий и могучий {message.from_user.first_name}!'
                                                   f' Твой город {city}')
            latitude, longitude = geo_pos(city)
            code_loc = code_location(latitude, longitude, token_accu)
            you_weather = weather(code_loc, token_accu)
            print_weather(you_weather, message)
            yandex_weather_x = yandex_weather(latitude, longitude, token_yandex)
            print_yandex_weather(yandex_weather_x, message)
        else:
            bot.send_message(message.from_user.id, f'О великий и могучий {message.from_user.first_name}!'
                                                   f' Я не знаю Ваш город! Просто напиши:'
                                                   f'"Мой город *****" и я запомню твой стандартный город!')
    elif message.text.lower()[:9] == 'мой город':
        cities, flag = add_city(message)
        if flag == 0:
            print(cities, message)
            bot.send_message(message.from_user.id, f'О великий и могучий {message.from_user.first_name}!'
                                                   f' Теперь я знаю Ваш город! это'
                                                   f' {cities[message.from_user.id]}')
        else:
            print(cities, message)
            bot.send_message(message.from_user.id, f'О великий и могучий {message.from_user.first_name}!'
                                                   f' Что то пошло не так :( ')
    else:
        try:
            city = message.text
            tmp_city = message.text
            bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}! Твой город {city}')
            latitude, longitude = geo_pos(city)
            code_loc = code_location(latitude, longitude, token_accu)
            you_weather = weather(code_loc, token_accu)
            print_weather(you_weather, message)
            yandex_weather_x = yandex_weather(latitude, longitude, token_yandex)
            print_yandex_weather(yandex_weather_x, message)
        except AttributeError as err:
            bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Не вели казнить,'
                                                   f' вели слово молвить! Я не нашел такого города!'
                                                   f'И получил ошибку {err}, попробуй другой город')


bot.polling(none_stop=True)

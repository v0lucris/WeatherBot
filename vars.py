import yaml
import os
import dotenv
import telebot

try:
    with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), "r") as tmp_cfg:
        conf = yaml.safe_load(tmp_cfg)
except yaml.YAMLError as e:
    print(f'Ошибка чтения файла конфигурации: {e}')



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
token = dotenv.get_key(dotenv_path, 'token')
token_accu = dotenv.get_key(dotenv_path, 'token_accu')
token_yandex = dotenv.get_key(dotenv_path, 'token_yandex')

if os.path.exists(dotenv_path):
    dotenv.load_dotenv(dotenv_path)
conf_dir = conf["path"]["config_dir"]
db_dir = conf["path"]["db_dir"]
cities = os.path.dirname(__file__) + '/cities.json'
bot = telebot.TeleBot(token)
tmp_city='Сеул'
yandex_forecast={}

#шаблоны общения
##Приветствие:
hello = {'привет', 'здарова', 'здравствуйте','добрый день', 'доброе утро', 'добрый вечер', 'hello', 'hi','hey'}

    



import requests
import datetime
from pprint import pprint
from config import open_weather_token

def get_weather(city, open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Show": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }
    try:
        url = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = url.json()
        #pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода)"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        speed = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        len_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        print(f'***{datetime.datetime.now()}***\n'
              f'Погода в городе: {city}\n'
              f'Температура: {cur_weather} С°{wd}\n'
              f'Влажность: {humidity}\n'
              f'Давление: {pressure}\n'
              f'Скорость ветра: {speed}\n'
              f'Восход солнца: {sunrise_timestamp}\n'
              f'Заход солнца: {sunset_timestamp}\n'
              f'Продолжительность светого дня: {len_day}\n'
              f'Желаю вам Хорошего дня!')


    except Exception as ex:
        print(ex)
        print('Проверьте название города')

def main():
    city = input('Введите город: ')
    get_weather(city,open_weather_token)

if __name__ == '__main__':
    main()

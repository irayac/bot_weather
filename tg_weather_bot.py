import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dispatcher = Dispatcher(bot)

@dispatcher.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши название города, я пришлю сводку погоды')

@dispatcher.message_handler()
async def get_weather(message: types.Message):
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
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = url.json()

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

        await message.reply(f'***{datetime.datetime.now()}***\n'
              f'Погода в городе: {city}\n'
              f'Температура: {cur_weather} С°{wd}\n'
              f'Влажность: {humidity}\n'
              f'Давление: {pressure}\n'
              f'Скорость ветра: {speed}\n'
              f'Восход солнца: {sunrise_timestamp}\n'
              f'Заход солнца: {sunset_timestamp}\n'
              f'Продолжительность светого дня: {len_day}\n'
              f'Желаю вам Хорошего дня!')


    except:
        await message.reply('Проверьте название города')


if __name__ == "__main__":
    executor.start_polling(dispatcher)


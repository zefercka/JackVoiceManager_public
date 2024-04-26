# -*- coding: utf8 -*-

# execute commands

import datetime
import json
import os.path
import re
import subprocess
import sys
import threading
import time

import colorama
import keyboard

import pymorphy2
import requests
from pyautogui import screenshot
# import selenium
import ru_core_news_lg
import wikipedia
import pyperclip
from colorama import Back, Fore, Style
from deep_translator import GoogleTranslator
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from timezonefinder import TimezoneFinder

import config
import data_exchange

# browser = None
# browser_type = "Chrome"
# opts_browser = Options()
# opts_browser.headless = True

# path = os.path.dirname(sys.executable)
# path = path.split('\\')[0] + r"\MyScripts\profile"
colorama.init()

# path_browser = r"drivers/chromedriver.exe"
# browser = Chrome(executable_path=path_browser, options=opts_browser)
# browser = helium.start_firefox("www.google.com", headless=False)

time_zone = None
tf = TimezoneFinder()
city_ru = requests.get('https://ru.sxgeo.city').json()['city']['name_ru']      # Имя города на русском
city_en = requests.get('https://ru.sxgeo.city').json()['city']['name_en']    # Имя города на английском

nlp = ru_core_news_lg.load()
nlp.Defaults.stop_words |= {'сколько'}

morph = pymorphy2.MorphAnalyzer(lang='ru')

# openWeatherToken
api_weather = 'c5097413ad66dc7ba5e055799536255a'

# mapbox token
mapbox_token = "pk.eyJ1IjoiemVmZXJja2EiLCJhIjoiY2t5emo1czNuMTJycjJ3cWw3MXZpcGNhbCJ9.vrMV3din8h1ysugNeuHZ-Q"

translator_ru_en = GoogleTranslator(source="ru", target="en")

wikipedia.set_lang("ru")

month_days = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

log = None
calendar_ = None


def set_logger(lg):
    global log
    log = lg


def set_calendar():
    global calendar_
    calendar_ = GoogleCalendar()


class DateTime:
    times = datetime.datetime.now()

    def __init__(self, year=times.year, month=times.month, day=times.day, hour=times.hour, minute=times.minute,
                 second=times.second, data_str=None):
        if data_str is None:
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour
            self.minute = minute
            self.second = second

        else:
            data_l = data_str.split("T")    # ["2021-12-31", "13:00:00"]
            data_ = data_l[0].split("-")    # ["2021", "12", "31"]
            time_ = data_l[1].split(":")    # ["13", "00", "00"]

            self.year = int(data_[0])
            self.month = int(data_[1])
            self.day = int(data_[2])
            self.hour = int(time_[0])
            self.minute = int(time_[1])
            self.second = int(time_[2])

    def seconds(self):
        while self.second >= 60:
            self.second -= 60
            self.minute += 1
        self.minutes()

    def minutes(self):
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        self.hours()

    def hours(self):
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
        self.days()

    def days(self):
        while self.day > month_days[self.month]:
            if self.month != 2:
                self.day -= month_days[self.month]
                self.month += 1
            else:
                if (self.year % 4 == 0) and (self.year % 100 != 0) or (self.year % 400 == 0):
                    self.month += 1
                    self.day -= 29
                else:
                    self.month += 1
                    self.day -= 28

            if self.month > 12:
                self.year += 1
                self.month -= 12

    def str_format(self):
        str_format = f"{self.year}-" \
                          f"{self.month if len(str(self.month)) == 2 else f'0{self.month}'}-" \
                          f"{self.day if len(str(self.day)) == 2 else f'0{self.day}'}T" \
                          f"{self.hour if len(str(self.hour)) == 2 else f'0{self.hour}'}:" \
                          f"{self.minute if len(str(self.minute)) == 2 else f'0{self.minute}'}:" \
                          f"{self.second if len(str(self.second)) == 2 else f'0{self.second}'}"

        return str_format


class Browser:
    def __init__(self):
        options = ChromeOptions()
        options.headless = True
        # options_browser.add_argument(f"--user-data-dir={path}")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36")

        self.browser = Chrome(options=options, executable_path="chromedriver.exe")

    def exchange_rate(self, request):
        self.browser.get(f"https://yandex.ru/search/?text={request}")

        cost = self.browser.execute_script('return(document.querySelectorAll(".Textinput-Control")[1].value)')
        rate = self.browser.execute_script('return(document.querySelector(".ConverterHeader-Rate").textContent)')\
            .split()[-1]

        end = search_ends(int(cost[-1]), word=rate)

        costed = convert_number_to_text(int(cost.split(",")[0]), 0) + "и" + \
                 convert_number_to_text(int(cost.split(",")[1]), 0)

        return costed + " " + end


class GoogleCalendar:
    def __init__(self):
        self.auth_calendar()

    def auth_calendar(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except:
                pass # убрать
                os.remove("token.json")
                self.auth_calendar()

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    def create_notification(self, data):
        # data - (name, data_time_start, data_time_name)
        # name = str
        # data_time = str - Year-Month-Day T Hour:Minute:Second
        event = {
            'summary': f'{data[0]}',
            'start': {
                'dateTime': f'{data[1]}+03:00',
                'timeZone': 'Europe/Moscow',
            },
            'end': {
                'dateTime': f'{data[1]}+03:00',
                'timeZone': 'Europe/Moscow',
            },
        }

        self.service.events().insert(calendarId='primary', body=event).execute()


class NoteBook:
    def __init__(self):
        import speech_recognition as sr

        self.sr = sr
        self.r = sr.Recognizer()
        self.m = []
        self.stopped = 1

    def start(self):
        if self.stopped == 1:
            self.stopped = 0
            threading.Thread(target=self.rec).start()
            threading.Thread(target=self.listen).start()
        else:
            self.stopped = 1

    def rec(self):
        while self.stopped == 0:
            if len(self.m) > 0:
                audio = self.m[0]
                try:
                    action = self.r.recognize_google(audio, language="ru_RU").lower()
                    if action.strip() != "":
                        keyboard.write(" " + action.replace("точка", ".").replace("запятая", ","))
                    del self.m[0]
                except Exception as err:
                    del self.m[0]
                    continue

            threading.Event().wait(2)

    def listen(self):
        with self.sr.Microphone() as source:
            while self.stopped == 0:
                try:
                    audio = self.r.listen(source=source, phrase_time_limit=5)
                    self.m.append(audio)
                    continue
                except:
                    continue


ntn = NoteBook()

browser = Browser()


def text_transform(text_):
    request = nlp(text_)

    text_lemma = ''
    for token in request:
        text_lemma += str(token.lemma_) + ' '

    text = ''
    for word in nlp(text_lemma):
        if word.is_stop is False:
            text += str(word) + ' '

    return text


def get_param(text, params):

    # params - список параметров: "city", "day"
    # Функция вернёт словарь - response
    # -----
    # response:
    # "param_city" - город из запроса на русском языке
    # "param_day" - через сколько дней произойдёт событие

    year = int(datetime.datetime.now().strftime("%Y"))

    # print(params)

    data_now = DateTime()

    response = {
        "param_city": None,
        "param_day": 0,
        "time_format": "",
    }

    tokens = nlp(text)

    for token_id in range(len(tokens)):     # Определение года - по умолчанию настоящий
        token = tokens[token_id]
        if token.pos_ == "NUM":
            try:
                if str(tokens[token_id + 1]) == "год" or str(tokens[token_id - 1]) == "год":
                    year = int(str(token))
            except:
                continue

    time_str = DateTime()
    for param_name in params:
        if param_name == "city":    # Определение города в запросе
            for token_id in range(len(tokens)):
                token = tokens[token_id]
                if token.pos_ == "PROPN":
                    if response["param_city"] is None:
                        response["param_city"] = str(token)
                    else:
                        response["param_city"] += str(token)

        elif param_name == "day":   # Определение разницы дней между настоящим и в запросе (возможно через сколько
            # дней это должно произойти)
            for token_id in range(len(tokens)):
                token = tokens[token_id]
                if (token.pos_ == "NUM") or (token.pos_ == "ADJ"):
                    check = str(token).split(':')
                    if len(check) == 1:
                        try:
                            if str(tokens[token_id + 1]) == "день" and str(tokens[token_id - 1]) in ['через']:
                                response["param_day"] = int(str(token))
                                time_str.day += response["param_day"]
                                time_str.days()
                            
                            elif str(tokens[token_id + 1]) in config.months:
                                try:
                                    if time_str.month == config.months[str(tokens[token_id + 1])]:
                                        # Если месяц сейчас равен месяцу в запросе
                                        if data_now.day < int(str(token)):
                                            # Если день сейчас меньше чем день в запросе то
                                            response["param_day"] = abs(int((datetime.datetime.now() - datetime.datetime(
                                                year, config.months[str(tokens[token_id + 1])], int(str(token)))).days))
                                            # дата сейчас - дата в запросе

                                            time_str.day += response["param_day"]
                                            time_str.days()
                                            time_str.hour = 8
                                            time_str.minute = 0
                                            time_str.second = 0
                                            # Установка даты и времени (8:00:00) для напоминания
                                        elif data_now.day == int(str(token)):
                                            # Если день сейчас равен дню в запросе, то напоминание ставиться на 23:00
                                            time_str.hour = 23
                                            time_str.minute = 0
                                            time_str.second = 0
                                        else:
                                            time_str.year += 1

                                    elif data_now.month < config.months[str(tokens[token_id + 1])]:
                                        # Если месяц сейчас меньше чем месяц в запросе
                                        response["param_day"] = abs(int((datetime.datetime.now() - datetime.datetime(
                                            year, config.months[str(tokens[token_id + 1])], int(str(token)))).days))
                                        time_str.day += response["param_day"]
                                        time_str.days()

                                    else:
                                        time_str.year += 1
                                        time_str.month = config.months[str(tokens[token_id + 1])]
                                        time_str.day = int(str(token))
                                        time_str.hour = 8
                                        time_str.minute = 0
                                        time_str.second = 0
                                        # Установка даты и времени (8:00:00) для напоминания
                                except ValueError:
                                    return "Названая вами дата не существует"

                        except Exception as err:
                            print(Fore.GREEN + Style.BRIGHT + "execute_command - get_param (day): " + Style.NORMAL + Fore.RED + str(err))
                            break

                elif token.pos_ == 'ADV' and str(token) in config.ADV_list:
                    try:
                        response["param_day"] = config.ADV_list.index(str(token)) + 1
                        time_str.day += response["param_day"]
                    except:
                        continue

        elif param_name == "time":
            time_ = 0
            for token_id in range(len(tokens)):
                token = tokens[token_id]
                if token.pos_ == "NUM":
                    check = str(token).split(":")
                    if len(check) == 1:
                        try:
                            if str(tokens[token_id + 1]) == "секунда" and str(tokens[token_id - 1]):
                                # через 10 секунд
                                time_ += int(str(token))
                            elif str(tokens[token_id + 1]) == "минута" and str(tokens[token_id - 1]) in ['через']:
                                # через 10 минут
                                time_ += int(str(token)) * 60
                            elif str(tokens[token_id + 1]) == "час" and str(tokens[token_id - 1]) in ['через']:
                                # через 10 часов
                                time_ += int(str(token)) * 3600
                            elif str(tokens[token_id + 1]) == "минута":
                                # в 15 минут
                                if (time_str.minute < int(str(token)) and time_str.day == data_now.day) or \
                                        (time_str.day > data_now.day):
                                    time_str.minute = int(str(token))
                                else:
                                    time_str.minute = int(str(token))
                                    time_str.hour += 1

                                time_str.minutes()

                            elif str(tokens[token_id + 1]) == "час":
                                # в 15 часов
                                if (data_now.hour < int(str(token)) and time_str.day == data_now.day) or \
                                        (time_str.day > data_now.day):
                                    time_str.hour = int(str(token))
                                    time_str.minute = 0
                                    time_str.second = 0
                                else:
                                    time_str.hour = int(str(token))
                                    time_str.day += 1

                                time_str.hours()

                        except ValueError:
                            return "Ошибка времени"
                    else:
                        # Напомни в 16:00
                        times = str(token).split(':')

                        if (time_str.minute < int(times[1]) and time_str.day == data_now.day) or \
                                (time_str.day > data_now.day):
                            time_str.minute = int(times[1])
                        else:
                            time_str.minute = int(times[1])
                            time_str.hour += 1

                        if (data_now.hour < int(times[0]) and time_str.day == data_now.day) or \
                                (time_str.day > data_now.day):
                            time_str.hour = int(times[0])
                            time_str.minute = 0
                            time_str.second = 0
                        else:
                            time_str.hour = int(times[0])
                            time_str.day += 1

                elif (token.pos_ == "ADJ") and (":" in str(token)):
                    # Напомни в 16:00
                    times = str(token).split(':')

                    if (time_str.minute < int(times[1]) and time_str.day == data_now.day) or \
                            (time_str.day > data_now.day):
                        time_str.minute = int(times[1])
                    else:
                        time_str.minute = int(times[1])
                        time_str.hour += 1

                    if (data_now.hour < int(times[0]) and time_str.day == data_now.day) or \
                            (time_str.day > data_now.day):
                        time_str.hour = int(times[0])
                        time_str.minute = 0
                        time_str.second = 0
                    else:
                        time_str.hour = int(times[0])
                        time_str.day += 1

            time_str.second += time_
            time_str.seconds()

        response["time_format"] = time_str.str_format()

    return response


def search_ends(number, type_=None, word=None):
    if type_ is not None:
        if abs(number) < 15:
            end = config.ends[number][type_]
        else:
            end = config.ends[number % 10][type_]

    else:
        if abs(number) < 15:
            n = abs(number)
        else:
            n = [number % 10]

        form = config.cases_inflect[n]
        end = morph.parse(word)[0].inflect({form[0], form[1]}).word

    return end


def help_convert(number, type_):
    text = ""
    if number not in config.numbers_text:
        while True:
            num = str(number)

            n = len(num)    # кол-во разрядов
            d = int("1" + "0"*(n-1))

            a, b = divmod(number, d)

            text += config.numbers_text[int(str(a)+"0"*(n-1))][type_]
            text += " "

            if b != 0:
                if b not in config.numbers_text:
                    number = b
                else:
                    text += config.numbers_text[b][type_]
                    break
            else:
                break
    else:
        text = config.numbers_text[number][type_]

    return text


def convert_number_to_text(number, type_):
    text = ""
    if number not in config.numbers_text:
        while True:
            num = str(number)

            n = len(num)  # кол-во разрядов
            if n in [1, 2, 3, 4]:
                d = int("1" + "0" * (n - 1))
            elif n in [5, 6]:
                d = 1000
            elif n in [7, 8, 9]:
                d = 1000000

            print(d)

            a, b = divmod(number, d)

            if n in [4, 5, 6, 7, 8, 9]:
                text += help_convert(a, 1)
                text += " "
                if n in [4, 5, 6]:
                    text += search_ends(a, 6)
                elif n in [7, 8, 9]:
                    text += search_ends(a, 8)
                text += " "
            else:
                text += config.numbers_text[int(str(a) + "0" * (n - 1))][type_]
                text += " "

            if b != 0:
                if b not in config.numbers_text:
                    number = b
                else:
                    text += config.numbers_text[b][type_]
                    break
            else:
                break
    else:
        text = config.numbers_text[number][type_]
    print(text)
    return text


def data_to_text(data):
    try:
        response = ""
        data_ = DateTime(data_str=data)

        if data_.day % 10 > 4:
            response += f"{convert_number_to_text(data_.day, 0)[0:-1]}ое "
        else:
            if data_.day < 11:
                response += f"{config.data_number[data_.day]} "
            else:
                response += f"{convert_number_to_text(int(str(data_.day // 10)+'0'), 0)} {config.data_number[data_.day]} "

        response += f"{morph.parse(config.months_[data_.month])[0].inflect({'gent'}).word} " \
                    f"{convert_number_to_text(data_.hour, 0)} {search_ends(data_.hour, 0)} {convert_number_to_text(data_.minute, 1)} {search_ends(data_.hour, 1)}"
        return response
    except Exception as err:
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)


def weather_request(text_):
    method = 'weather'

    params = get_param(text_transform(text_), ["city", "day"])

    param_day = params["param_day"]
    param_city = params["param_city"]
    if param_city is None:
        param_city = city_ru

    if param_day != 0:
        method = "onecall"

    # print(param_city)
    # print(param_day)

    if param_day == 0:
        try:
            response = requests.get(f'http://api.openweathermap.org/data/2.5/{method}?q={param_city}&appid='
                                    f'{api_weather}&units=metric').json()
            # print(response)
            temp = round(float(str(response['main']['temp'])))
            text_answer = f"Сейчас в {morph.parse(param_city)[0].inflect({'loct'}).word}, температура составляет " \
                          f"{temp} {search_ends(abs(temp), 2)}, " \
                          f"{config.weather_id[response['weather'][0]['id']]}"
        except KeyError:
            text_answer = f"Я не смог найти город {param_city}"
            log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                      type_="INFO", inf="Город не найден")
        except Exception as err:
            log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                      err=err)
            return "Возникла непредвиденная ошибка"
    else:
        if param_day < 7:
            try:
                response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{param_city}.json?'
                                        f'types=region&'
                                        f'access_token={mapbox_token}').json()
                cord = response["features"][0]["center"]
                lat = cord[1]
                lon = cord[0]

                print(lat, lon)
                response = requests.get(f'http://api.openweathermap.org/data/2.5/{method}?appid={api_weather}&units=metric&'
                                        f'lat={lat}&lon={lon}&exclude=current,minutely,hourly&lang=ru').json()

                min_temp = round(response['daily'][param_day]['temp']['min'])
                max_temp = round(response['daily'][param_day]['temp']['max'])

                text_answer = f"Через {param_day} {search_ends(param_day, 3)} в " \
                              f"{morph.parse(param_city)[0].inflect({'loct'}).word} " \
                              f"минимальная температура составит {min_temp} " \
                              f"{search_ends(abs(min_temp), 2)}, " \
                              f"максимум температура поднимется до {'минус' if max_temp < 0 else ''} {convert_number_to_text(abs(max_temp), 2)} " \
                              f"{search_ends(abs(max_temp), 7)}, " \
                              f"{config.weather_id[response['daily'][param_day - 1]['weather'][0]['id']]}"

                log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                          status=True)
                # print(text_answer)
            except KeyError as err:
                log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                          status=False, type_="INFO", inf="Город не найден")
                return "Я не смог найти город {param_city}"
            except Exception as err:
                log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                          status=False, err=err)
                return "Возникла непредвиденная ошибка"
        else:
            try:
                city_en_weather = translator_ru_en.translate(param_city)
                subprocess.Popen(config.browser_path + f' /new_tab "https://yandex.ru/pogoda/{city_en_weather}"')
                log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                          status=True)
                return "Открываю прогноз погоды"
            except Exception as err:
                log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                          status=False, err=err)
                return "Возникла непредвиденная ошибка"

    return text_answer


def google_search_def(text_):
    time_start = time.time()

    text_search = text_[1]
    for word in ["найди в гугл", 'поиск в гугл', 'найти в google', 'поиск в google', 'google', 'гугл', 'найти в гугл']:
        text_search = text_search.strip(word)

    text_search = text_search.strip(' ')
    print(text_search)

    try:
        subprocess.Popen(f'{config.browser_path} /new_tab "https://www.google.ru/search?q={text_search}"')

        print(time.time() - time_start)
        return 'Открываю результаты'

    except Exception as err:
        print("(google search) error: " + str(err))
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)

        print(time.time() - time_start)
        return 'Возникла непредвиденная ошибка'


def time_request(text_):
    time_start = time.time()
    params = get_param(text_transform(text_), ["city"])
    print(params)

    param_city = params["param_city"]
    if param_city is None:
        param_city = city_en

    # print(f"{time.time() - time_start} - params")

    try:

        response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{param_city}.json?'
                                f'types=country,region,place&'
                                f'access_token={mapbox_token}').json()
        cord = response["features"][0]["center"]
        lat = cord[1]
        lon = cord[0]

        t_z = tf.timezone_at_land(lng=lon, lat=lat)
        # print(f"{time.time() - time_start} - timezones")
        while True:
            try:    
                time_ = requests.get(f"http://worldtimeapi.org/api/timezone/{t_z}").json()['datetime'].split('T')[1].split(':')
                break
            except:
                continue

        # print(time_)
        # print(f"{time.time() - time_start} - time_str")
        text_time = ''

        text_time += convert_number_to_text(int(time_[0]), 0) + " "
        text_time += search_ends(int(time_[0]), 0)
        text_time += " " + convert_number_to_text(int(time_[1]), 1) + " "
        text_time += search_ends(int(time_[1]), 1)

        # print(f"{time.time() - time_start} - time_transofrm")

        answer_text = f'Время в {morph.parse(param_city)[0].inflect({"loct"}).word} {text_time}'

        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                  status=True)
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                  status=True, type_="INFO", inf=f"{time.time() - time_start}")

        # print(Fore.GREEN + Style.BRIGHT + "Execute_command - time_request: " + Style.NORMAL + Fore.WHITE + "successful")
        # print(Fore.GREEN + Style.BRIGHT + "Execute_command - time_request (time): " + Style.NORMAL + Fore.WHITE + f"{time.time() - time_start}")
    except Exception as err:
        print(Fore.GREEN + Style.BRIGHT + "Execute_command - time_request: " + Style.NORMAL + Fore.RED + str(err))
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)
        return "Произошла непредвиденная ошибка"

    return answer_text


def notification(text_):
    text = text_transform(text_)
    print(text)
    params = get_param(text, ["day", "time"])

    print(params)

    resp = data_to_text(params["time_format"])

    try:
        data = (f"Напоминание", params["time_format"])
        calendar_.create_notification(data)

        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                  status=True)
        return "Напоминание установлено в google календарь на " + resp
    except Exception as err:
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)
        return "Не удалось установить напоминание в google календарь"


def create_screenshots(*args):
    try:
        if config.path_to_screenshots.strip() != "":
            screenshot(
                fr"{config.path_to_screenshots}\screenshot-{datetime.datetime.now().strftime('%H-%M-%S-%Y-%m-%d')}.png")
            return "Скриншот сохранён в папке по умолчанию"
        else:
            screenshot(
                fr"{os.getcwd()}\screenshots\screenshot-{datetime.datetime.now().strftime('%H-%M-%S-%Y-%m-%d')}.png")

            log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                      status=True)
            return "Скриншот успешно сохранён"
    except Exception as err:
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)
        return "Не удалось сохранить скриншот"


def create_route(text_):
    x = text_.replace("-", " - ").split()

    from_ = ""
    target = ""
    k = 0  # 0 - перебор, 1 - от, 2 - до

    delete = ["маршрут", "построй", "путь", "строй", "дорогу", "сколько", "ехать", "покажи", "как",
              "доехать", "построить", "посмотреть", "маршрута", "карта", "дорога"]

    z = []
    for i in x:
        if i not in delete:
            z.append(i)

    for i in z:
        if i == "от" or i == "из":
            k = 1
        elif i == "до" or i == "в":
            k = 2
        elif i == "-":
            q = 0
            while z[q] != "-":
                from_ += z[q]
                from_ += " "
                q += 1
            k = 2
        else:
            if k == 1:
                from_ += i
                from_ += " "
            elif k == 2:
                target += i
                target += " "

    print(from_, target)

    try:
        if from_.strip() != "":
            response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{from_}.json?'
                                    f'types=region,address,place,poi&'
                                    f'access_token={mapbox_token}').json()
            cord = response["features"][0]["center"]
            lat_f = cord[1]
            lon_f = cord[0]
        else:
            response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{city_ru}.json?'
                                    f'types=region&'
                                    f'access_token={mapbox_token}').json()
            cord = response["features"][0]["center"]
            lat_f = cord[1]
            lon_f = cord[0]
    except Exception as err:
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)
        return "Произошла непредвиденная ошибка"

    try:
        if target.strip() != "":
            response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{target}.json?'
                                    f'types=region,address,place,poi&'
                                    f'access_token={mapbox_token}').json()
            cord = response["features"][0]["center"]
            lat_t = cord[1]
            lon_t = cord[0]
        else:
            return "Я не смог найти место назначение"
    except Exception as err:
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)
        return "Произошла непредвиденная ошибка"

    try:
        url = (f"https://api.mapbox.com/directions/v5/mapbox/driving/{lon_f},{lat_f};{lon_t},{lat_t}?access_token=" +
                f"{mapbox_token}")
        # print(url)
        response = requests.get(url)
    except Exception as err:
        log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                  err=err)
        return "Произошла непредвиденная ошибка"

    if response.status_code == 200:
        try:
            j = response.json()['routes'][0]
            dist = round(float(j['distance']) / 1000, 1)
            t = round(float(j['duration']) / 60, 1)

            d = int(t // 1440)
            h = int((t - d * 1440) // 60)
            m = round(t - (d * 1440 + h * 60))

            t_ans = ''

            if d > 0:
                t_ans += f"{convert_number_to_text(d, 0)} {search_ends(d, 3)} "
            if h > 0:
                t_ans += f"{convert_number_to_text(h, 0)} {search_ends(h, 0)} "
            if m > 0:
                t_ans += f"{convert_number_to_text(m, 1)} {search_ends(m, 1)}"

            log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name,
                      status=True)

            if dist >= 1:
                if dist%1 != 0.0:
                    return "Длина маршрута составит " + str(dist).replace(".", " и ", 1) + " кило" + \
                           search_ends(int(dist % 1*10), 5) + ", время в пути: " + t_ans
                else:
                    return "Длина маршрута составит " + str(int(dist)) + " кило" + search_ends(int(dist % 1 * 10), 5) \
                            + ", время в пути: " + t_ans

            else:
                return "Длина маршрута составит " + str(int(dist*1000)) + search_ends(int(dist % 1 * 10), 5) + \
                       ", время в пути: " + t_ans

        except Exception as err:
            log.write(file=os.path.basename(__file__).split(".")[0], func=sys._getframe().f_code.co_name, status=False,
                      err=err)
            return "Не удалось построить маршрут"
    else:
        print("")
        return "Ошибка соединения с сервером"


def exchange(text_):
    rtr = browser.exchange_rate(text_)
    return rtr

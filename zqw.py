# # import requests
# # import time
# # from deep_translator import GoogleTranslator as GT
# # from execute_command import search_ends, convert_number_to_text
# #
# # print(convert_number_to_text(22, 0))
# # print(convert_number_to_text(00, 1))
# #
# # t_ru_en = GT(source="auto", target="en")
# #
# # t_ = time.time()
# # param_1 = t_ru_en.translate("Флорида США")
# # param_2 = t_ru_en.translate("Техас США")
# # print(param_1, param_2)
# #
# # # print(convert_number_to_text(100406, 0))
# #
# # print(f'https://graphhopper.com/api/1/geocode?q={param_1}'
# #                                 f'&key=afa34048-7782-459f-96ba-7d77f61b9c14')
# # response = requests.get(f'https://graphhopper.com/api/1/geocode?q={param_1}'
# #                                 f'&key=afa34048-7782-459f-96ba-7d77f61b9c14').json()
# # print(response)
# # cord_1 = f"{response['hits'][0]['point']['lng']},{response['hits'][0]['point']['lat']}"
# #
# # response = requests.get(f'https://graphhopper.com/api/1/geocode?q={param_2}'
# #                                 f'&key=afa34048-7782-459f-96ba-7d77f61b9c14').json()
# # cord_2 = f"{response['hits'][0]['point']['lng']},{response['hits'][0]['point']['lat']}"
# # print(f'https://graphhopper.com/api/1/geocode?q={param_2}'
# #                                 f'&key=afa34048-7782-459f-96ba-7d77f61b9c14')
# # print(cord_1, cord_2)
# #
# # url = (f"https://api.mapbox.com/directions/v5/mapbox/driving/{cord_1};{cord_2}?access_token=" +
# #         "pk.eyJ1IjoiemVmZXJja2EiLCJhIjoiY2t5emo1czNuMTJycjJ3cWw3MXZpcGNhbCJ9.vrMV3din8h1ysugNeuHZ-Q")
# # print(url)
# # response = requests.get(url)
# #
# #
# # def refactor_time(t):
# #     d = int(t // 1440)
# #     h = int((t - d*1440) // 60)
# #     m = round(t - (d*1440 + h*60))
# #
# #     t_ans = ''
# #
# #     if d > 0:
# #         t_ans += f"{convert_number_to_text(d, 0)} {search_ends(d, 3)} "
# #     if h > 0:
# #         t_ans += f"{convert_number_to_text(h, 0)} {search_ends(h, 0)} "
# #     if m > 0:
# #         t_ans += f"{convert_number_to_text(m, 1)} {search_ends(m, 1)}"
# #
# #     print(t_ans)
# #
# #
# # if response.status_code == 200:
# #     try:
# #         j = response.json()['routes'][0]
# #         d = round(float(j['distance']) / 1000, 1)
# #         t = round(float(j['duration']) / 60, 1)
# #         refactor_time(t)
# #         print(str(d) + " километров")
# #     except Exception as err:
# #         print("Не удалось построить маршрут: ", err)
# # else:
# #     print("Ошибка соединения с сервером")
# #
# # print(time.time() - t_)
#
# from deep_translator import GoogleTranslator as GT
# import keyboard
#
# t_ru_en = GT(source="auto", target="en")
#
# keyboard.add_hotkey('Ctrl', lambda: print('Hello'))
#
# while True:
#     a = 1
#
# import config
# import execute_command
#
#
# def help_(number, type_):
#     text = ""
#     if number not in config.numbers_text:
#         while True:
#             num = str(number)
#
#             n = len(num)    # кол-во разрядов
#             d = int("1" + "0"*(n-1))
#
#             a, b = divmod(number, d)
#
#             text += config.numbers_text[int(str(a)+"0"*(n-1))][type_]
#             text += " "
#
#             if b != 0:
#                 if b not in config.numbers_text:
#                     number = b
#                 else:
#                     text += config.numbers_text[b][type_]
#                     break
#             else:
#                 break
#     else:
#         text = config.numbers_text[number][type_]
#
#     return text
#
#
# number = 19000000
# type_ = 0
#
# text = ""
# if number not in config.numbers_text:
#     while True:
#             num = str(number)
#
#             n = len(num)    # кол-во разрядов
#             match n:
#                 case 1 | 2 | 3 | 4:
#                     d = int("1" + "0"*(n-1))
#                 case 5 | 6:
#                     d = 1000
#                 case 7 | 8 | 9:
#                     d = 1000000
#             print(d)
#
#             a, b = divmod(number, d)
#
#             match n:
#                 case 4 | 5 | 6 | 7 | 8 | 9:
#                     text += help_(a, 1)
#                     text += " "
#                     match n:
#                         case 4 | 5 | 6:
#                             text += execute_command.search_ends(a, 6)
#                         case 7 | 8 | 9:
#                             text += execute_command.search_ends(a, 8)
#                     text += " "
#                 case _:
#                     text += config.numbers_text[int(str(a)+"0"*(n-1))][type_]
#                     text += " "
#
#             if b != 0:
#                 if b not in config.numbers_text:
#                     number = b
#                 else:
#                     text += config.numbers_text[b][type_]
#                     break
#             else:
#                 break
# else:
#     text = config.numbers_text[number][type_]
#
# print(text)
#
# import keyboard
# import threading
#
# def on_triggered():
#     print("Ваша функция!!!")
#
# keyboard.add_hotkey('num 0', on_triggered)
#
# print(1)

# import os
# import sys
# import threading
#
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
#
# path = os.path.dirname(sys.executable)
# path = path.split('\\')[0] + r"\MyScripts\profile"
#
# options_browser = ChromeOptions()
# options_browser.headless = True
# # options_browser.add_argument(f"--user-data-dir={path}")
# options_browser.add_argument("--use-fake-ui-for-media-stream")# звук
# options_browser.add_argument("--disable-gpu")
# options_browser.add_argument("--window-size=1920,1200")
# options_browser.add_argument("--no-sandbox")
# options_browser.add_argument("--allow-insecure-localhost")
# options_browser.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36")
# options_browser.add_experimental_option("excludeSwitches", ["enable-automation"])
# options_browser.add_experimental_option('excludeSwitches', ['enable-logging'])
#
#
# browser = Chrome(options=options_browser, executable_path="chromedriver.exe")
#
# # wait = WebDriverWait(browser, 500)
#
# browser.get("https://speechpad.ru")
# # browser.find_element(By.ID, "recbtn").click()
# # browser.find_element(By.ID, "recbtn").click()
# WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "recbtn")))
# print(1)
# browser.execute_script(r'document.querySelector("#recbtn").click()')
# browser.execute_script("window.scrollTo(0, 1000)")
# while browser.find_element(By.ID, "recbtn").get_attribute("value") == " включить запись ":
#     browser.find_element(By.ID, "recbtn").click()
#     threading.Event().wait(1)
#     browser.get_screenshot_as_file("LambdaTestVisibleScreen.png")
# # browser.minimize_window()
# # browser.find_element(By.ID, "recbtn").click()
# browser.get_screenshot_as_file("LambdaTestVisibleScreen.png")
# browser.quit()
#
# while True:
#     threading.Event().wait(2)
#     text = browser.find_element(By.CLASS_NAME, "-metrika-nokeys").get_attribute("value")
#     browser.execute_script(r'document.querySelector(".-metrika-nokeys").value = ""')
#     if text.strip() != "":
#         print(text)

# import speech_recognition as sr
# import threading
#
# r = sr.Recognizer()
#
# def rec(audio):
#     try:
#         action = r.recognize_google(audio, language="ru_RU").lower()
#         print(action)
#         return 0
#
#     except:
#         pass
#
# with sr.Microphone() as source:
#     while True:
#         audio = r.listen(phrase_time_limit=5, source=source)
#         threading.Thread(target=rec, args=(audio, )).start()
#         print(1)

# import requests
#
# headers = {
#     'Authorization': 'Bearer Ug8kpjef1uc8zY227wK8kCfzbRN72AQyACcYPRVpQM5Pj6oJ1',
#     'Content-Type': 'audio/wave',
# }
#
# with open('Untitled 1.wav', 'rb') as f:
#     data = f.read()
#
# response = requests.post('https://voice.mcs.mail.ru/asr', headers=headers, data=data)
# print(response.json()["result"]["texts"][0]['text'])

import time
import pymorphy2

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from execute_command import *

morph = pymorphy2.MorphAnalyzer(lang='ru')

options_browser = ChromeOptions()
options_browser.headless = True
# options_browser.add_argument(f"--user-data-dir={path}")
options_browser.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36")

browser = Chrome(options=options_browser, executable_path="chromedriver.exe")

q = time.time()

browser.get("https://yandex.ru/search/?text=10 долларов в рублях")

cost = browser.execute_script('return(document.querySelectorAll(".Textinput-Control")[1].value)')
valute = browser.execute_script('return(document.querySelector(".ConverterHeader-Rate").textContent)').split()[-1]

print(cost, search_ends(int(cost[-1]), word="рубль"))

print(time.time() - q)

# import requests
# import pymorphy2
#
# morph = pymorphy2.MorphAnalyzer(lang='ru')
#
# del_words = ["курс", "к", "какой", "сколько"]
# t = "курс доллара к белорускому рублю".split()
# z = []
# for i in t:
#     if i not in del_words:
#         q = morph.parse(i)[0].normal_form
#         z.append(q)
#
# print(z)
#
# x = [["белоруский рубль"], ["драм", "армянский драм"], ["юань", "китайский юань"],
#      ['фунт стерлингов', 'фунт'], ["доллар", "доллар сша"], ["евро"], ["рупий", "индийский рупий"],
#      ["канадский доллар"], ["крона", "датская крона"]]
#
# if len(z) == 3:
#     for i in
#
#
# r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()["Valute"]
#
#
# for i in r.items():
#     x.append(i[1]["Name"].lower())
# print(x)
import os
import sys
import threading

import colorama
from colorama import Back, Fore, Style
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

colorama.init()
path = os.path.dirname(sys.executable)
path = path.split('\\')[0] + r"\MyScripts\profile"


class YandexMusic:
    def __init__(self):
        options_browser = ChromeOptions()
        options_browser.headless = False
        options_browser.add_argument(f"--user-data-dir={path}")

        self.browser = Chrome(options=options_browser, executable_path="chromedriver.exe")

        # adblock = None
        # self.browser.get("https://chrome.google.com/webstore/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom")
        # while adblock is None:
        #     try:
        #         adblock = self.browser.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div")
        #     except:
        #         continue

        # if adblock.text == "Установить":
        #     adblock.click()

        self.browser.get("https://passport.yandex.ru/auth")

        if self.browser.current_url == "https://passport.yandex.ru/auth":
            self.browser.quit()
            options_browser.headless = False
            self.browser = Chrome(options=options_browser, executable_path="chromedriver.exe")
            self.browser.get("https://passport.yandex.ru/auth")

        else:
            self.browser.get("https://music.yandex.ru/")
            self.remove_repeat()
            try:
                self.browser.execute_script("""document.querySelector(".d-icon_shuffle-gold ").click()""")
                self.shuffle_status = 0
            except:
                self.shuffle_status = 0

        self.action_chains = ActionChains(self.browser)
        self.music_status = 0

    def remove_repeat(self):
        self.browser.execute_script("""
        try {
            document.querySelector(".d-icon_repeat-gold").click();
        } catch {
            console.log(1)
        }""")

        threading.Event().wait(0.3)

        self.browser.execute_script("""
        try {
            document.querySelector(".d-icon_repeat-one-gold").click();
        } catch {
            console.log(1)
        }""")

    def play_favourite(self):
        self.browser.execute_script("""document.querySelectorAll(".nav-kids__link")[4].click()""")

        threading.Event().wait(1)
        self.browser.execute_script("""
        a = document.querySelectorAll(".playlist__title")
        for (i = 0; i < a.length; i++) {
            console.log(a[i].title)
            if (a[i].title === "Мне нравится") {
                a[i].click()
            }
        }""")
        threading.Event().wait(3)

        while True:
            try:
                # self.browser.find_elements(By.CLASS_NAME, "button-play__type_playlist")[-1].click()
                self.browser.execute_script("""elements = document.querySelectorAll(".button-play__type_playlist")
                elements[elements.length - 1].click()""")
                self.music_status = 1

                for i in range(2):
                    threading.Event().wait(0.5)
                    self.play_pause()

                break
            except Exception as err:
                print(err)
                threading.Event().wait(0.4)
                continue

    def repeat_playlist(self):
        self.remove_repeat()
        self.browser.execute_script("""document.querySelector(".d-icon_repeat").click()""")

    def shuffle(self):
        if self.shuffle_status == 0:
            while True:
                try:
                    self.browser.execute_script("""document.querySelector(".d-icon_shuffle").click()""")
                    self.shuffle_status = 1
                    break
                except:
                    continue

            print("Перемешивание включено")

        else:
            while True:
                try:
                    self.browser.execute_script("""document.querySelector(".d-icon_shuffle-gold").click()""")
                    self.shuffle_status = 0
                    break
                except:
                    continue
            print("Перемешивание выключено")

    def play_pause(self):
        if self.music_status == 0:
            while True:
                try:
                    self.browser.execute_script("""document.querySelector(".player-controls__btn_play").click()""")
                    self.music_status = 1
                    break
                except:
                    continue

        else:
            while True:
                try:
                    self.browser.execute_script("""document.querySelector(".player-controls__btn_pause").click()""")
                    self.music_status = 0
                    break
                except:
                    continue


class Spotify:
    def __init__(self):
        self.started = False

        self.music_status = 0
        self.repeat_status = 0
        self.shuffle_status = 0
        self.browser = None

    def start_browser(self):
        self.started = True

        options_browser = ChromeOptions()
        # options_browser.headless = True
        options_browser.add_argument(f"--user-data-dir={path}")
        # options_browser.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.browser = Chrome(options=options_browser, executable_path="chromedriver.exe")
        wait = WebDriverWait(self.browser, 500)

        self.browser.get("https://accounts.spotify.com/ru/login")

        while True:
            if self.browser.current_url != "https://accounts.spotify.com/ru/login":
                break
            else:
                threading.Event().wait(1)
                continue

        self.browser.get("https://open.spotify.com/collection/tracks")

        # Ожидание полной загрузки страницы
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "A8NeSZBojOQuVvK4l1pS")))
        # element = None
        # while element is None:
        #     try:
        #         element = self.browser.find_element(By.CLASS_NAME, "A8NeSZBojOQuVvK4l1pS")
        #         # self.browser.execute_script("""a = document.querySelector(".pp1ooFGqFEUG5ucC6_KW")
        #         # if (a) { a.click() }""")
        #         threading.Event().wait(0.2)
        #     except:
        #         threading.Event().wait(0.5)
        #         continue

        try:
            self.browser.find_element(By.CLASS_NAME, "pp1ooFGqFEUG5ucC6_KW")
            self.shuffle_status = 1
        except:
            self.shuffle_status = 0

        # Вынужденная мера
        self.play()
        threading.Event().wait(0.3)
        self.browser.find_element(By.CLASS_NAME, "d4u88Fc9OM6kXh7FYYRj").click()
        threading.Event().wait(0.3)
        self.browser.find_element(By.CLASS_NAME, "d4u88Fc9OM6kXh7FYYRj").click()
        threading.Event().wait(0.3)
        self.pause()
        threading.Event().wait(0.5)

    def remove_repeat(self, *args):
        try:
            self.browser.execute_script("""document.querySelector(".yKo7LWUCQCEALszRxAaS").click()""")
            threading.Event().wait(0.35)
            self.remove_repeat()
        except:
            self.repeat_status = 0
            return "повтор выключен"

    def play_favourite(self, *args):
        try:
            self.browser.execute_script("""document.querySelector(".pTIS4aTGrcrLRflgLO5S").click()""")
            threading.Event().wait(0.5)
            self.browser.execute_script("""document.querySelectorAll(".RfidWIoz8FON2WhFoItU")[0].click()""")
            self.music_status = 1
            print(Fore.GREEN + Style.BRIGHT + "Spotify - play_favourite: " + Style.NORMAL + Fore.WHITE + "successful")
            return "Плейлист 'Любимые треки' включен"
        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - play_favourite: " + Style.NORMAL + Fore.RED + str(err))
            self.play_favourite()
            return "При выполнение функции произошла ошибка"

    def shuffle(self, *args):
        try:
            self.browser.execute_script("""a = document.querySelector(".d4u88Fc9OM6kXh7FYYRj")
                if (a) { a.click() }""")

            try:
                self.browser.find_element(By.CLASS_NAME, "pp1ooFGqFEUG5ucC6_KW")
                self.shuffle_status = 1
            except:
                self.shuffle_status = 0

            if self.shuffle_status == 0:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - shuffle_on: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Перемешивание включено"
            else:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - shuffle_off: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Перемешивание выключено"

        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - shuffle: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    def repeat(self, text=None):
        try:
            self.browser.execute_script("""document.querySelector(".bQY5A9SJfdFiEvBMM6J5").click()""")
            threading.Event().wait(0.5)
            try:
                rep = self.browser.find_element(By.CLASS_NAME, "yKo7LWUCQCEALszRxAaS")
            except:
                rep = None

            print(Fore.GREEN + Style.BRIGHT + "Spotify - repeat: " + Style.NORMAL + Fore.WHITE + "successful")
            if rep:
                print(rep.text)
                return "повтор включен"
            else:
                return "повтор выключен"
        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - repeat: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    # def repeat_track(self, text=None):
    #     self.remove_repeat()

    #     try:
    #         threading.Event().wait(0.3)
    #         self.browser.execute_script("""document.querySelector(".bQY5A9SJfdFiEvBMM6J5").click()""")
    #         threading.Event().wait(0.3)
    #         self.browser.execute_script("""document.querySelector(".bQY5A9SJfdFiEvBMM6J5").click()""")
    #         self.repeat_status = 2
    #         print(Fore.GREEN + Style.BRIGHT + "Spotify - repeat_track: " + Style.NORMAL + Fore.WHITE + "successful")
    #         return "повтор трека включен"
    #     except Exception as err:
    #         print(Fore.GREEN + Style.BRIGHT + "Spotify - repeat_track: " + Style.NORMAL + Fore.RED + str(err))
    #         return "При выполнение функции произошла ошибка"

    def next_track(self, text=None):
        try:
            self.browser.execute_script("""document.querySelector(".ARtnAVxkbmzyEjniZXVO").click()""")
            elements = self.browser.find_elements(By.CLASS_NAME, "h4HgbO_Uu1JYg5UGANeQ")
            threading.Event().wait(0.1)
            try:
                if elements[0] == self.browser.find_element(By.CLASS_NAME, "iSbqnFdjb1SuyJ3uWydl"):
                    print(Fore.GREEN + Style.BRIGHT + "Spotify - next_track: " + Style.NORMAL + Fore.WHITE + "successful")
                    print(self.repeat_status)
                    if self.repeat_status == 0:
                        self.music_status = 0
                        return "Плейлист закончился"
                    else:
                        return "следущий трек включен"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "Spotify - next_track: " + Style.NORMAL + Fore.WHITE + "successful")
                    return "следущий трек включен"
            except:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - next_track: " + Style.NORMAL + Fore.WHITE + "successful")
                return "следущий трек включен"

        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - next_track: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    def previous_track(self, text=None):
        try:
            self.browser.execute_script("""document.querySelector(".FKTganvAaWqgK6MUhbkx").click()""")
            threading.Event().wait(0.3)
            self.browser.execute_script("""document.querySelector(".FKTganvAaWqgK6MUhbkx").click()""")
            print(Fore.GREEN + Style.BRIGHT + "Spotify - previous_track: " + Style.NORMAL + Fore.WHITE + "successful")
            return "Предыдущий трек включен"
        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - previous_track: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    def change_status_music(self):
        try:
            self.browser.execute_script("""
            if (document.querySelector(".A8NeSZBojOQuVvK4l1pS").ariaLabel === "Слушать") { throw "err"}""")
            self.music_status = 1
        except:
            self.music_status = 0

    def play(self, text=None):
        try:
            self.change_status_music()
            if self.music_status == 0:
                self.browser.execute_script("""document.querySelector(".A8NeSZBojOQuVvK4l1pS").click()""")
                self.music_status = 1
                print(Fore.GREEN + Style.BRIGHT + "Spotify - play: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Музыка включена"
            else:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - play: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Музыка уже включена"
        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - play: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    def pause(self, text=None):
        try:
            self.change_status_music()
            if self.music_status == 1:
                self.browser.execute_script("""document.querySelector(".A8NeSZBojOQuVvK4l1pS").click()""")
                self.music_status = 0
                print(Fore.GREEN + Style.BRIGHT + "Spotify - pause: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Музыка остановлена"
            else:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - pause: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Музыка уже остановлена"
        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - pause: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    def is_liked(self):
        try:
            self.browser.execute_script("""
            a = document.querySelector(".control-button-heart").classList
            if (a[3] == "rRF_r7EyCHjZv058JACi") { throw "err" }""")
            return False
        except:
            return True

    def like(self, text=None):
        try:
            liked = self.is_liked()
            if liked is True:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - like: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Этот трек уже добавлен в избранное"
            else:
                self.browser.execute_script("""document.querySelector(".control-button-heart").click()""")
                print(Fore.GREEN + Style.BRIGHT + "Spotify - like: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Трек добавлен в избранное"

        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - like: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

    def dislike(self, text=None):
        try:
            liked = self.is_liked()
            if liked is True:
                self.browser.execute_script("""document.querySelector(".control-button-heart").click()""")
                print(Fore.GREEN + Style.BRIGHT + "Spotify - dislike: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Трек удалён из избранного"
            else:
                print(Fore.GREEN + Style.BRIGHT + "Spotify - dislike: " + Style.NORMAL + Fore.WHITE + "successful")
                return "Этот трек ещё не добавлен в избранное"
            
        except Exception as err:
            print(Fore.GREEN + Style.BRIGHT + "Spotify - dislike: " + Style.NORMAL + Fore.RED + str(err))
            return "При выполнение функции произошла ошибка"

# music = YandexMusic()
# music.shuffle()
# threading.Event().wait(1)
# # music.play_pause()
# threading.Event().wait(1)
# music.play_favourite()

# time.sleep(10)

# def music_browser_start():
#     global m_br, actionChains
#     # opts = FirefoxOptions()
#     # opts.headless = True
#     m_br = Firefox(r"D:\python project\GeekBrains\voicemanager\MyScripts\drivers\geckodriver.exe")
#     m_br.get("https://open.spotify.com/")
#     print(1)
#     # if "Chrome" == "Chrome":
#     #     br_opts = ChromeOptions()
#     #     br_opts.add_argument(f"--user-data-dir={path}")
#     #     br_opts.headless = True
#     #     br_opts.add_argument("--unmute-audio")
#     #     m_br = Chrome("drivers/chromedriver.exe", options=br_opts)
#     #     actionChains = ActionChains(m_br)
#     #     m_br.maximize_window()
#     #     m_br.get("https://open.spotify.com/")
#
#
# def play_my_favourite_playlist():
#     global m_br
#     m_br.get("https://open.spotify.com/collection/tracks")
#
#     button_start_music = None
#     while not button_start_music:
#         try:
#             button_start_music = m_br.find_elements_by_class_name('_47lzH_9ZSVGM4UUdX90')[1]
#             button_start_music.click()
#             print("Favourite playlist started")
#         except: continue
#
#
# def next_track():
#     global m_br
#     m_br.execute_script("""document.querySelector(".nCpaRcGYhTBxygEV_tLd").click()""")
#     print("Next track")
#
#
# def last_track():
#     global m_br
#     m_br.execute_script("""document.querySelector(".L4O7J5ORFBAJ8bEMYXCi").click()""")
#     m_br.execute_script("""document.querySelector(".L4O7J5ORFBAJ8bEMYXCi").click()""")
#     print("Last track")
#
#
# def remove_repeat():
#     try:
#         m_br.execute_script("""document.querySelector(".LGeyjw_GB3ErqpcSNtX3").click()""")
#         threading.Event().wait(0.3)
#         m_br.execute_script("""document.querySelector(".LGeyjw_GB3ErqpcSNtX3").click()""")
#         return 0
#     except:
#         return 0
#
#
# def repeat_track():
#     remove_repeat()
#     # actionChains.double_click(m_br.find_element(By.CLASS_NAME, "enINDdBnsAC2KVIJckWK")).perform()
#     # m_br.find_element(By.CLASS_NAME, "enINDdBnsAC2KVIJckWK").click()
#     threading.Event().wait(0.3)
#     m_br.execute_script("""document.querySelector(".enINDdBnsAC2KVIJckWK").click()""")
#     threading.Event().wait(0.3)
#     m_br.execute_script("""document.querySelector(".LGeyjw_GB3ErqpcSNtX3").click()""")
#     # m_br.execute_script("""document.querySelector(".LGeyjw_GB3ErqpcSNtX3").click()""")
#     print("Track repeating")
#
#
# music_browser_start()
# time.sleep(4)
# play_my_favourite_playlist()
# # next_track()
# time.sleep(2)
# # repeat_track()

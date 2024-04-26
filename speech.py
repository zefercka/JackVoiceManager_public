# -*- coding: utf8 -*-

import json
import os
import subprocess
import threading
import time  # для тестов

import joblib
import pyaudio
import pyttsx3
import simpleaudio
import speech_recognition as sr  # Распознование онлайн
from colorama import Fore, Style
from vosk import KaldiRecognizer, Model  # Распознование оффлайн

import config
import data_exchange
import execute_command as ec
import music
import UC

r = sr.Recognizer()

engine = pyttsx3.init()

model = Model("model_ru")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

voices = engine.getProperty('voices')

vectorizer = joblib.load("vectorizer.pkl")
classifier = joblib.load("model1.pkl")
classes = list(classifier.classes_)   # классы в модели

listening = 0 # Для остановки прослушивания
# for voice in voices:
#     print(voice, voice.id)
#     engine.setProperty('voice', voice.id)
#     engine.say("Hello World!")
#     engine.runAndWait()
#     engine.stop()

engine.setProperty('voice', voices[1].id)
spotify = music.Spotify()
song_start = simpleaudio.WaveObject.from_wave_file(r"Sounds\SoundStart.wav")


hotwords = ("джек слушай", "джек привет", 'привет джек', 'слушай джек', 'привет жек', 'слушай жек', 'жек привет',
            'джек', 'жек', 'джеки', 'джеки привет', 'жеки', 'жеки привет', 'привет жеки')


commands = {
    "google_search": ec.google_search_def,
    "weather": ec.weather_request,
    "time": ec.time_request,
    "notification": ec.notification,
    "screenshot": ec.create_screenshots,
    "play_favourite": spotify.play_favourite,
    "pause": spotify.pause,
    "play": spotify.play,
    "repeat": spotify.repeat,
    "next_track": spotify.next_track,
    "previous_track": spotify.previous_track,
    "shuffle": spotify.shuffle,
    "like": spotify.like,
    "dislike": spotify.dislike,
    "route": ec.create_route,
    "exchange": ec.exchange,
}

print("work")

def get_command(text_):  # Определение команды
    global spotify

    time_start = time.time()
    print(text_)
    if text_ in UC.commands:
        # print(UC.commands[text_])
        os.system(f'\"{UC.commands[text_]}\"')
        print(Fore.BLUE + Style.BRIGHT + "speech - get_command (time): " + Style.NORMAL + str(time.time() - time_start))

    else:
        command_rtr = classifier.predict(vectorizer.transform([text_]))[0]
        ind = classes.index(command_rtr)
        per = classifier._predict_proba_lr(vectorizer.transform([text_]))[0][ind]   # процент совпадения команды
        print(per)

        # print(Fore.BLUE + "speech - get_command (text): " + str(text))
        print(Fore.BLUE + "speech - get_command (time): " + str(time.time() - time_start))
        if per >= 0.09:
            if (command_rtr in config.music_commands) and (spotify.started is False):
                spotify.start_browser()
                rtr = commands[command_rtr](text_)
            else:
                rtr = commands[command_rtr](text_)

            say(rtr, False)
        
        else:
            say("Я ещё так не умею", False)


def command():
    if ec.ntn.stopped == 1:
        if config.method_recognition == 0:
            with sr.Microphone() as source:
                r.pause_threshold = 1

                song_start.play()

                audio = r.listen(source)

            try:
                action = r.recognize_google(audio, language="ru_RU").lower()
                print(action)
                get_command(action)
                return 0

            except Exception as err:
                print(err)
                say("Я вас не понял, попробуйте ещё раз", False)
                return 0

        else:
            try:
                song_start.play()
                stream.start_stream()

                while True:
                    data = stream.read(4000)

                    if len(data) == 0:
                        break

                    if rec.AcceptWaveform(data):
                        x = json.loads(rec.Result())
                        text = x['text']
                        print(text)
                        get_command(text)
                        break
                    else:
                        pass

                return 0

            except Exception as err:
                print(err)
                return 0


def say(words, listen):
    engine.say(words)
    engine.runAndWait()

    if listen is True:
        command()

    return 0


def wait_hotwords():
    print("work")
    try:
        stream.start_stream()
        while True:
            data = stream.read(4000)

            if len(data) == 0:
                break

            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())['text']

                if text.startswith(hotwords):
                    command()

            else:
                pass

    except Exception as err:
        print(err)


def listen_speech_new_command():
    global listening
    if listening == 1:
        if config.method_recognition == 0:
            r = sr.Recognizer()

            with sr.Microphone() as source:
                r.pause_threshold = 1

                song_start.play()

                audio = r.listen(source)

            try:
                action = r.recognize_google(audio, language="ru_RU").lower()

                data_exchange.say_command_text = action
                listening = 0

                return 0

            except:
                say("Я вас не понял, повторите после звукового сигнала", False)
                listen_speech_new_command()

        else:
            try:
                song_start.play()

                stream.start_stream()
                while listening == 1:
                    data = stream.read(4000)

                    if len(data) == 0:
                        break

                    if rec.AcceptWaveform(data):
                        x = json.loads(rec.Result())

                        data_exchange.say_command_text = x['text']

                        return 0
                    else:
                        pass
                else:
                    x = json.loads(rec.Result())

                    data_exchange.say_command_text = x['text']
                    listening = 0
            except Exception as err:
                print(err)

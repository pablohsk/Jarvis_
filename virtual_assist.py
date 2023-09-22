import pyttsx3
import random
import os
import datetime
import schedule
import time
import json
import playsound
import pygame.mixer
import speech_recognition as sr
import requests
import spotipy
from django.contrib.admin.templatetags.admin_list import results
from spotipy.oauth2 import SpotifyOAuth
from gtts import gTTS
from pytube import YouTube
from myapp.google import search_on_google
from myapp.news import News
from myapp.reminders import Reminder


class VirtualAssistant:
    def __init__(self, assistant_name, person):
        self.person = person
        self.assistant_name = assistant_name
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.voice_data = ''

    def engine_speak(self, audio_string):
        audio_string = str(audio_string)
        tts = gTTS(text=audio_string, lang='en')
        r = random.randint(1, 2000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Aguarde a reprodução do áudio terminar
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        # Aguarde um segundo após o término da reprodução antes de tentar excluir o arquivo
        time.sleep(1)

        # Agora, tente excluir o arquivo
        try:
            os.remove(audio_file)
        except Exception as e:
            print(f"Error deleting audio file: {e}")

        print(self.assistant_name + ':', audio_string)

    def record_audio(self, ask=""):
        with sr.Microphone() as source:
            if ask:
                self.engine_speak(ask)
                print("Recording")

            audio = self.r.listen(source, 4, 4)
            print('looking at the data base')

            try:
                self.voice_data = self.r.recognize_google(audio)
            except sr.UnknownValueError:
                self.engine_speak(f"Sorry {self.person}, I can't understand what you said, please repeat")
            except sr.RequestError:
                self.engine_speak("Sorry, I can't connect to the server")

            print(">>", self.voice_data.lower())
            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    def there_exist(self, terms):
        for term in terms:
            if term in self.voice_data:
                return True

    def get_weather_data(self, location):
        api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric",  # Unidade de temperatura em Celsius
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            return None

    def get_spotify_data(self, query):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET',
                                                       redirect_uri='YOUR_REDIRECT_URI',
                                                       scope='playlist-modify-public,user-library-modify,user-library-read,user-read-playback-state,user-modify-playback-state'))

        # Implemente ações do Spotify com base no comando de voz (query)
        # Exemplo: results = sp.search(q=query, type='track', limit=1)

        return results

    def get_reminders_data(self):
        reminder = Reminder()  # Instancie a classe Reminder
        reminder.load_reminders()

        # Implemente a obtenção de lembretes a partir da instância do Reminder
        reminders = reminder.get_events()

        return reminders

    def get_news_data(self):
        news = News()  # Instancie a classe News
        news.fetch_headlines()

        # Implemente a obtenção de notícias a partir da instância do News
        news_headlines = news.articles

        return news_headlines

    def get_youtube_data(self, query):
        yt_results = []

        # Pesquise vídeos no YouTube usando a biblioteca pytube
        try:
            search_results = YouTube.search(query)

            for video in search_results:
                video_title = video.title
                video_url = video.url
                yt_results.append({'title': video_title, 'url': video_url})

            return yt_results
        except Exception as e:
            print(f"Error searching on YouTube: {e}")
            return None

    def respond(self):
        if self.there_exist(['hey', 'hi', 'hello', 'oi', 'holla']):
            greetings = [f'Hi {self.person}, how can I help you?',
                         'Hi, what do you want to do now?',
                         'I am here to assist you!']
            greet = greetings[random.randint(0, len(greetings) - 1)]
            self.engine_speak(greet)

        elif self.there_exist(['get weather', 'weather', 'tell me the weather']):
            self.engine_speak("Sure, where would you like to know the weather?")
            location = self.record_audio('Please tell me the location:')
            weather_data = self.get_weather_data(location)
            if weather_data:
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                self.engine_speak(
                    f"The weather in {location} is {description} with a temperature of {temperature} degrees Celsius.")
            else:
                self.engine_speak("Sorry, I couldn't fetch the weather data.")

        elif self.there_exist(['play music', 'music', 'play a song']):
            self.engine_speak("Sure, what song would you like to play?")
            query = self.record_audio('Please tell me the song name:')
            spotify_data = self.get_spotify_data(query)
            if spotify_data:
                # Implemente a lógica para controlar o Spotify com base nos dados recebidos
                pass
            else:
                self.engine_speak("Sorry, I couldn't find the song.")

        elif self.there_exist(['reminders', 'show my reminders', 'list reminders']):
            reminders_data = self.get_reminders_data()
            if reminders_data:
                self.engine_speak("Here are your reminders:")
                for i, reminder in enumerate(reminders_data):
                    self.engine_speak(f"Reminder {i + 1}: {reminder}")
            else:
                self.engine_speak("You have no reminders.")

        elif self.there_exist(['news', 'tell me the news', 'latest news']):
            news_data = self.get_news_data()
            if news_data:
                self.engine_speak("Here are the latest headlines:")
                for i, article in enumerate(news_data):
                    self.engine_speak(f"Headline {i + 1}: {article}")
            else:
                self.engine_speak("Sorry, I couldn't find any news.")

        elif self.there_exist(['search on youtube', 'youtube', 'find video']):

            self.engine_speak("What video would you like to search for on YouTube?")

            query = self.record_audio('Please tell me the video title:')

            # Chama a função get_youtube_data para obter resultados do YouTube

            youtube_data = self.get_youtube_data(query)

            if youtube_data:

                # Implemente a lógica para mostrar resultados do YouTube

                for i, result in enumerate(youtube_data):
                    title = result['title']

                    url = result['url']

                    self.engine_speak(f"Result {i + 1}: {title}. You can watch it at {url}")

            else:

                self.engine_speak("Sorry, I couldn't find any YouTube videos.")

        elif self.there_exist(['search on google', 'google', 'find information']):

            self.engine_speak("What would you like to search for on Google?")

            query = self.record_audio('Please tell me your query:')

            google_data = search_on_google(query)

            if google_data:

                # Implemente a lógica para mostrar resultados do Google

                for i, result in enumerate(google_data):
                    self.engine_speak(f"Result {i + 1}: {result}")

            else:

                self.engine_speak("Sorry, I couldn't find any information on Google.")


if __name__ == "__main__":
    assistant = VirtualAssistant('Jarvis', 'Pablo')
    while True:
        voice_data = assistant.record_audio('Listening...')
        assistant.respond()
        if assistant.there_exist(['bye', 'goodbye', 'see you', 'see you later', 'see you']):
            assistant.engine_speak(f"You're welcome {assistant.person}. Goodbye!")
            break

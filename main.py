import datetime
import os
import sys
import pyautogui
import time
import webbrowser
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences  # type: ignore
import random
import numpy as np
import psutil

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")  # initialize
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

engine = initialize_engine()  # Initialize the engine once

def speak(text):
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.....", end="", flush=True)
        r.pause_threshold = 1.5
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment = 2
        r.energy_threshold = 4000
        r.phrase_time_limit = 10
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="", flush=True)
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    day_of_week = day_dict.get(day, "Unknown day")
    print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()
    if(hour >= 0) and (hour <= 12) and ('AM' in t):
        speak(f"Good Morning Master, it's {day} and the clock ticks at {t}")
    elif(hour >= 12) and (hour <= 16) and ('PM' in t):
        speak(f"Good Afternoon Master, it's {day} and the clock ticks at {t}")
    else:
        speak(f"Good Evening Master, it's {day} and the clock ticks at {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening whatsapp for you")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening discord server for you")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening instagram for you")
        webbrowser.open("https://instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Master, today's schedule is")
    week = {
        "monday": "today u have project 2 lab, biology lecture and Indian Knowledge system class in first half and then the electives in second half",
        "tuesday": "today u have biology and Indian Knowledge System class in first half and then ML lab in second half",
        "wednesday": "today u have all the three electives in the second half",
        "thursday": "today u have only Mobile Computing Class",
        "friday": "today u have summer training lab in first half and two electives in second half",
        "saturday": "today is reserved for extra-curricular activities"
    }
    speak(week.get(day, "No schedule available for today"))

def openApp(command):
    if "calculator" in command:
        speak("Opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("Opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("Opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')
    else:
        speak("Sorry, I can't open that application")

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')
    else:
        speak("Sorry, I can't close that application")
    
def  browsing(query):
    if 'google' in query:
        speak("What should I search for you master.....")
        s=command().lower()
        webbrowser.open(f"{s}")
    elif 'edge' in query:
        speak("What should I search for you master.....")
        os.startfile('C:\\Users\\Public\\Desktop\\Microsoft Edge.lnk')

def condition():
    usage=str(psutil.cpu_percent())
    speak(f"CPU is at{usage} percentage")
    battery=psutil.sensors_battery()
    percentage=battery.percent
    speak(f"Our system has {percentage} percentage battery")

    if percentage>=80:
        speak("We have enough charging to get things done")
    elif percentage>=40 and percentage<=80:
        speak("If available please connect charger,otherwise we can still go for some time")
    else:
        speak("Master, we have low battery. I suggest you to connect a charger immediately")

if __name__ == "__main__":
    wishMe()
    while True:
        query=command().lower()
        #query = input("Enter your command->")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif("university time table" in query) or ("schedule" in query):
            schedule()
        elif("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("volume increased")
        elif("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("volume decreased")
        elif("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("volume muted")
        elif("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
        
        elif("open google" in query) or ("open edge" in query):
            browsing(query)
        elif("system conditions" in query) or ("condition of system" in query):
            speak("checking the system conditions")
            condition()
        elif "exit" in query:
            sys.exit()
#speak("Hello, I am Neo")
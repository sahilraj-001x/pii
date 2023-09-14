import speech_recognition as sr
from playsound import playsound
import re
import pyttsx3

engine = pyttsx3.init()
# engine.setProperty('rate', 160)
# engine.setProperty('volume', 0.7)
# voices = engine.getProperty("voices")
# engine.setProperty('voice', voices[10].id)

r = sr.Recognizer()
def actions():
    while True:
        try:
            with sr.Microphone() as source:
                print("Talk")
                audio_text = r.listen(source, phrase_time_limit=5)
                command = r.recognize_google(audio_text)
                break
        except:
            engine.say("Please repeat again, I did not get it")
            engine.runAndWait()
    return command

def hindi():
    playsound('questions_lang/hindi/hi_q1.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/hindi/hi_q2.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/hindi/hi_q3.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/hindi/hi_q4.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/hindi/hi_q5.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/hindi/hi_q6.mp3')
    command = actions()
    print(command)

def bengali():
    playsound('questions_lang/bengali/bn_q1.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/bengali/bn_q2.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/bengali/bn_q3.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/bengali/bn_q4.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/bengali/bn_q5.mp3')
    command = actions()
    print(command)
    playsound('questions_lang/bengali/bn_q6.mp3')
    command = actions()
    print(command)

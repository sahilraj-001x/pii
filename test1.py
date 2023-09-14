import speech_recognition as sr
import pyttsx3
from questions import *
from playsound import playsound

r = sr.Recognizer()
engine = pyttsx3.init()
# engine.setProperty('rate', 160)
# engine.setProperty('volume', 0.7)
# voices = engine.getProperty("voices")
# engine.setProperty('voice', voices[10].id)


def talk(say):
    engine.say(say)
    engine.runAndWait()

def actions():
    while True:
        try:
            with sr.Microphone() as source:
                print("Talk")
                audio_text = r.listen(source)
                command = r.recognize_google(audio_text)
                break
        except:
            talk("Please repeat again, I did not get it")
    return command

def run():
    while True:
        talk("Please select your language")
        command = actions().lower()
        print(command)
        if "hindi" in command:
            print("hindi")
            hindi()
        elif "bengali" in command:
            print("bengali")
            bengali()
        elif "quit" or "Quit" or "QUIT" in command:
            break
        else:
            talk("Please chose a different language, your language is still not added to our system")
run()
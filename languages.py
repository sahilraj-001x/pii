import pyttsx3
from gtts import gTTS
from playsound import playsound

# converter = pyttsx3.init()
# converter.setProperty('rate', 150)
# converter.setProperty('volume', 0.7)
# voices = converter.getProperty("voices")
# converter.setProperty('voice', voices[41].id)
#
# converter.say("आपका नाम क्या है")
# converter.runAndWait()

import os

mytext = 'what is you name'

bn_q1 = "আপনার নাম কি"
bn_q2 = "আপনার বয়স কত"
bn_q3 = "আপনার জন্মদিন কবে"
bn_q4 = "আপনার ফোন নম্বর কি"
bn_q5 = "আপনার সম্পূর্ণ ঠিকানা কি"
bn_q6 = "আপনার পিনকোড কি"

hi_q1 = "आपका नाम क्या है"
hi_q2 = "आपकी उम्र क्या हैं"
hi_q3 = "कृपया अपनी जन्मतिथि बताएं"
hi_q4 = "कृपया अपना फोन नंबर बताएं"
hi_q5 = "कृपया अपना पूरा पता बताएं"
hi_q6 = "कृपया अपना पिनकोड बताएं"

gu_q1 = "કૃપા કરીને મને તમારું નામ જણાવો"
gu_q2 = "તમારી ઉંમર કેટલી છે"
gu_q3 = "તમારો જન્મદિવસ શું છે"
gu_q4 = "કૃપા કરીને મને તમારો ફોન નંબર જણાવો"
gu_q5 = "કૃપા કરીને તમારું સંપૂર્ણ સરનામું આપો"
gu_q6 = "તમારો પિનકોડ શું છે"

ma_q1 = "तुझं नाव काय आहे"
ma_q2 = "तुमचे वय काय आहे"
ma_q3 = "तुमचा वाढदिवस काय आहे"
ma_q4 = "तुमचा फोन नंबर काय आहे"
ma_q5 = "कृपया तुमचा पत्ता सांगा"
ma_q6 = "कृपया तुमचा पिनकोड सांगा"

uk_q1 = "তোকামার নাকপাম কিকপি"
uk_q2 = "তোকপমার বপथ़স ককপত"
uk_q3 = "তোকামার ফোকপন লকপামবার কিকপি"
uk_q4 = "তোকামার ঠিকপিকানা কিকপি"
uk_q5 = "তোকপমার পিকপিন নাকগামবার কিকপি"

mar_q1 = "आपरो नाम कई हैँ"
mar_q2 = "आपरी उम्र कई है"
mar_q3 = "कृपया आपरो फ़ोन नंबर डेओ"
mar_q4 = "आपरो पुरो पतों कई है"
mar_q5 = "आपरो पिनकोड कई है"

# Language in which you want to convert
language = 'gu'
myobj = gTTS(text=gu_q6, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("questions_lang/gujarati/gu_q6.mp3")


# # Playing the converted file
playsound('questions_lang/gujarati/gu_q6.mp3')
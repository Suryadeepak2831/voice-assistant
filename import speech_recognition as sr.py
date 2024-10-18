import speech_recognition as sr
import pyttsx3
from datetime import datetime
import requests

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an error with the service.")
            return ""

def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}.")

def tell_date():
    today = datetime.today()
    current_date = today.strftime("%B %d, %Y")
    speak(f"Today's date is {current_date}.")

def search_web(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    data = response.json()
    if 'RelatedTopics' in data and data['RelatedTopics']:
        results = data['RelatedTopics'][0]['Text']
        speak(f"Here is what I found: {results}")
    else:
        speak("I couldn't find any information on that.")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()

        if 'hello' in command:
            speak("Hello! How can I help you?")
        elif 'time' in command:
            tell_time()
        elif 'date' in command:
            tell_date()
        elif 'search' in command:
            query = command.replace('search', '').strip()
            if query:
                search_web(query)
            else:
                speak("What would you like me to search for?")
        elif 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't catch that. Could you repeat it?")

if _name_ == "_main_":
    main()
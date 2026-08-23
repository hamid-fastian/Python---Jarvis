import speech_recognition as sr
import webbrowser
import pyttsx3 # text to speech
import musiclibrary
import requests
import wikipedia
from datetime import datetime
import platform

r=sr.Recognizer()
newsapi="d3357780881a44eda7c3bee686874ea8"

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processcommand(c):
    
    # Open Websites
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)

    # NEWS HEADLINS
    elif "news" in c.lower():
        speak("Here are the latest news headlines")
        r=requests.get(f"https://newsapi.org/v2/everything?q=Pakistan&sortBy=publishedAt&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles=data.get('articles',[])

            for index,article in enumerate(articles[:5]):
                print(f"{index+1}.{article['title']}")
                speak(article['title'])
        else:
            print("Error:", r.status_code)
    
    # Time and Date
    elif "time" in c.lower() or "date" in c.lower():
        a=datetime.now()
        d=str(a).split(" ")
        print(f"Date: {str(d[0])}")
        print(f"Time: {str(d[1])}")

    # Weather Check
    elif "weather" in c.lower():
        li=c.split(" ")
        city=li[4]
        url=f"https://wttr.in/{city}?format=3" 
 
        response=requests.get(url) 
        if(response.status_code==200): 
            print(f"{response.text}") 
        else: 
            print("Could not fetch weather data.") 
 
    # System Information 
    elif "system" in c.lower(): 
        print("") 
        print("System:", platform.system()) 
        print("Release:", platform.release()) 
        print("Version:", platform.version()) 
        print("Machine:", platform.machine()) 
        print("Processor:", platform.processor()) 
        print("") 
 
    # Wikipedia Search     
    else: 
        query = c.lower() 
 
        try: 
            result = wikipedia.summary(query, sentences=2) 
            print(result) 
            speak(result) 
 
        except wikipedia.exceptions.DisambiguationError: 
            speak("There are multiple results. Please be more specific.") 
 
        except wikipedia.exceptions.PageError: 
            speak("I could not find information about that topic.") 


if __name__=="__main__":  
    speak("Initializing Jarvis......") 
    while True: 
        # listen for the word "jarvis" 
        r = sr.Recognizer() 
        try: 
           with sr.Microphone() as source: 
                print("Listening......") 
                audio = r.listen(source, timeout=2, phrase_time_limit=2) 
           word = r.recognize_google(audio) 
           if(word.lower() == "jarvis"): 
                speak("Ya") 
               # listen for command 
                with sr.Microphone() as source: 
                    print("Jarvis Active......") 
                    audio = r.listen(source) 
                    command = r.recognize_google(audio) 
                     
                    processcommand(command) 
        except Exception as e: 
            print("Error; {0}".format(e)) 
 

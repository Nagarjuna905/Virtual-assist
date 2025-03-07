import speech_recognition as sr
import webbrowser
import datetime
from gtts import gTTS
import pygame
import os
import pyttsx3
from musiclibrary import music  

#initilize recognize , pygame mixer and pyttsx3
recognizer = sr.Recognizer()
pygame.mixer.init()
engine = pyttsx3.init()


# Function to convert text to speech using through pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to convert text to speech
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Function to stop music
def stop_music():
    print("Stopping music...")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        speak("Music stopped.")
    else:
        print("No music is currently playing.")
        speak("No music is currently playing.")


# Function to process commands
def processCommand(c):
    print(f"Recognized command: {c}")
    if "hello" in c.lower():
        speak("Hello! How can I assist you today?")
    elif "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "time" in c.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "stop music" in c.lower():
        stop_music()
    elif c.lower().startswith("play"):
        # Extract the song name from the command
        song_name = c.lower().replace("play", "").strip()
        if song_name in music:
            speak(f"Playing {song_name}.")
            webbrowser.open(music[song_name])
        else:
            speak(f"Sorry, I don't have {song_name} in my library.")
    elif "exit" in c.lower() or "quit" in c.lower():
        speak("Goodbye! Have a great day.")
        exit()
    else:
        speak("Say it again!")

# Main function
if __name__ == "__main__":
    speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
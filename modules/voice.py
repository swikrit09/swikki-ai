# import pyttsx3
# import speech_recognition as sr

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = recognizer.listen(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "Error: Sorry, I did not understand that."
#     except sr.RequestError:
#         return "Error: Could not request results; check your network connection."
    
# def stop_listening():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("Listening stopped.")
#         return "Listening stopped."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

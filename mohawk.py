import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

#Name of this Voice Assistant is Mohawk

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#There are 2 voices, voices[0] is david, which is male voice and voices[1] is zira, which is female voice
# print(voices) 
# print(voices[0].id)
#Set only 1 voice either male or female
engine.setProperty('voice', voices[0].id)

#Create a dictionary , which is a mapping b/w the user name and its email id. This will be used in send_email()
mail_dict = {"<User 1>" : "<Email id for User 1>",
             "<User 2>" : "<Email id for User 2>",
             "<User 3>" : "<Email id for User 3>" }

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour < 12:
        speak("Good Morning!!")

    elif hour >= 12 and hour <18:
        speak("Good Afternoon!")
    
    else:
        speak("Good Evening!")

    speak("Mohawk at your service sir")

def take_cmd():
    """ It takes voice input from microphone and returns text string output """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting background noise, 1 sec")
        #pause_threshold = 1 means say you want to say Housefull, now you say House and within 1 sec, you say full, so it will treat Housefull as a single word
        #if you say house and after more than 1 sec, you say full then it will treat it as 2 separate words house and full.
        r.pause_threshold = 1
        r.energy_threshold = 50
        r.adjust_for_ambient_noise(source, duration = 1)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query =  r.recognize_google(audio, language='en-in')
        print(f"User Said:{query}\n")

    except:
        print("Sorry, Please say that again")
        return "None"
    
    return query

def send_email(to, content):
    #Before doing below, 1st step is to enable less secure apps in the gmail account from which you will be sending the mail. 
    # If you don't enable less secure apps, you can't send mail from here. Once you enable less secure apps proceed below
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("<Email id from which email will be sent>", "<Password>")
    server.sendmail("<Email id from which email will be sent>", to, content)
    server.close()

if __name__ == "__main__":
    wish()
    #Speak as soon as you see the message Adjusting background noise 1sec and before Listening message comes
    while True:
        query = take_cmd().lower()
        if "shutdown" in query:
            speak("Thank you Sir, Shutting down")
            break
            
        if "wikipedia" in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 1)
            print(results)
            speak("According to wikipedia")
            speak(results)  

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "play music" in query:
            #Give \\ in directory , where 1st \ is an escape sequence to allow 2nd \ in the string
            music_dir = "<Music Directory path>"

            #listdir will convert all the contents in the directory into a list
            songs = os.listdir(music_dir)

            #Print all the songs in the directory
            print(songs)

            #Here music_dir refers to the song directory, thus use os.path.join below. If music_dir refers to the song itself, don't use os.path.join
            #Also if we are playing the 1st song in the directory, write songs[0]
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {time}")

        elif "open visual studio" in query:
            app_path = "<Visual studio exe path>"

            #Here we are directly giving the application path of the exe file and not the directory path, so no need to use os.path.join below
            os.startfile(app_path)

        elif "joke" in query:
            speak("Am i a joke to you?")

        elif "alexa" in query:
            speak("She is a good friend of mine")

        elif "yourself" in query:
            speak("I was built by Sayantan , who is a bit boring guy as compared to me. I am awesome and never try to mess with me by asking to tell jokes")

        elif "email to" in query:
            list = query.split(' ')
            word = list[-1]
            mail = mail_dict[word]
            print(mail)
            try:
                speak("What should I write")
                content = take_cmd()
                send_email(mail,content)
                speak("Email has been sent successfully")
            except Exception as e:
                print(e)
                speak("Sorry Email can't be sent")






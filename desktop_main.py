import speech_recognition
import speech_recognition as ever
import pyaudio
import pyttsx3
import random
import requests
import webbrowser
import datetime
import sqlite3
import yagmail
import string
import math
import os
import wikipedia
from misc import state_codes, greetings
import subprocess
from twilio.rest import Client


def speak(text):
    """main function that you call when you want the assistant to speak"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    """main function that you call when you want to get your audio command"""
    record = ever.Recognizer()
    with ever.Microphone() as source:
        audio = record.listen(source)
        said = ''

        try:
            said = record.recognize_google(audio)
            print(said)     # remove after testing
        except Exception as e:
            print("Excetion: " + str(e))
    return said.lower()


def open_web(command):
    """main function that allows to open the web with given command 'open up google.com'"""
    # TODO maybe we can put some logic in here that determines 'open web' or 'open folder'
    remove_open = str(command.split('go to'))
    speak("Opening" + remove_open)
    url = f'http://{command}'
    edited = url.split('go to')
    p1 = edited[0]
    p2 = edited[1]
    p3 = p1 + p2
    p4 = p3.replace(' ', '')
    webbrowser.open_new(p4)
    speak(remove_open + "opened")


def tell_time():
    """simple function that takes in user voice input request to know the current time and returns current time"""
    time = datetime.datetime.now().strftime('%I:%M %p')
    speak(time)


def get_weather(command):
    """main function that takes user voice input and uses OpenWeather API to return current weather for user input"""
    weather_phrases = "how is the weather in"
    country_code = +1
    api_key = os.environ.get('weather_api_key')
    new_variable = ''
    final = ''
    summary = ''
    get_code = ''
    url = ''
    city_name = ''
    final_city = ''
    if weather_phrases in command:
        new_variable = command.split(weather_phrases)
        cut_index = new_variable[1]
        final = str(cut_index.lstrip())

    new = final.split(' ')
    for i in new:
        if i in state_codes.keys():
            get_code = state_codes[i]
            city_name = final
            if len(new) == 3:
                city_name2 = new[0]
                city_name3 = new[1]
                final_city = city_name2 + '%20' + city_name3
            elif len(new) == 2:
                final_city = new[0]

    url = f'https://api.openweathermap.org/data/2.5/weather?q={final_city}&{get_code}&{country_code}&appid={api_key}&units=imperial'
    data = requests.get(url)
    content = data.json()

    # TODO just run the fucking thing
    overcast = content["weather"][0]["description"]
    name = content['name']
    temps = int(content['main']['temp'])
    humidity = content['main']['humidity']

    summary = f"The current weather in {name} is {temps} degrees, with an overcast of {overcast}, and the humidity is {humidity} percent"
    speak(summary)


def wiki(command):
    """main function you call when you want to look up something, commands are 'who is' or 'what is' or 'what are'"""
    wiki_phrases = ['what are', 'who is', 'what is a', 'who are the', 'what is the']
    new_var = ''
    cut_index = ''
    final = ''
    for phrase in wiki_phrases:
        if phrase in command:
            new_var = command.split(phrase)
            cut_index = new_var[1]
            final = str(cut_index.lstrip())
    summary = wikipedia.summary(final, sentences=1)
    speak(summary)


def local_weather(command):
    # Function that tells the local weather.
    current_loc = 'vancouver'    # Change to your local
    api_key = os.environ.get('weather_api_key')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={current_loc}&appid={api_key}&units=imperial'
    data = requests.get(url)
    content = data.json()

    overcast = content['weather'][0]['description']
    name = content['name']
    temps = int(content['main']['temp'])
    humidity = content['main']['humidity']
    summary = f"The current weather in {name} is {temps} degrees, with an overcast of {overcast}," \
              f" and the humidity is {humidity}"
    speak(summary)


def note(command):
    def note(command):
        """function that takes a note when commanded too and adds note to new note file"""
    # TODO maybe change the file name to add time in with date

    time_filename = datetime.datetime.utcnow()
    time = datetime.datetime.now().strftime('%I-%M%p')
    convert = 'note taken-' + str(time_filename).split(' ')[0] + '.txt'   # name of the file
    destination = 'C:/Users/yklac/Desktop/Other/notes' + '/' + convert
    source = "C:/Users/yklac/Desktop/projects/ProjectEver/mainEver/" + convert
    dest = 'C:/Users/yklac/Desktop/Other/notes'

    subprocess.Popen(["notepad.exe", convert], cwd=dest)

    with open(convert, 'w') as new_file:
        new_file.write(command)

    new_file.close()
    os.rename(source, destination)


def tell_date():
    # Function that tells the date
    today = datetime.date.today()
    day = datetime.date.isoweekday(today)
    daysOfWeek = {1: "Monday",
                  2: "Tuesday",
                  3: "Wednesday",
                  4: "Thursday",
                  5: "Friday",
                  6: "Saturday",
                  7: "Sunday"
                  }
    monthsOfyear = {"01": "January", "02": "February", "03": "March", "04": "April",
                    "05": "May", "06": "June", "07": "July", "08": "August", "09": "September",
                    "10": "October", "11": "November", "12": "December"}

    month = str(today).split("-")[1]
    main_day = str(today).split('-')[2]
    end_thing = ""
    if main_day:
        end_thing = "th"
    elif main_day.endswith('3'):
        end_thing = "rd"
    elif main_day.endswith("2"):
        end_thing = "nd"
    elif main_day.endswith('1'):
        end_thing = "st"

    main_today = f"Today is {daysOfWeek[day]}, {monthsOfyear[month]} the {main_day}{end_thing}, " \
                 f"of the year {str(today).split('-')[0]}"
    speak(main_today)


def spell(command):
    """simple def that takes in user command and returns how to spell whatever word is given"""
    word = command.split(" ")[4]
    char4 = []
    for char in word:
        char4.append(char)

    main_word = ' '.join(char4)
    speak(f"you spell {word} as {main_word}")


def create_list(command):
    # function that takes in user input and creates a shopping list of that.
    # example: user says 'create new walmart list' computer then says, what would you like to add
    # then user gives a list of things they want to add
    ind = command.split(" ")
    twilio_number = "+19286837692"
    mine = os.environ.get("my_number")
    speak("What would you like to add?")
    get_items = get_audio()
    convert = get_items.split(" ")
    if "and" in convert:
        convert.remove('and')
        items = '\n'.join(convert)
        message = f"""Create New {ind[2].capitalize()} List:\n{items}"""
        account_sid = os.environ.get('twilio_account_SID')
        auth_token = os.environ.get('twilio_auth_token')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=mine
        )

        speak("Sent you the new {} list".format(ind[2]))


def send_text(command):
    # function that sends a text for the user, example: user says, send a text to Grace Random.
    # Then the computer looks into a database you have your contacts in, and retrieves the number
    # that belongs to that data and texts it, after the computer asks the user for the message
    command_split = command.split(" ")
    first_name = command_split[4].capitalize()
    last_name = command_split[5].capitalize()
    name = first_name + " " + last_name
    db = sqlite3.connect("contacts")
    phone_number = ''
    for row in db.execute("SELECT * FROM contacts WHERE first_name = ? AND last_name = ?", [first_name, last_name]):
        phone_number = row[3]
    speak("What do you want to say?")
    audio = get_audio()
    message = f"Evr AI Systems:\nMessage From Christopher:\n{audio}"

    speak(f"Your message to {name} says {audio}. Want me to send it?")
    command_ny = get_audio()

    if "yeah" or "yes" in command_ny:
        twilio_number = "+19286837692"
        account_sid = os.environ.get('twilio_account_SID')
        auth_token = os.environ.get('twilio_auth_token')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )
        speak("Message sent")
    elif "no" in command_ny:
        speak("No message was sent")


def odin_overide():
    # Odin override command triggers this function which is the function you call when you want to do something
    # like accessing a passwords database or something else. You say the command and the function gets called
    # creating a random number that is then sent to your phone, and you read it back to the function. And then
    # you can proceed with whatever. I only have one command inside this function, that's the password database search
    speak("Odin Override pass code required!")
    letters = string.ascii_uppercase
    nums = string.digits
    all2 = letters + nums
    ran = random.sample(all2, 6)
    odin_password = ''.join(ran)
    message2 = f"""Odin Override Code Request:\n\n{odin_password}"""
    twilio_number = "+19286837692"
    mine = os.environ.get('my_number')
    account_sid = os.environ.get('twilio_account_SID')
    auth_token = os.environ.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message2,
        from_=twilio_number,
        to=mine
    )
    # print(odin_password)    # TODO remove after finish
    # code_input = input("Pass Code: ").upper()
    code_input = get_audio()
    print(code_input)
    if code_input == odin_password:
        # print("Command?")   # TODO REMOVE
        speak("Command?")
        new_command = get_audio()
        # new_command = input("> ")      # TODO REMOVE
        if "whats the password for" in new_command:
            account_name = new_command.split(" ")[4]
            db = sqlite3.connect("evr_passwords.db")
            # (account_name TEXT, username TEXT, password TEXT)
            conn = db.cursor()
            info_list = []

            for row in conn.execute("SELECT * FROM evr_passwords WHERE account_name = ?", [account_name]):
                for item in row:
                    info_list.append(item)

            info = "\n".join(info_list)

            message = f"""Evr AI Systems\nOdin Override Request:\n \n{info}"""
            db.close()

            speak("Would you like me to email it or text it to you?")
            # print("Would you like me to email it or text it to you?")
            sender = get_audio()
            # sender = input("> ")    # TODO REMOVE

            if "email it" or "email" == sender:
                sender = 'evr.systems.auto@gmail.com'
                receiver = 'kirko190255@gmail.com'
                subject = 'Evr AI Systems: Odin Override: Password Info'
                paw = 'bortgdzfuhnjvisa'

                yag = yagmail.SMTP(user=sender, password=paw)
                yag.send(to=receiver, subject=subject, contents=message)

                speak("Email Sent!")

            elif "text it" or "text" == sender:
                twilio_number = "+19286837692"
                mine = "+17257260877"
                account_sid = os.environ.get('twilio_account_SID')
                auth_token = os.environ.get('twilio_auth_token')
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=message,
                    from_=twilio_number,
                    to=mine
                )
                speak("Text Sent")

        elif "whats the wifi password" in new_command:
            account_name = new_command.split(" ")[2]
            db = sqlite3.connect("evr_passwords.db")
            # (account_name TEXT, username TEXT, password TEXT)
            conn = db.cursor()
            info_list = []

            for row in conn.execute("SELECT * FROM evr_passwords WHERE account_name = ?", [account_name]):
                for item in row:
                    info_list.append(item)

            info = "\n".join(info_list)

            message = f"""Evr AI Systems\nOdin Override Request:\n \n{info}"""
            db.close()

            speak("Would you like me to email it or text it to you?")
            # print("Would you like me to email it or text it to you?")
            sender = get_audio()
            # sender = input("> ")    # TODO REMOVE

            if "email it" or "email" == sender:
                sender = 'evr.systems.auto@gmail.com'
                receiver = 'kirko190255@gmail.com'
                subject = 'Evr AI Systems: Odin Override: Password Info'
                paw = 'bortgdzfuhnjvisa'

                yag = yagmail.SMTP(user=sender, password=paw)
                yag.send(to=receiver, subject=subject, contents=message)
                speak("Email Sent!")

            elif "text it" or "text" == sender:
                twilio_number = "+19286837692"
                mine = "+17257260877"
                account_sid = os.environ.get('twilio_account_SID')
                auth_token = os.environ.get('twilio_auth_token')
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=message,
                    from_=twilio_number,
                    to=mine
                )
                speak("Text Sent")

        elif "too be used" in new_command:
            pass

        else:
            speak("Odin Override command not recognized, returning to outer loop")


def cal_fun():
    """main function that does calculation for user"""
    speak("Ready..")
    calculation = get_audio()
    broken = calculation.split(" ")
    first_number = broken[1]
    second_number = broken[3]
    operator_thing = broken[2]
    print(broken)
    result = ""
    print(operator_thing)
    if operator_thing == "*":
        result = int(second_number) * int(first_number)
        speak(f"{first_number} times {second_number} equals {result}")
    elif operator_thing == "+":
        result = int(second_number) + int(first_number)
        speak(f"{first_number} plus {second_number} equals {result}")
    elif operator_thing == "-":
        result = int(second_number) - int(first_number)
        speak(f"{first_number} minus {second_number} equals {result}")
    elif operator_thing == "/":
        result = int(second_number) // int(first_number)
        speak(f"{first_number} divided by {second_number} equals {result}")
    elif "square" in broken:
        first_number = broken[5]
        result = math.sqrt(int(first_number))
        speak(f"The square root of {first_number} is {result}")


if __name__ == "__main__":
    wake_word = 'hey ever'
    greets = random.choice(greetings)

    while True:
        print("Listening...")
        text = get_audio()

        if text.count(wake_word) > 0:
            speak(greets)
            command = get_audio()

            if 'go to' in command:
                open_web(command)

            if 'time' in command:
                tell_time()

            wiki_phrases = ['what are', 'who is', 'what is a', 'who are the', 'what is the']
            for p in wiki_phrases:
                if p in command:
                    wiki(command)

            weather_phrases = "how is the weather in"
            if weather_phrases in command:
                get_weather(command)

            weather_phrases2 = ["what is the weather outside", "how is it outside", "what's the weather"]
            for x in weather_phrases2:
                if x in command:
                    local_weather(command)

            if 'write this down' in command:
                speak("What do you want me to write down?")
                command1 = get_audio()
                note(command1)
            #
            # if "whats" or "what's" in command:
            #     calculate(command)

            if "how do you spell" in command:
                spell(command)

            if "create new" in command:
                create_list(command)

            if "what is today's date" in command:
                tell_date()

            if 'odin override' in command:
                odin_overide()

            if "send a text" in command:
                send_text(command)

            if "calculation" in command:
                cal_fun()
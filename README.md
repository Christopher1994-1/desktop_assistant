# desktop_assistant
# A simple desktop assistant

## Simple yet useful desktop assistant that you can run in the background and have it to minor tasks for you if you're busy doing something else. 
It listens for the wake word which in my case is "hey ever" which it then is ready to take on your commands.


**Command**: go to chess.com
Opens a new window that goes to the specified website.

Command: what time is it?, or what's the time?
When this command is heard it calls a simple function that tells you the current time.

Command: what are, who is, what is a, who are the, what is the - ?
This command takes a question you have of something and uses the Wikipedia module and reads off the first two sentences of information.

Command: How is the weather in - ?
Given this command is a city name, it will look up the current weather of that city using the OpenWeatherMap api.

Command: what is the weather outside?, how is it outside?, what's the weather?
This command is much like the last weather command but instead this one returns your citys current weather. 

Command: Write this down.
This command is a more useful one, when this command is triggered you simply say the command, it then asks you 'what is it you want me to write down?'
You say whatever it is you'd like to be written down. It then takes what you say and creates a new notepad file with your information saved on that file.

Command: How do you spell - ?
This command is another super simple one, when this is triggered it takes the word you want to spell and repeats which character of the word back to you.

Command: Create new
This command is a bit more useful, the command is used for creating shopping lists. It works the same way as the 'write this down' command but instead of
opening a notepad file it sends you a text of the list you created using Twilio's API.

Command: what is today's date?
This commands is a simple one that when called tells back the date to the user.

Command: Send a text - 
This command when heard looks into a contacts database and searches for the matching information given by first and last name. It then asks what would you like
to say and sends a text to the number it finds related to the name.

Command: Odin Override:
This command is for other uses that you may want to add that need another level of authorisation. Example. You need a password for an account you have saved
in a database. You simply use the command, it then sends you a text with a six charactor number which you then repeat back to the assistant. Then you can carry on with
the information you want or whatever deed you program into it.
